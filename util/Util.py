import aiofiles


async def read_env_to_dict(env_path) -> dict:
    env_dict = {}
    async with aiofiles.open(env_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith('#'):
                key, value = line.split('=', 1)
                env_dict[key] = value
    return env_dict
