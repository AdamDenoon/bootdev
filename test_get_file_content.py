from functions.get_file_content import get_file_content

def run_test(working_dir, file_path, print_file=False):
    try:
        print(f'Result for \'{file_path}\':')
        text = get_file_content(working_dir, file_path)
        print(f"{file_path} length: {len(text)}")
        print(f"{file_path} truncated: {'truncated' in text}")
        if print_file:
            print("\n".join("  " + line for line in text.split("\n")))
    except RuntimeError as err:
        print(f'Error: {err}')

def main():
    run_test("calculator", "lorem.txt")
    run_test("calculator", "main.py", True)
    run_test("calculator", "pkg/calculator.py", True)
    run_test("calculator", "/bin/cat", True)
    run_test("calculator", "pkg/does_not_exist.py", True)

if __name__ == "__main__":
    main()

