import os

# ANSI color codes for colored output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
ENDC = '\033[0m'  # Reset to default color


def list_files_in_directory(directory_path):
    """
    Lists all files in the specified directory and returns their full paths.
    """
    try:
        if not os.path.isdir(directory_path):
            print(f"{RED}❌ The provided path is not a directory: {directory_path}{ENDC}")
            exit(1)

        files = [os.path.join(directory_path, file) for file in os.listdir(directory_path)]
        print(f"{BLUE}📁 Files in the directory {directory_path}:{ENDC}")
        for file in files:
            print(f"{GREEN}📄 {file}{ENDC}")
        return files

    except Exception as e:
        print(f"{RED}❌ An error occurred: {e}{ENDC}")
        exit(1)
