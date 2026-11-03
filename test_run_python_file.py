from functions.run_python_file import run_python_file

def run_test(working_dir: str, file_path: str, args: list[str] | None = None):
    try:
        print(f'Result for \'{file_path}\':')
        text = run_python_file(working_dir, file_path, args)
        print(f"{text}")
    except RuntimeError as err:
        print(f'Error: {err}')

def main():
    run_test("calculator", "main.py")
    run_test("calculator", "main.py", ["3 + 5"])
    run_test("calculator", "tests.py")
    run_test("calculator", "../main.py")
    run_test("calculator", "nonexistent.py")
    run_test("calculator", "lorem.txt")

if __name__ == "__main__":
    main()

