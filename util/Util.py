import aiofiles
import importlib.util
import os


async def read_env_to_dict(env_path) -> dict:
    env_dict = {}
    async with aiofiles.open(env_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith('#'):
                key, value = line.split('=', 1)
                env_dict[key] = value
    return env_dict


def load_class_from_file_path(file_path, *args, **kwargs):
    """
    Load and instantiate a class from a given Python file, assuming the class name matches the file name.

    Args:
        file_path (str): The full path to the Python file.
        *args: Arguments to pass to the class constructor.
        **kwargs: Keyword arguments to pass to the class constructor.

    Returns:
        An instance of the specified class.

    Raises:
        ImportError: If the spec or module cannot be loaded, or class not found.
        FileNotFoundError: If the file does not exist.
    """
    # Verify the file exists
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"No such file: {file_path}")

    # Extract the class name from the file name
    class_name = os.path.splitext(os.path.basename(file_path))[0]

    # Load the module from the given file path
    spec = importlib.util.spec_from_file_location(class_name, file_path)
    if spec is None:
        raise ImportError(f"Could not load spec from {file_path}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # Get the class and instantiate it
    if hasattr(module, class_name):
        cls = getattr(module, class_name)
        return cls(*args, **kwargs)
    else:
        raise ImportError(f"Class {class_name} not found in {file_path}")
