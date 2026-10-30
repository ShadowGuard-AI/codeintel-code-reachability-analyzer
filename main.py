import argparse
import logging
import os
import sys
import ast

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def setup_argparse():
    """
    Sets up the argument parser for the code reachability analyzer.
    """
    parser = argparse.ArgumentParser(description="Analyze code for unreachable code blocks.")
    parser.add_argument("file_or_directory", help="Path to the Python file or directory to analyze.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output (debug logging).")
    parser.add_argument("-e", "--exclude", nargs="+", help="List of files or directories to exclude from analysis.", default=[])  # Added exclude option

    return parser.parse_args()

def is_code_reachable(file_path):
    """
    Analyzes a Python file to identify potentially unreachable code blocks.

    Args:
        file_path (str): Path to the Python file.

    Returns:
        list: A list of line numbers where unreachable code is suspected.  Returns an empty list if no unreachable code is suspected or if there's an error.
    """
    try:
        with open(file_path, "r") as f:
            source_code = f.read()
        tree = ast.parse(source_code)
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
        return []
    except SyntaxError as e:
        logging.error(f"Syntax error in {file_path}: {e}")
        return []
    except Exception as e:
        logging.error(f"An unexpected error occurred while analyzing {file_path}: {e}")
        return []

    # Unreachability is a property of a statement list: the statement
    # after a return, raise, break or continue in the same list cannot
    # run. The old code looked at the terminator's immediate AST
    # parent and only proceeded when that parent was the function
    # itself, so a return inside an if, loop or try block, which is
    # where terminators usually sit, was never checked at all.
    # Walking every statement list (body, orelse, finalbody, handler
    # and case bodies all appear as list fields) covers those nests
    # without special casing each compound statement.
    terminators = (ast.Return, ast.Raise, ast.Break, ast.Continue)
    unreachable = set()
    for node in ast.walk(tree):
        for _field, value in ast.iter_fields(node):
            if not isinstance(value, list) or not value:
                continue
            if not all(isinstance(item, ast.stmt) for item in value):
                continue
            for index, statement in enumerate(value[:-1]):
                if isinstance(statement, terminators):
                    following = value[index + 1]
                    if hasattr(following, 'lineno'):
                        unreachable.add(following.lineno)
    return sorted(unreachable)

def process_file_or_directory(file_or_directory, exclude_list):
    """
    Processes a file or directory, analyzing each Python file.

    Args:
        file_or_directory (str): Path to the file or directory.
        exclude_list (list): List of files or directories to exclude.
    """
    if os.path.isfile(file_or_directory):
        if file_or_directory.endswith(".py") and file_or_directory not in exclude_list:
            logging.info(f"Analyzing file: {file_or_directory}")
            unreachable_lines = is_code_reachable(file_or_directory)
            if unreachable_lines:
                print(f"Unreachable code suspected in {file_or_directory} at lines: {unreachable_lines}")
    elif os.path.isdir(file_or_directory):
        for root, _, files in os.walk(file_or_directory):
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    if file_path not in exclude_list:
                        logging.info(f"Analyzing file: {file_path}")
                        unreachable_lines = is_code_reachable(file_path)
                        if unreachable_lines:
                            print(f"Unreachable code suspected in {file_path} at lines: {unreachable_lines}")
    else:
        logging.error(f"Invalid file or directory: {file_or_directory}")


def main():
    """
    Main function to execute the code reachability analyzer.
    """
    args = setup_argparse()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logging.debug("Verbose mode enabled.")

    file_or_directory = args.file_or_directory
    exclude_list = args.exclude

    # Validate inputs
    if not os.path.exists(file_or_directory):
        logging.error(f"Error: {file_or_directory} does not exist.")
        sys.exit(1)

    for item in exclude_list:
        if not os.path.exists(item):
            logging.warning(f"Warning: Exclude path {item} does not exist.")

    process_file_or_directory(file_or_directory, exclude_list)

if __name__ == "__main__":
    """
    Entry point for the script.
    """
    main()

