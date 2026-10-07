# Copyright (c) 2026, The application provides centralized HR management with configurable workflows, employee self-service capabilities, attendance and leave management, payroll processing, and reporting to improve HR efficiency and compliance. and Contributors
# See license.txt

# import frappe
from frappe.tests import IntegrationTestCase


# On IntegrationTestCase, the doctype test records and all
# link-field test record dependencies are recursively loaded
# Use these module variables to add/remove to/from that list
EXTRA_TEST_RECORD_DEPENDENCIES = []  # eg. ["User"]
IGNORE_TEST_RECORD_DEPENDENCIES = []  # eg. ["User"]



class IntegrationTestMonthlyEmployeeAllowance(IntegrationTestCase):
	"""
	Integration tests for MonthlyEmployeeAllowance.
	Use this class for testing interactions between multiple components.
	"""

	pass
