![Banner](banner.png)

# codeintel-Code-Reachability-Analyzer
A tool that analyzes code to identify potentially unreachable code blocks based on static analysis. This can help identify dead code and potential logical errors. Works on the Python AST directly, checking each statement list for statements after a return, raise, break or continue, and reports every following statement in that list, each with its own line. An exclusion entry naming a directory excludes everything under it, and exclusion entries are compared as normalised absolute paths. A named file that cannot be read or parsed produces an error result and the run exits 1. - Focused on Tools for static code analysis, vulnerability scanning, and code quality assurance

## Install
`git clone https://github.com/ShadowStrikeHQ/codeintel-code-reachability-analyzer`

## Usage
`./codeintel-code-reachability-analyzer [params]`

## Parameters
- `-h`: Show help message and exit
- `-v`: No description provided
- `-e`: List of files or directories to exclude from analysis.

## License
Copyright (c) ShadowStrikeHQ
