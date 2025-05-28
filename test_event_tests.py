#!/usr/bin/env python3
import os
import sys
import unittest

if __name__ == "__main__":
    # Set the Django settings module
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoProject.settings')

    # Initialize Django
    import django
    django.setup()

    # Run migrations to ensure database tables exist
    from django.core.management import call_command
    call_command('migrate', interactive=False)

    # Load the test case
    from event.tests import TriggerAlarmTestCase

    # Create a test suite with the TriggerAlarmTestCase
    suite = unittest.TestLoader().loadTestsFromTestCase(TriggerAlarmTestCase)

    # Run the tests
    result = unittest.TextTestRunner().run(suite)

    # Exit with appropriate status code
    sys.exit(not result.wasSuccessful())
