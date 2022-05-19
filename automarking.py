#!/usr/bin/python3

'''
NOTE:
1. If labs do not provide an AUTOMARKING_CONFIG_FILE, the DEFAULT_CONFIG
(all False) will be used:
    - coverage: boolean to indicate if coverage should be assessed.
    - lint: boolean to indicate if lint should be assessed.
    - server: boolean to indicate if a STUDENT_SERVER should be started.
    - coverage_factor: weighting of coverage (0-1)
    - lint_factor weighting of lint (0-1)
2. Test score is generated from our tests on student code.
3. Coverage score is generated from students tests on students code.
4. Lint score is COMP1531 on students.
5. See Mark Calculations in the relevant section in the code.
'''

# pylint: disable=missing-function-docstring,line-too-long,too-few-public-methods

import sys
import subprocess
import os
import json
import time
import glob
import textwrap

#=============================================================================#
# Settings (Note: other globals initiate in main)
#=============================================================================#

# Automarking Defaults
DEFAULT_CONFIG = {
    "coverage": False,
    "lint": False,
    "server": False,
    "coverage_factor": 0.2,
    "lint_factor": 0.1,
}

# Result output files
JEST_JSON = "__automarking_test__.json"
ESLINT_JSON = "__eslint_result___.json"
COVERAGE_JSON = "coverage/coverage-summary.json"
ARTEFACT_FILE = "mark.txt"

# Config files
AUTOMARKING_CONFIG_FILE = "automarking-config.json"

# Miscellaneous
JEST_TIMEOUT = 60
NUM_COMMITS = 5
SCORE_DECIMAL_PLACES = 2
STUDENT_SERVER = "src/server"
LINT_DIR = "src"

class Colour:
    '''
    For color printing
    '''
    F_Blue = "\x1b[34m"
    F_Red = "\x1b[31m"
    F_Green = "\x1b[32m"
    F_Yellow = "\x1b[33m"
    F_Magenta = "\x1b[35m"
    F_DarkGray = "\x1b[90m"
    F_LightGray = "\x1b[37m"
    F_Cyan = "\x1b[36m"
    F_LightMagenta = "\x1b[95m"
    F_LightYellow = "\x1b[93m"
    F_LightRed = "\x1b[91m"
    F_LightGreen = "\x1b[92m"
    F_LightBlue = "\x1b[94m"
    # Formatting
    BOLD = '\033[1m'
    # End colored text
    END = '\033[0m'
    NC ='\x1b[0m'

#=============================================================================#
# Marks Calculation (out of 1)
#=============================================================================#

def calculate_test_score(passed, total):
    return 0 if total == 0 else passed/total


def calculate_lint_score(errors, warnings):
    return max(0, 1 - (0.20 * errors) - (0.10 * warnings))


def calculate_coverage_score(line, branch, statement, function):
    coverage_items = [line, branch, statement, function]
    return 0 if 0 in coverage_items else (sum(coverage_items) / len(coverage_items)) / 100


def calculate_final_score(config, test_score, coverage_score, lint_score):
    coverage_factor = config['coverage_factor']
    lint_factor = config['lint_factor']

    if not config['coverage']:
        coverage_score, coverage_factor = 0, 0
    if not config['lint']:
        lint_score, lint_factor = 0, 0

    test_factor = round(1 - (coverage_factor + lint_factor), 2)

    if test_factor < 0:
        raise SystemExit("ERROR: Test factor should not be negative!")
    if sum([test_factor, coverage_factor, lint_factor]) > 1:
        print([test_factor, coverage_factor, lint_factor])
        raise SystemExit("ERROR: Sum of scale factors cannot be greater than 1!")

    final_score = round(
        (
            test_score * test_factor
            + coverage_score * coverage_factor
            + lint_score * lint_factor
        ),
        SCORE_DECIMAL_PLACES
    )

    return {
        'final_score': final_score,
        'test_factor': test_factor,
        'coverage_factor': coverage_factor,
        'lint_factor': lint_factor,
    }


