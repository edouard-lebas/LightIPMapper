import argparse
from src.utils import YELLOW, ENDC, list_files_in_directory
from src.file_analyzer import FileAnalyzer
from src.ip_mapper import IpMapper

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze files and map IP addresses")
    parser.add_argument('-d', '--directory', required=True, help="Directory path to analyze")
    args = parser.parse_args()

    print(f"{YELLOW}🔍 Analyzing directory: {args.directory}{ENDC}")

    file_paths = list_files_in_directory(args.directory)

    continue_script = input("Do you want to continue? (y/n): ").strip().lower()
    if continue_script != 'y':
        print(f"{YELLOW}🛑 Script terminated by the user.{ENDC}")
        exit(1)

    analyzer = FileAnalyzer(file_paths)
    analyzer.extract_ips()
    analyzer.locate_ips()

    mapper = IpMapper(analyzer.ip_locations, analyzer.unlocated_ips)
    mapper.create_map()
