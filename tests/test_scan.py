# tests/test_scan.py
import subprocess
import pytest
from modules import scan # Import your scan module

def test_scan_start_calls_airodump(mocker):
    """
    Tests if scan.start() calls subprocess.run with the correct command.
    """
    # 1. 'mocker' comes from pytest-mock.
    # 2. We "patch" (replace) the real 'subprocess.run' with a mock object.
    mock_run = mocker.patch('subprocess.run')

    # 3. Run your function
    scan.start('wlan0')

    # 4. Assert (check) that the mock was called exactly once
    #    with the command we expected.
    mock_run.assert_called_once_with(['airodump-ng', 'wlan0'])

def test_scan_start_handles_keyboard_interrupt(mocker):
    """
    Tests if scan.start() correctly handles Ctrl+C (KeyboardInterrupt)
    and prints a message instead of crashing.
    """
    # 1. Patch subprocess.run and make it *raise* a KeyboardInterrupt
    #    when it's called.
    mocker.patch('subprocess.run', side_effect=KeyboardInterrupt)
    
    # 2. Patch 'colorful_print' to check what it prints
    mock_print = mocker.patch('modules.scan.colorful_print')

    # 3. Run the function
    scan.start('wlan0')

    # 4. Assert that the friendly "Scan stopped" message was printed.
    mock_print.assert_called_with("\nScan stopped. Returning to main menu.", "green")
