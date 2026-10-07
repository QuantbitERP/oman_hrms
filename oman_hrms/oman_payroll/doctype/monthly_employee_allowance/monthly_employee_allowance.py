# Copyright (c) 2026, The application provides centralized HR management with configurable workflows, employee self-service capabilities, attendance and leave management, payroll processing, and reporting to improve HR efficiency and compliance. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import getdate, formatdate

class MonthlyEmployeeAllowance(Document):

	def on_submit(self):
		self.create_additional_salary_entries()

	def before_save(self):
		self.validate_date_overlap()

	def create_additional_salary_entries(self):
		for row in self.monthly_employee_allowance_details:
			if not row.allowance:
				continue

			existing = frappe.get_all(
				"Additional Salary",
				filters={
					"employee": row.employee,
					"salary_component": row.salary_component,
					"from_date": self.from_date,
					"to_date": self.to_date,
					"docstatus": ["!=", 2],
				},
				limit=1,
			)

			if existing:
				continue

			doc = frappe.new_doc("Additional Salary")
			doc.employee = row.employee
			doc.salary_component = row.salary_component
			doc.ref_doctype = "Monthly Employee Allowance"
			doc.ref_docname = self.name
			doc.amount = row.allowance
			doc.company = self.company
			doc.is_recurring = 1

			joining_date = frappe.get_value("Employee", row.employee, "date_of_joining")
			if joining_date and getdate(joining_date) > getdate(self.from_date):
				doc.from_date = joining_date
			else:
				doc.from_date = self.from_date

			doc.to_date = self.to_date

			doc.insert(ignore_permissions=True)
			doc.submit()


	@frappe.whitelist()
	def validate_date_overlap(self):
		if not self.from_date or not self.to_date:
			return
		self_from_date = getdate(self.from_date)
		self_to_date = getdate(self.to_date)

		existing = frappe.db.get_value(
			"Monthly Employee Allowance",
			{
				"name": ["!=", self.name],
				"from_date": ["<=", self_to_date],
				"to_date": [">=", self_from_date],
				"docstatus": 1,
			},
			["name", "from_date", "to_date"],
			as_dict=1,
		)

		if existing:
			frappe.throw(
				f"Date range overlaps with record {existing.name}"
				f" from {formatdate(existing.from_date)} to {formatdate(existing.to_date)}"
			)
