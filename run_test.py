#!/usr/bin/env python3
import os
import sys
import subprocess

if __name__ == "__main__":
    # Set the Django settings module
    os.environ['DJANGO_SETTINGS_MODULE'] = 'DjangoProject.settings'
    
    # Run the original command
    cmd = ['python3', '-m', 'unittest', 'event.tests.TriggerAlarmTestCase']
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    # Print the output
    print("STDOUT:")
    print(result.stdout)
    
    print("\nSTDERR:")
    print(result.stderr)
    
    # Exit with the same status code
    sys.exit(result.returncode)