def calculate_grade(percentage):
    # https://www.student.unsw.edu.au/grade
    if percentage > 100:
        return 'Error: Please notify a staff!'
    if percentage >= 85:
        return 'High Distinction (HD, 85-100)'
    if percentage >= 75:
        return 'Distinction (DN, 75-84)'
    if percentage >= 65:
        return 'Credit (CR, 65-74)'
    if percentage >= 50:
        return 'Pass (PS, 50-64)'
    return 'Fail (FL, 0-49)'


#=============================================================================#
# Setup
#=============================================================================#

def get_jest_config():
    """
    Will create jest.config.cjs for lab01-lab03

    '.cjs' file mainly because { "type": "module" } in lab03.
    """
    if os.path.exists("jest.config.js"):
        return "jest.config.js"

    with open("jest.config.cjs", 'w', encoding='utf-8') as file:
        file.write(textwrap.dedent("""\
            const config = {
              verbose: true,
            };

            module.exports = config;
            """)
        )
        return "jest.config.cjs"


def load_config():
    if not os.path.exists(AUTOMARKING_CONFIG_FILE):
        return DEFAULT_CONFIG

    with open(AUTOMARKING_CONFIG_FILE, 'r', encoding='utf-8') as file:
        return {**DEFAULT_CONFIG, **json.load(file)}


#=============================================================================#
# Subprocesses NPX
#=============================================================================#

def git_log(num_logs):
    print(Colour.F_Red, Colour.BOLD, f" \n=== Git Log (last {num_logs} commits) ===\n ")
    sys.stdout.flush()
    subprocess.run([
        'git', 'log', f'-{num_logs}', '--color', '--graph', '--abbrev-commit',
        '--pretty=tformat:%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cD) %C(bold blue)%an%Creset',
    ], check=False)


def start_server(coverage):
    args = ['npx']
    if coverage:
        args += ['nyc', '--reporter=json-summary']

    args += [ "ts-node", STUDENT_SERVER ]

    return subprocess.Popen(
        args,
        # stdout=subprocess.PIPE,
        # stderr=subprocess.DEVNULL,
    )


def npx_jest(coverage, is_automarking):
    args = [
        "npx",
        "jest",
        "--colors",
        "--verbose",
        "--runInBand",
        f"--config={JEST_CONFIG_FILE}",
    ]
    if coverage:
        args += [
            "--coverage",
            "--coverageReporters=text",
            "--coverageReporters=json-summary",
        ]

    if is_automarking:
        args += [
             "--json",
             f"--outputFile={JEST_JSON}",
            AUTOMARKING_TEST_FILE
        ]
    else:
        args.append(f"--testPathIgnorePatterns={AUTOMARKING_TEST_FILE}")

    try:
        subprocess.run(args, check=False, timeout=JEST_TIMEOUT)
    except subprocess.TimeoutExpired:
        print(f" \n> WARNING: Jest timed out after {JEST_TIMEOUT} seconds\n ")
        sys.stdout.flush()


def npx_eslint():
    args = [
        "npx",
        "eslint",
        "--color",
        LINT_DIR,
        "./**.js"
    ]

    subprocess.run(args, check=False)

    args += [
        "--format=json",
        f"--output-file={ESLINT_JSON}",
    ]
    return subprocess.run(args, check=False)


#=============================================================================#
# Utilities
#=============================================================================#

def jest_regular(coverage, is_automarking):
    npx_jest(coverage, is_automarking)


def jest_server(coverage, is_automarking):
    server = start_server(coverage)
    time.sleep(2)
    # Coverage is measured on the server itself, not from jest
    npx_jest(False, is_automarking)
    server.terminate()


def jest_execute(is_server, coverage, is_automarking):
    if is_server:
        jest_server(coverage, is_automarking)
    else:
        jest_regular(coverage, is_automarking)


