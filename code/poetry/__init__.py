"""Auxiliar module to implement Poetry commands."""

import subprocess as sp
from shutil import which


def lint():
    """Run Black as linter."""
    print("====| LINT: RUNNING BLACK")
    if which("black"):
        sp.check_call("black --check .", shell=True)
    else:
        _missing_command("black")


def format_code():
    """Format code."""
    print("====| FORMAT: RUNNING BLACK")
    if which("black"):
        sp.check_call("black .", shell=True)
    else:
        _missing_command("black")


def _missing_command(command):
    """Print error with command"""
    print("====| ERROR: WRONG COMMAND: " + command)
