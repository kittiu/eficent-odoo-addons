# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.addons.analytic_resource_plan_stock.tests import (
    test_analytic_resource_plan_stock,
)


class TestAnalyticResourcePlanStockPickingPurchaseRequest(
    test_analytic_resource_plan_stock.TestAnalyticResourcePlanStock
):

    @classmethod
    def setUpClass(cls):
        super(
            TestAnalyticResourcePlanStockPickingPurchaseRequest, cls
        ).setUpClass()
        cls.analytic_account_obj = cls.env["account.analytic.account"]
        cls.resource_plan_line_obj = cls.env["analytic.resource.plan.line"]
        cls.product_id = cls.env.ref("product.product_product_27")
        cls.partner = cls.env.ref("base.res_partner_1")
        cls.analytic_plan_version = cls.env.ref(
            "analytic_plan.analytic_plan_version_P00"
        )
        cls.location_id = cls.env.ref("stock.stock_location_stock")
        cls.product_id.write({"expense_analytic_plan_journal_id": 1})
        cls.analytic_plan_journal_obj = cls.env[
            "account.analytic.plan.journal"
        ]
        cls.purchase_request_obj = cls.env["purchase.request"]
        cls.purchase_request_line_obj = cls.env["purchase.request.line"]
        cls.partner = cls.env.ref("base.res_partner_1")
        cls.analytic_plan_version = cls.env.ref(
            "analytic_plan.analytic_plan_version_P00"
        )
        cls.product_id = cls.env.ref("product.product_product_27")
        cls.location_id = cls.env.ref("stock.stock_location_stock")
        cls.analytic_plan_journal = cls.analytic_plan_journal_obj.create(
            {"name": "Sale", "type": "sale", "code": "SAL", "active": True}
        )
        cls.product_id.write(
            {
                "expense_analytic_plan_journal_id":
                    cls.analytic_plan_journal.id
            }
        )

    def test_analytic_resource_plan_stock_picking(self):
        self.resource_plan_line.unit_amount = 2.0
        upd_qty = self.env["stock.change.product.qty"].create(
            {
                "product_id": self.resource_plan_line.product_id.id,
                "product_tmpl_id":
                    self.resource_plan_line.product_id.product_tmpl_id.id,
                "new_quantity": 1.0,
                "location_id": self.env.ref("stock.stock_location_stock").id,
            }
        )
        upd_qty.change_product_qty()
        self.resource_plan_line.action_button_confirm()
        purchase_request_line = self.resource_plan_line.purchase_request_lines[
            0
        ]
        purchase_request = purchase_request_line.request_id
        purchase_request.button_to_approve()
        purchase_request.button_approved()
        self.assertEqual(
            self.resource_plan_line.request_state,
            "approved",
            "should approved request",
        )
        self.assertEqual(
            self.resource_plan_line.requested_qty, 1.0, "bad qty requested"
        )