def make_artefact(project_name, final_score):
    with open(ARTEFACT_FILE, 'w', encoding='utf-8') as file:
        file.write(f"{project_name}|{final_score}|")


def get_automarking_file():
    automarking_files = glob.glob('automarking.test.[jt]s')
    if len(automarking_files) != 1:
        raise SystemExit("Did not find exactly 1 test file:", automarking_files)
    return automarking_files[0]


def remove_if_exist(path):
    try:
        os.remove(path)
        print(f"- Removed '{path}'.")
    except OSError:
        print(f"- Failed to remove '{path}'.")


def cleanup():
    print(Colour.BOLD + Colour.F_Red + "CLEANUP: Cleaning generated files", Colour.NC)
    remove_if_exist("jest.config.cjs")
    remove_if_exist(ESLINT_JSON)
    remove_if_exist(ARTEFACT_FILE)
    remove_if_exist(JEST_JSON)


#=============================================================================#
# Get from JSON
#=============================================================================#

def get_jest_score_from_json():
    try:
        with open(JEST_JSON, "r", encoding='utf-8') as json_file:
            test_result = json.load(json_file)
            passed =  test_result.get('numPassedTests', 0)
            failed = test_result.get('numFailedTests', 0)
            total = test_result.get('numTotalTests', 0)
            score = calculate_test_score(passed, total)
            return { 'passed': passed, 'failed': failed, 'total': total, 'score': score }
    except FileNotFoundError:
        print(" \n> WARNING: Failed to read jest results\n ")
        sys.stdout.flush()
        return { 'passed': 0, 'failed': 0, 'total': 0, 'score': 0 }


def get_coverage_score_from_json():
    try:
        with open(COVERAGE_JSON, "r", encoding='utf-8') as json_file:
            coverage_result = json.load(json_file)["total"]
            line = coverage_result["lines"]['pct']
            branch = coverage_result["branches"]['pct']
            statement = coverage_result["statements"]['pct']
            function = coverage_result["functions"]['pct']
            if line == "Unknown":
                line, branch, statement, function = 0, 0, 0, 0
            score = calculate_coverage_score(line, branch, statement, function)
            return {
                'line': line, 'branch': branch, 'score': score,
                'statement': statement, 'function': function
            }
    except FileNotFoundError:
        print(" \n> WARNING: Failed to read coverage results\n ")
        sys.stdout.flush()
        return { 'line': 0, 'statement': 0, 'function': 0, 'branch': 0, 'score': 0 }


def get_lint_score_from_json():
    try:
        with open(ESLINT_JSON, "r", encoding='utf-8') as json_file:
            lint_results = json.load(json_file)
            errors = 0
            warnings = 0
            for entry in lint_results:
                errors += entry.get('errorCount', 0)
                warnings += entry.get('warningCount', 0)

            score = calculate_lint_score(errors, warnings)
            return { 'errors': errors, 'warnings': warnings, 'score': score }

    except FileNotFoundError:
        print(" \n> WARNING: Failed to read eslint results\n ")
        sys.stdout.flush()
        return { 'errors': 0, 'warnings': 0, 'score': 0 }


#=============================================================================#
# Display
#=============================================================================#

