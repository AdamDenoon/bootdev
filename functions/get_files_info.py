import os

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}
def get_files_info(working_directory: str, directory: str=".") -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        return directory_info(target_dir)
    
    except RuntimeError as err:
        return f'Error: {err}'

def directory_info(directory):
    results = []

    for name in os.listdir(directory):
        path = os.path.join(directory, name)
        file_size = os.path.getsize(path)
        is_dir = os.path.isdir(path)

        results.append(
            f"- {name}: file_size={file_size} bytes, is_dir={is_dir}"
        )

    return "\n".join(results)
