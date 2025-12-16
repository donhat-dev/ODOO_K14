
from odoo import models, fields, api

from odoo.exceptions import ValidationError

from odoo.tools import float_round

class TrainingOrder(models.Model):
    _name = 'training.order'
    _rec_name = 'order_number'

    order_number = fields.Char(string="Order Number", readonly=True)
    customer_name = fields.Char(string="Customer Name", default='Nhat', readonly=True)

    customer_id = fields.Many2one(comodel_name='res.partner', string="Customer", ondelete="restrict")
    lead_id = fields.Many2one('crm.lead', string="Related Lead")
    
    active = fields.Boolean(string="Active", default=True)

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

    order_line_ids = fields.One2many(
        'training.order.line',
        'order_id',
        string="Order Lines"
    )

    total_amount = fields.Float(
        string="Total Amount",
        compute='_compute_total_amount',
        store="True"
    )

    user_id = fields.Many2one(
        'res.users',
        string="Salesperson",
        default=lambda self: self.env.user
    )

    @api.depends('order_line_ids.total_price')
    def _compute_total_amount(self):
        for record in self:
            # total = 0
            # for line in record.order_line_ids:
            #     total += line.total_price

            total_prices = record.order_line_ids.mapped('total_price')
            total = sum(total_prices)
            record.total_amount = total

    @api.onchange('order_line_ids')
    def _onchange_order_line_quantity(self):
        if self.order_line_ids:
            for line in self.order_line_ids:
                if not self.env.context.get('check_quantity_limit', False):
                    continue
                if line.quantity > 1:
                    raise ValidationError("Quantity cannot be greater than 1.")
    
    @api.constrains('customer_id')
    def _check_customer_id_unique(self):
        for record in self:
            exist_order_id = self.env['training.order'].search([('customer_id', '=', record.customer_id.id),
                                                                ('id', '!=', record.id)
                                                                ], limit=1) 
            if exist_order_id:
                raise ValidationError("Order exist !")

    @api.model
    def create(self, vals):
        sequence = self.env['ir.sequence'].search([(('code', '=', 'training.order'))], limit=1)
        if not sequence:
            sequence = self.env['ir.sequence'].create({
                'name': 'Training Order Sequence',
                'code': 'training.order',
                'prefix': 'TO',
                'padding': 5
            })
        vals['order_number'] = sequence.next_by_id()

        res = super().create(vals)
        return res
    

    def button_approve_1(self):
        if not self.env.user.has_group('training_center.group_training_manager'):
            raise ValidationError("You do not have permission to approve at Level 1.")

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
    

class TrainingOrderLine(models.Model):
    _name = 'training.order.line'

    order_id = fields.Many2one(
        'training.order',
        string="Order",
        ondelete="cascade"
    )

    course_id = fields.Many2one(
        'training.course',
        string="Course",
        ondelete="restrict"
    )

    name = fields.Char(string="Description")
    description = fields.Text(string="Details")

    quantity = fields.Float(string="Quantity", default=1,
                              digits=(16, 2)
                              )
    unit_price = fields.Float(string="Unit Price", default=0.0, digits=(16, 2)
                              )
    total_price = fields.Float(string="Total Price",
                               compute="_compute_total_price", store=True, readonly=False,
                               inverse="_compute_unit_price"
                               )
                               
    
    @api.depends('quantity', 'unit_price')
    def _compute_total_price(self):
        for record in self:
            record.total_price = float_round(record.quantity * record.unit_price, precision_digits=2, rounding_method='HALF-UP')
    
    def _compute_unit_price(self):
        for record in self:
            if record.quantity != 0:
                record.unit_price = record.total_price / record.quantity
            else:
                record.unit_price = 0.0

    def action_open_options_wizard(self):
        self.ensure_one()
        return {
            'name': 'Order Line Options',
            'type': 'ir.actions.act_window',
            'res_model': 'training.order.options.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_order_line_id': self.id,
            }
        }

class TrainingOrderOptionsWizard(models.TransientModel):
    _name = 'training.order.options.wizard'
    _description = 'Training Order Options Wizard'

    order_line_id = fields.Many2one(
        'training.order.line',
        string="Order Line",
        required=True
    )

    order_line_id_description = fields.Text(
        string="Order Line Description",
        related='order_line_id.description'
    )