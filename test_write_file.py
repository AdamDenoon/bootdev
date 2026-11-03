from functions.write_file import write_file

def run_test(working_dir, file_path, content):
    try:
        print(f'Result for \'{file_path}\':')
        text = write_file(working_dir, file_path, content)
        print(f"{text}")
    except RuntimeError as err:
        print(f'Error: {err}')

def main():
    run_test("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
    run_test("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
    run_test("calculator", "/tmp/temp.txt", "this should not be allowed")

if __name__ == "__main__":
    main()

