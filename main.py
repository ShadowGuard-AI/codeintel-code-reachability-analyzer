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
        list: A list of line numbers where unreachable code is suspected.
              Returns an empty list if no unreachable code is suspected.
              Returns None if the file could not be read or parsed, so
              the caller can tell an error apart from a clean file.
    """
    try:
        with open(file_path, "r") as f:
            source_code = f.read()
        tree = ast.parse(source_code)
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
        return None
    except SyntaxError as e:
        logging.error(f"Syntax error in {file_path}: {e}")
        return None
    except Exception as e:
        logging.error(f"An unexpected error occurred while analyzing {file_path}: {e}")
        return None

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
                    # I flag every later statement in the list, even when the
                    # terminator sits inside a condition I cannot evaluate. Code
                    # after an if that returns is reachable when the branch is not
                    # taken, so this list is suspects to read, not proof.
                    for following in value[index + 1:]:
                        if hasattr(following, 'lineno'):
                            unreachable.add(following.lineno)
    # I collect in a set because one line can follow terminators in
    # more than one enclosing list. Sorting at the end gives the
    # caller line order instead of walk order.
    return sorted(unreachable)


def is_excluded(file_path, exclude_list):
    """
    Compares normalised absolute paths. An exclusion entry that is a
    directory excludes everything under it; a file entry excludes
    that file, whatever spelling the path was given in.
    """
    file_abs = os.path.abspath(file_path)
    for entry in exclude_list:
        # I resolve a relative entry against the caller's working
        # directory, not against the target. An exclude written for one
        # directory run from another can quietly match nothing.
        entry_abs = os.path.abspath(entry)
        if file_abs == entry_abs or file_abs.startswith(entry_abs + os.sep):
            return True
    return False

def process_file_or_directory(file_or_directory, exclude_list):
    """
    Processes a file or directory, analyzing each Python file.

    Args:
        file_or_directory (str): Path to the file or directory.
        exclude_list (list): List of files or directories to exclude.

    Returns:
        bool: True if any file could not be read or parsed, False otherwise.
    """
    had_error = False
    if os.path.isfile(file_or_directory):
        if file_or_directory.endswith(".py") and not is_excluded(file_or_directory, exclude_list):
            logging.info(f"Analyzing file: {file_or_directory}")
            unreachable_lines = is_code_reachable(file_or_directory)
            if unreachable_lines is None:
                had_error = True
            elif unreachable_lines:
                print(f"Unreachable code suspected in {file_or_directory} at lines: {unreachable_lines}")
    elif os.path.isdir(file_or_directory):
        for root, dirs, files in os.walk(file_or_directory):
            dirs[:] = [d for d in dirs if not is_excluded(os.path.join(root, d), exclude_list)]
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    if not is_excluded(file_path, exclude_list):
                        logging.info(f"Analyzing file: {file_path}")
                        unreachable_lines = is_code_reachable(file_path)
                        if unreachable_lines is None:
                            had_error = True
                        elif unreachable_lines:
                            print(f"Unreachable code suspected in {file_path} at lines: {unreachable_lines}")
    else:
        logging.error(f"Invalid file or directory: {file_or_directory}")
        had_error = True
    return had_error


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

    if process_file_or_directory(file_or_directory, exclude_list):
        sys.exit(1)

if __name__ == "__main__":
    """
    Entry point for the script.
    """
    main()

