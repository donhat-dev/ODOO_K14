
from odoo import models, fields, api

class TrainingOrder(models.Model):
    _name = 'training.order'

    order_number = fields.Char(string="Order Number", required=True)
    customer_name = fields.Char(string="Customer Name", default='Nhat', readonly=True)
    order_date = fields.Date(string="Order Date")
    state = fields.Selection(
        [('draft', 'Draft'),
         ('waiting_approval_1', 'Waiting for Approval Level 1'),
         ('approved_1', 'Approved Level 1'),
         ('approved_2', 'Approved Level 2'),
         ('done', 'Done')],
        string="Status",
        default='draft'
    )

    approve_1_user_id = fields.Many2one(
        'res.users',
        string="Approved By (Level 1)",
        groups="base.group_system"
    )

    approve_2_user_id = fields.Many2one(
        'res.users',
        string="Approved By (Level 2)",
        groups="base.group_system"
    )

    is_approved_1 = fields.Boolean(
        string="Is Approved Level 1",
        compute='_compute_is_approved_1'
    )

    is_approved_2 = fields.Boolean(
        string="Is Approved Level 2",
        compute='_compute_is_approved_2'
    )

    @api.model
    def create(self, vals):
        res = super().create(vals)
        return res
    

    def button_approve_1(self):
        for record in self:
            record.state = 'approved_1'

    def button_approve_2(self):
        for record in self:
            record.state = 'approved_2'

    def _compute_is_approved_1(self):
        for record in self:
            record.is_approved_1 = self.env.user == record.approve_1_user_id

    def _compute_is_approved_2(self):
        for record in self:
            record.is_approved_2 = self.env.user == record.approve_2_user_id