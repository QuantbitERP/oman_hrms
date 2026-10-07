// Copyright (c) 2026, The application provides centralized HR management with configurable workflows, employee self-service capabilities, attendance and leave management, payroll processing, and reporting to improve HR efficiency and compliance. and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Monthly Employee Allowance", {
// 	refresh(frm) {

// 	},
// });
frappe.ui.form.on("Monthly Employee Allowance", {
    refresh(frm) {
        frm.fields_dict.monthly_employee_allowance_details.grid
            .get_field("salary_component")
            .get_query = function(doc, cdt, cdn) {
                return {
                    filters: {
                        custom_monthly_allowance: 1
                    }
                };
            };
    }
});
frappe.ui.form.on("Monthly Employee Allowance Details", {
    allowance_units(frm, cdt, cdn) {
        calculate_allowance_amount(frm, cdt, cdn);
    },

    allowance_rate(frm, cdt, cdn) {
        calculate_allowance_amount(frm, cdt, cdn);
    }
});

function calculate_allowance_amount(frm, cdt, cdn) {
    let row = frappe.get_doc(cdt, cdn);
    
    row_amount = flt(row.allowance_units) * flt(row.allowance_rate);
    frappe.model.set_value(cdt, cdn, "allowance", row_amount);
    frm.refresh_field("monthly_employee_allowance_details");
}