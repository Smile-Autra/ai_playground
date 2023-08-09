import os
import subprocess
from typing import Tuple


def pytest_code(code_path: str) -> Tuple[bool, str]:
    try:
        # python3 -m pytest -v <code_path>
        output = subprocess.check_output(['python3', '-m', 'pytest', '-v', code_path])
    except subprocess.CalledProcessError as e:
        return False, e.output.decode('utf-8')
    return True, output.decode('utf-8')


def exec_code(module_path: str) -> Tuple[bool, str]:
    result = subprocess.run(['python3', '-m', module_path], capture_output=True)
    if result.stderr:
        raise RuntimeError('Execute code error:\n' + result.stderr.decode('utf-8'))
    return True, result.stdout.decode('utf-8')
