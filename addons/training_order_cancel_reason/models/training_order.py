# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class TrainingOrder(models.Model):
    _inherit = 'training.order'

    state = fields.Selection(
        selection_add=[('canceled', 'Canceled')], 
        ondelete={"canceled": "set default"}
    )
    cancel_reason = fields.Text(string="Cancel Reason")

    order_line_count = fields.Integer(
        string="Order Line Count",
        compute="_compute_order_line_count"
    )

    @api.depends('order_line_ids')
    def _compute_order_line_count(self):
        for order in self:
            order.order_line_count = len(order.order_line_ids)
    
    def action_view_order_lines(self):
        self.ensure_one()

        # action = self.env.ref('training_center.action_training_order_line').read()[0]
        # action['domain'] = [('id', 'in', self.order_line_ids.ids)]
        # action['context'] = {
        #     'default_order_id': self.id,
        #     'default_unit_price': 1000
        # }
        # action['name'] = "%s Order Lines (%s)" % (self.display_name, len(self.order_line_ids))
        # return action

        return {
            'type': 'ir.actions.act_window',
            'name': "%s Order Lines (%s)" % (self.display_name, self.order_line_count),
            'res_model': 'training.order.line',
            'view_mode': 'list,form',
            'domain': [('id', 'in', self.order_line_ids.ids)],
            'context': {
                'default_order_id': self.id,
                'default_unit_price': 1000
            }
        }