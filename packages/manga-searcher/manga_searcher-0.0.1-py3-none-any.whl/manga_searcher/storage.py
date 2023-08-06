# For type hinting Any type.
from typing import Any

# For serialization.
import pickle

# For making storage directory.
from dir_handeler.dir import Dir

from myanimelist_downloader.downloader import Dir


def store(data_directory: Dir, key: str, value: Any = None) -> Any:
    """Store/retrive value.

    Args:
        key (str): Key for value.
        value (Any, optional): Value or callable to get value. Defaults to None.

    Returns:
        Any: Stored value.
    """

    # Generate filepath.
    filepath: str = Dir("storage", data_directory).file_path(key)

    # Was value callable?
    value_callable: bool = callable(value)

    # Try to write or read.
    try:
        # Open file.
        with open(
            filepath,
            "{type}b".format(type="w" if value and not value_callable else "r"),
        ) as file:
            # Write value to file.
            if value and not value_callable:
                pickle.dump(value, file)
                return value
            # Read value from file.
            else:
                try:
                    return pickle.load(file)
                # Unpickling failed.
                except pickle.UnpicklingError:
                    # If value was callable, set to call output.
                    if value_callable:
                        return store(
                            data_directory=data_directory, key=key, value=value()
                        )
                    # Value was not callable so just return None.
                    else:
                        return None
    # If file was not found.
    except FileNotFoundError:
        # If value was callable, set to call output.
        if value_callable:
            return store(data_directory=data_directory, key=key, value=value())
        # Value was not callable so just return None.
        else:
            return None
