from functions.get_files_info import get_files_info

def run_test(working_dir, dir):
    try:
        if dir == ".":
            print('Result for current directory:')
        else:
            print(f'Result for \'{dir}\' directory:')
        text = get_files_info(working_dir, dir)
        print("\n".join("  " + line for line in text.split("\n")))
    except RuntimeError as err:
        print(f'Error: {err}')

def main():
    run_test("calculator", ".")
    run_test("calculator", "/bin")
    run_test("calculator", "../")
    run_test("calculator", "pkg")

if __name__ == "__main__":
    main()