def output_results(config, project_name):
    jest = get_jest_score_from_json() or {}
    coverage = get_coverage_score_from_json() if config['coverage'] else {}
    lint = get_lint_score_from_json() if config['lint'] else {}

    result = calculate_final_score(
        config,
        jest.get('score', 0),
        coverage.get('score', 0),
        lint.get('score', 0),
    )

    print(' \n ')
    if jest:
        print(Colour.F_LightGreen + "===============================================")
        print(Colour.BOLD + Colour.F_Green + f"JEST (weighting: {result['test_factor']})", Colour.NC)
        print("- Staff automarking on student code")
        print(Colour.F_LightGreen + "===============================================", Colour.NC)
        print(f"Tests Passed   : {jest['passed']}")
        print(f"Tests Failed   : {jest['failed']}")
        print(f"Tests Total    : {jest['total']} ")
        print(Colour.F_LightGreen + f"Test Score     : {jest['score']:.2f}/1", Colour.NC)
        print(' \n ')

    if coverage:
        print(Colour.F_LightYellow + "===============================================")
        print(Colour.BOLD + Colour.F_Yellow + f"COVERAGE (weighting: {result['coverage_factor']})", Colour.NC)
        print("- Student or given tests on student code")
        print(("""\
  Note:
  - This is one way we have chosen to
  quantify your test quality.
  - Higher coverage can be achieved by
 testing many different scenarios.
  - This topic is not covered until week 8,
  so interpret the result however you like
  or conduct YOUR OWN further research.\
        """))
        print(Colour.F_LightYellow + "===============================================", Colour.NC)
        print(f"Line           : {coverage['line']}%")
        print(f"Statement      : {coverage['statement']}%")
        print(f"Function       : {coverage['function']}%")
        print(f"Branch         : {coverage['branch']}%")
        print(Colour.F_LightYellow + f"Coverage Score : {coverage['score']:.2f}/1", Colour.NC)
        print(' \n ')

    if lint:
        print(Colour.F_LightMagenta + "===============================================")
        print(Colour.BOLD + Colour.F_Magenta + f"ESLINT (weighting: {result['lint_factor']})", Colour.NC)
        print("- Staff lint on student code")
        print(Colour.F_LightMagenta + "===============================================", Colour.NC)
        print(f"Errors         : {lint['errors']}")
        print(f"Warnings       : {lint['warnings']}")
        print(Colour.F_LightMagenta + f"Lint Score     : {lint['score']:.2f}/1", Colour.NC)
        print(' \n ')

    percentage = round(result['final_score'] * 100)
    print(Colour.F_LightBlue + "===============================================", Colour.NC)
    print(Colour.BOLD + Colour.F_Blue + "AUTOMARKING RESULT", Colour.NC)
    print("- Combined score of all components")
    print(Colour.F_LightBlue + "===============================================", Colour.NC)
    print(f"Percentage     : {percentage}%")
    print(f"Final Grade    : {calculate_grade(percentage)}")
    print(Colour.F_LightBlue + f"Final Score    : {result['final_score']:.2f}/1", Colour.NC)
    print(' \n ')

    make_artefact(project_name, result['final_score'])


#=============================================================================#
# Driver
#=============================================================================#

def automarker(project_name):
    config = load_config()

    print(Colour.F_LightYellow, Colour.BOLD, " \n=== Staff Tests ===\n ", Colour.NC)
    sys.stdout.flush()
    jest_execute(config['server'], False, True)

    if config['coverage']:
        print(Colour.F_Green, Colour.BOLD, " \n=== Student Tests ===\n ", Colour.NC)
        sys.stdout.flush()
        jest_execute(config['server'], True, False)

    if config['lint']:
        print(Colour.BOLD + Colour.F_Magenta + " \n=== Running Lint ===\n ", Colour.NC, end='')
        sys.stdout.flush()
        if npx_eslint().returncode == 0:
            print("\nNo linting warnings or errors, well done!")

    output_results(config, project_name)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise SystemExit(f'Usage:\n  $ python3 {sys.argv[0]} $CI_PROJECT_NAME [OPTIONAL_DIR_PATH]')

    DEBUG = False
    if len(sys.argv) == 3:
        dir_path = sys.argv[2]
        print(f"cd {dir_path}")
        os.chdir(dir_path)
        DEBUG = True

    CI_PROJECT_NAME = sys.argv[1]
    AUTOMARKING_TEST_FILE = get_automarking_file()
    JEST_CONFIG_FILE = get_jest_config()

    print(Colour.BOLD + f" \nAutomarking {CI_PROJECT_NAME}" + Colour.NC)
    sys.stdout.flush()

    git_log(NUM_COMMITS)
    automarker(CI_PROJECT_NAME)

    if DEBUG:
        cleanup()
