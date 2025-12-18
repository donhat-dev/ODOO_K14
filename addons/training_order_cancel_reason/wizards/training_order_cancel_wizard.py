# -*- coding: utf-8 -*-

import logging
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class TrainingOrderCancelWizard(models.TransientModel):
    _name = 'training.order.cancel.wizard'
    _description = _('TrainingOrderCancelWizard')

    training_order_id = fields.Many2one('training.order', string="Order")
    cancel_reason = fields.Text(string="Cancel Reason")

    cancel_date = fields.Datetime(
        string="Cancel Date",
        default=lambda self: fields.Datetime.now()  
    )

    type = fields.Selection(
        selection=[
            ('1', 'Type 1'),
            ('2', 'Type 2'),
        ],
        default='1',
    )
    # @api.model
    # def default_get(self, fields_list):
    #     res = super().default_get(fields_list)

    #     if self.env.context.get('active_id'):
    #         res['training_order_id'] = self.env.context.get('active_id')
        
    #     return res

    def action_confirm(self):
        self.ensure_one()
        
        if self.cancel_reason:
            self.training_order_id.write(
                {
                    'cancel_reason': self.cancel_reason,
                    'state': 'canceled'
                }
            )

        if self.type == '2':
            return {
                'type': 'ir.actions.act_window_close'
            }

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'training.order.cancel.wizard',
            'view_mode': 'form',
            'context': {
                'default_training_order_id': self.training_order_id.id,
                'default_type': '2'
            },
            'target': 'new',
        }
