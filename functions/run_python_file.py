import os
import subprocess

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Executes a python file, returning its STDOUT and STDERR, if any",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path to execute, relative to the working directory (default is the working directory itself)",
                },
                "args": {
                    "type": ["array", "null"],
                    "items": {"type": "string"},
                    "description": "Arguments for execution",
                },
            },
        },
    },
}
def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        target_file_abs = os.path.abspath(target_file)
        valid_target_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs

        if not valid_target_file:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not target_file.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_file_abs]

        if args is not None:
            command.extend(args)


        print(f"command: {command}")

        completed = subprocess.run(command, capture_output=True, timeout=30, text=True, check=True, cwd=working_dir_abs)

        if completed.returncode != 0:
            return f"Process exited with code {completed.returncode}"

        if not len(completed.stdout) > 0 and not len(completed.stderr) > 0:
            return f"No output produced"

        output = ""

        if len(completed.stdout) > 0:
            output += f"STDOUT: {completed.stdout}"

        if len(completed.stderr) > 0:
            output += f"STDERR: {completed.stderr}"

        return output
                
    except RuntimeError as err:
        return f'Error executing Python file: {err}'
    except FileNotFoundError as err:
        return f'Error executing Python file: \'{err}\''