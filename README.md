![A tied sack with its seal unbroken in the foreground, sorting tables with open and tied sacks, a ball of twine, lanterns, and tied bundles in the middle, and a pigeonhole wall behind, with no lettering anywhere](intro-banner.png)

> Sack label plate: the medium line of the sorting office, ruled like a label. A tiny seal glyph sits beside this heading and no other.

# codeintel-Code-Reachability-Analyzer

![A round brass hand stamp resting on the mouth of a tied canvas sack, its seal across the twine knot, with the name set beneath in Basic in storm slate, the heading plate](logo.png)

![The below decks sorting office: long sorting tables, canvas sacks heaped at their ends, a pigeonhole wall behind, one open sack and one tied sealed sack on the nearest table, and a canvas destination board across the table front carrying codeintel-code-reachability-analyzer in chalk white on storm slate](banner.png)

![The sorting office in three depths: the pigeonhole wall stays still while lantern light strengthens and weakens, bundles are divided between an open sack that takes them in and a tied sack they rest beside untouched, and a ball of twine turns slowly at the front edge while the seal stamp rests unmoving](scene.svg)


A tool that analyzes code to identify potentially unreachable code blocks based on static analysis. This can help identify dead code and potential logical errors. Works on the Python AST directly, checking each statement list for statements after a return, raise, break or continue, and reports every following statement in that list, each with its own line. An exclusion entry naming a directory excludes everything under it, and exclusion entries are compared as normalised absolute paths. A named file that cannot be read or parsed produces an error result and the run exits 1. - Focused on Tools for static code analysis, vulnerability scanning, and code quality assurance

> **Pigeonhole inset: the division this tool makes.** The checking works on the Python AST directly, list by list. What sits after a return, raise, break, or continue in the same list has no route onward, and every following statement in that list is reported, each with its own line.

![Major separator: a tied twine rule stretched edge to edge, one knot at its centre and a buoy orange seal dot beside the knot](sep-heavy.svg)

## Install
`git clone https://github.com/ShadowStrikeHQ/codeintel-code-reachability-analyzer`

> **Pigeonhole inset: clone line flagged.** The install line above points to ShadowStrikeHQ, not to ShadowGuard-AI. It is preserved as printed and flagged here, not quietly corrected.

![Minor separator: a short centred length of twine with one knot and a small seal dot](sep-light.svg)

## Usage
`./codeintel-code-reachability-analyzer [params]`

> **Pigeonhole inset: usage line flagged.** The usage line above is a placeholder. The README names no target file or directory argument at all, so a reader following the README alone would not know what to point the tool at.

![Major separator: a tied twine rule stretched edge to edge, one knot at its centre and a buoy orange seal dot beside the knot](sep-heavy.svg)

## Parameters
- `-h`: Show help message and exit
- `-v`: No description provided
- `-e`: List of files or directories to exclude from analysis.

> **Pigeonhole inset: -v has no description in the README.** The parameter list above leaves -v undescribed, exactly as the README leaves it. The -e entry carries the directory exclusion rule: an entry naming a directory excludes everything under it, and entries are compared as normalised absolute paths.

![Major separator: a tied twine rule stretched edge to edge, one knot at its centre and a buoy orange seal dot beside the knot](sep-heavy.svg)

## License
Copyright (c) ShadowStrikeHQ

> **Pigeonhole inset: copyright line flagged.** The closing line above reads Copyright (c) ShadowStrikeHQ, preserved as printed and flagged beside the install fault. A named file that cannot be read or parsed produces an error result and the run exits 1: that exit rule is stated in the opening paragraph above and is recorded here as the third matter these insets are reserved for.
