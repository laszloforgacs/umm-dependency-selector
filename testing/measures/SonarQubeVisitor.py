import asyncio
import base64
import os
from typing import Final

import requests
from dotenv import set_key, find_dotenv

from data.repository.SourceRepositoryImpl import SOURCE_TEMP_DIR
from presentation.core.visitors.Visitor import BaseMeasureVisitor
from source_temp.PyGithub.github.Repository import Repository
from util.GithubRateLimiter import GithubRateLimiter

"""
"""

SONAR_BASE_URL: Final = "http://localhost:9000"
GLOBAL_ANALYSIS_TOKEN: Final = "GLOBAL_ANALYSIS_TOKEN"
UMM_DEPENDENCY_SELECTOR_GLOBAL_TOKEN: Final = "UMM_DEPENDENCY_SELECTOR_GLOBAL_TOKEN"

plugins_to_install = [
    "java",
    "python",
    "javascript",
    "typescript",
    "php",
    "csharp",
    "cpp",
    "ruby",
    "swift",
    "kotlin",
    "go",
    "scala",
    "web",
    "cssfamily",
    "xml",
    "vbnet"
]


class SonarQubeVisitor(BaseMeasureVisitor[dict]):
    def __init__(self, github_rate_limiter: GithubRateLimiter):
        super().__init__()

    async def measure(self, measure: 'BaseMeasure', repository: Repository) -> dict:
        try:
            cached_result = await self.get_cached_result(measure, repository)
            if cached_result is not None:
                return cached_result

            username, password = self._get_user_credentials()
            encoded_credentials = self._encode_credentials(username, password)

            sonarqube_admin = self._get_admin_user(encoded_credentials)

            if sonarqube_admin is None:
                # TODO: fix this
                return 0.0

            user_tokens = sonarqube_admin.get('userTokens', [])
            global_token = next(
                (token for token in user_tokens if
                 token.get('type', None) == GLOBAL_ANALYSIS_TOKEN and token.get('isExpired', False) is False),
                None)

            if global_token is None:
                result = self._create_user_token(encoded_credentials)

                # TODO: fix this
                if result is None:
                    return 0.0

                token = result.get('token')

                # TODO: fix this
                if token is None:
                    return 0.0

                set_key(find_dotenv(), UMM_DEPENDENCY_SELECTOR_GLOBAL_TOKEN, token)

                global_token = token
            else:
                global_token = os.getenv(UMM_DEPENDENCY_SELECTOR_GLOBAL_TOKEN)

            installed_plugin_keys = self._get_installed_plugin_keys(encoded_credentials)
            missing_plugin_keys = [plugin for plugin in plugins_to_install if plugin not in installed_plugin_keys]

            # TODO: Install missing plugins - cant do it without accepting the consent
            # for plugin_key in missing_plugin_keys:
            # self._install_plugin(encoded_credentials, plugin_key)

            sonar_projects = self._get_sonar_projects(encoded_credentials, repository)
            # TODO: fix this
            if sonar_projects is None:
                return 0.0

            components = sonar_projects.get('components', [])
            sonar_project = next(
                (component for component in components if
                 component.get('key', None) == repository.full_name.replace('/', '-')),
                None
            )

            if sonar_project is None:
                result = self._create_sonar_project(encoded_credentials, repository)
                if result is None:
                    return 0.0

                sonar_project = result.get('project')

            await self._scan_sonar_project(global_token, repository)

            metric_keys = self._get_available_metric_keys(encoded_credentials)

            measures_dict = self._get_measures_dict(encoded_credentials, repository, metric_keys)

            await self.cache_result(measure, repository, measures_dict)

            return measures_dict

        except Exception as e:
            raise Exception(str(e) + self.__class__.__name__)

    def _get_admin_user(self, encoded_credentials: str):
        url = f"{SONAR_BASE_URL}/api/user_tokens/search"
        headers = {
            'Authorization': f"Basic {encoded_credentials}"
        }
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code}")
            return None

    def _get_user_credentials(self) -> tuple[str, str]:
        username = os.getenv('SONARQUBE_ADMIN_USER')
        password = os.getenv('SONARQUBE_ADMIN_PASSWORD')
        return username, password

    def _create_user_token(self, encoded_credentials: str):
        url = f"{SONAR_BASE_URL}/api/user_tokens/generate"
        headers = {
            'Authorization': f"Basic {encoded_credentials}"
        }
        params = {
            "name": "UMM-Dependency Selector Global Token",
            "type": GLOBAL_ANALYSIS_TOKEN
        }

        response = requests.post(url, headers=headers, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code}")
            return None

    def _get_sonar_projects(self, encoded_credentials: str, repository: Repository):
        url = f"{SONAR_BASE_URL}/api/projects/search"
        headers = {
            'Authorization': f"Basic {encoded_credentials}"
        }
        params = {
            "projects": repository.full_name.replace('/', '-')
        }

        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code}")
            return None

    def _create_sonar_project(self, encoded_credentials: str, repository: Repository):
        url = f"{SONAR_BASE_URL}/api/projects/create"
        headers = {
            'Authorization': f"Basic {encoded_credentials}"
        }
        params = {
            "name": repository.full_name.replace('/', '-'),
            "project": repository.full_name.replace('/', '-'),
            "mainBranch": repository.default_branch
        }

        response = requests.post(url, headers=headers, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code}")
            return None

    async def _scan_sonar_project(self, global_token: str, repository: Repository):
        cmd = " ".join([
            "docker run",
            "--rm",
            f"-e SONAR_HOST_URL=http://host.docker.internal:9000",
            f"-e SONAR_SCANNER_OPTS='-Dsonar.projectKey={repository.full_name.replace('/', '-')} -Dsonar.exclusions=**/*.java,**/*.cs,**/*.cpp,**/*.class,**/*.h,**/*.hpp,**/*.cxx,**/*.c,**/*.cc,**/*.swift,**/*.obj,**/*.scala,**/*.vb,**/*.asm,**/*.go,**/*.pyc,**/*.pas,**/*.fs,**/*.r,**/*.d,**/*.sln,**/*.suo,**/*.exe,**/*.dll,**/*.so,**/*.dylib'",
            f"-e SONAR_TOKEN='{global_token}'",
            f"-v {os.getcwd()}/{SOURCE_TEMP_DIR}/{repository.name}:/usr/src",
            "sonarsource/sonar-scanner-cli"
        ])

        print(f"Scanning {repository.full_name}")

        process = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await process.communicate()

        if stderr:
            print("sonar-scanner has encountered an error")
            print(stderr.decode())

        if stdout:
            print("sonar-scanner has finished")
            print(stdout.decode())

    def _get_installed_plugin_keys(self, encoded_credentials: str) -> list[str]:
        url = f"{SONAR_BASE_URL}/api/plugins/installed"
        headers = {
            'Authorization': f"Basic {encoded_credentials}"
        }

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            result = response.json()
            plugins = result.get('plugins', [])
            plugin_keys = []
            for plugin in plugins:
                key = plugin.get('key', None)
                if key is not None:
                    plugin_keys.append(key)

            return plugin_keys
        else:
            print(f"Error: {response.status_code}")
            return []

    def _install_plugin(self, encoded_credentials: str, plugin_key: str):
        url = f"{SONAR_BASE_URL}/api/plugins/install"
        headers = {
            'Authorization': f"Basic {encoded_credentials}"
        }

        params = {
            "key": plugin_key
        }

        print(f"Installing plugin {plugin_key}")

        response = requests.post(url, headers=headers, params=params)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code}")
            return None

    def _get_available_metric_keys(self, encoded_credentials: str) -> list[str]:
        url = f"{SONAR_BASE_URL}/api/metrics/search"
        headers = {
            'Authorization': f"Basic {encoded_credentials}"
        }
        params = {
            "ps": 500
        }

        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            result = response.json()
            metrics = result.get('metrics', [])
            metric_keys = []
            for metric in metrics:
                key = metric.get('key', None)
                if key is not None:
                    metric_keys.append(key)

            return metric_keys
        else:
            print(f"Error: {response.status_code}")
            return []

    def _get_measures_dict(
            self,
            encoded_credentials: str,
            repository: Repository,
            metric_keys: list[str]
    ) -> dict[str, str]:
        url = f"{SONAR_BASE_URL}/api/measures/component"
        headers = {
            'Authorization': f"Basic {encoded_credentials}"
        }
        params = {
            "component": repository.full_name.replace('/', '-'),
            "metricKeys": ",".join(metric_keys)
        }

        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            result = response.json()
            measures = result.get('component', {}).get('measures', [])
            measures_dict = {}
            for measure in measures:
                key = measure.get('metric', None)
                value = measure.get('value', None)
                if key is not None and value is not None:
                    measures_dict[key] = value

            return measures_dict
        else:
            print(f"Error: {response.status_code}")
            return {}

    def _encode_credentials(self, username: str, password: str) -> str:
        string_to_encode = f"{username}:{password}"
        return base64.b64encode(string_to_encode.encode()).decode()
