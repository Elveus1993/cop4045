"""
Problem 1 - Line Numbering and Function Parser
Homework 2 - CS Assignment
"""

import ast
import io
import tokenize


def line_number(input_file: str, output_file: str) -> None:
    """
    Read lines from input_file and write them to output_file with line numbers.

    Each line is prefixed with its line number in the format:
    "1. import math" -- number, period, space, then original line content.

    Args:
        input_file: Path to the file to read from.
        output_file: Path to the file to write to.

    Returns:
        None

    Raises:
        Exception: Re-raises any exception encountered after printing
            a user-friendly error message to the terminal.
    """
    try:
        with open(input_file, 'r') as infile:
            lines = infile.readlines()

        with open(output_file, 'w') as outfile:
            for i in range(len(lines)):
                outfile.write(f"{i + 1}. {lines[i]}")

        print(f"Successfully wrote numbered lines to '{output_file}'.")

    except FileNotFoundError:
        print(f"Error: File '{input_file}' was not found.")
        raise
    except PermissionError:
        print(f"Error: Permission denied when accessing '{input_file}'.")
        raise
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise


def _strip_comments(source: str) -> str:
    """
    Remove all comment tokens (whole-line and inline) from Python source.

    Uses tokenize so that '#' characters inside string literals are
    preserved. Comment tokens are replaced with nothing; everything else
    is kept verbatim.

    Args:
        source: Python source code as a string.

    Returns:
        str: Source with all comments removed.
    """
    result_tokens = []
    readline = io.StringIO(source).readline

    for tok in tokenize.generate_tokens(readline):
        if tok.type == tokenize.COMMENT:
            continue
        result_tokens.append(tok)

    return tokenize.untokenize(result_tokens)


def parse_functions(filename: str) -> tuple:
    """
    Parse a Python file and extract all top-level function definitions.

    Reads the file, uses ast to locate function definitions, and returns
    a tuple of tuples sorted alphabetically by function name. Each inner
    tuple contains exactly four elements:
        (line_number, function_name, arg_string, function_code_string)

    The function_code_string contains the signature and body, with all
    empty lines and comments (whole-line and inline trailing) removed.
    Only top-level functions are included; nested functions are excluded.

    Args:
        filename: Path to the Python file to parse.

    Returns:
        tuple: Tuple of 4-element tuples, sorted alphabetically by
            function name. Empty tuple if no functions are found.

    Raises:
        Exception: Re-raises any exception encountered after printing
            a user-friendly error message to the terminal.
    """
    try:
        with open(filename, 'r') as infile:
            source = infile.read()

        lines = source.split('\n')
        tree = ast.parse(source)

        results = []

        # Only walk top-level functions (children of the Module node)
        for node in tree.body:
            if isinstance(node, ast.FunctionDef):
                func_name = node.name
                line_no = node.lineno
                end_line = node.end_lineno

                # Element 2: formal argument list as a string
                args = [arg.arg for arg in node.args.args]
                arg_string = ', '.join(args)

                # Extract raw source lines for this function
                func_lines = lines[line_no - 1:end_line]
                func_source = '\n'.join(func_lines)

                # Strip all comments (whole-line + inline) safely
                stripped_source = _strip_comments(func_source)

                # Remove empty / whitespace-only lines
                cleaned_lines = [
                    line for line in stripped_source.split('\n')
                    if line.strip() != ''
                ]
                function_code = '\n'.join(cleaned_lines) + '\n'

                results.append(
                    (line_no, func_name, arg_string, function_code)
                )

        # Sort alphabetically by function name (index 1)
        results.sort(key=lambda t: t[1])

        return tuple(results)

    except FileNotFoundError:
        print(f"Error: File '{filename}' was not found.")
        raise
    except SyntaxError as e:
        print(f"Error: Syntax error in '{filename}': {e}")
        raise
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise


def main() -> None:
    """
    Main program: tests line_number and parse_functions on this file.

    Writes numbered output to a separate .txt file so the original
    source .py file is never overwritten.
    """
    # Part (a): line_number test on this source file
    input_file = "funs.py"
    output_file = "funs_output.txt"

    print("=== Part (a): line_number ===")
    line_number(input_file, output_file)

    # Part (b): parse_functions test on this source file
    print("\n=== Part (b): parse_functions ===")
    funcs = parse_functions(input_file)


    for func in funcs:
        print(f"\nLine {func[0]}: {func[1]}({func[2]})")
        print("-" * 40)
        print(func[3])

    # print("\nRaw tuple:")
    # print(funcs)

    
if __name__ == "__main__":
    main()