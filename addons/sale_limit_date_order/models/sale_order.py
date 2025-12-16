from odoo import models, fields, api

from odoo.exceptions import ValidationError

class SaleOrder(models.Model):
    _inherit = "sale.order"

    partner_id = fields.Many2one(
        string="Student",
        readonly=False,
    )

    partner_id_code = fields.Char(
        string="Student Code",
    )

    def action_confirm(self):
        result = super().action_confirm()

        if result:
            for record in self:
                if not record.source_id:
                    raise ValidationError("Please Input Source !")
            
        return result
    
    @api.model_create_multi
    def create(self, vals_list):

        # Thêm vào trước gọi super() khi muốn thêm dữ liệu trước khi tạo bản ghi
        # for vals in vals_list:
        #     if 'payment_term_id' in vals and vals['payment_term_id']:
        #         raise ValidationError("You cannot create Sale Order with Payment Term.")
        
        # tag_ids = self.env['crm.tag'].search(
        #     [
        #         ('name','in',['VIP', 'INTERNAL']),
        #     ],
        #     offset=0,
        #     limit=1,
        #     order='create_date desc'
        # )

        # tag_ids = self.env['crm.tag'].browse(123455)
        # tag_names = tag_ids.name

        # for vals in vals_list:
        #     vals['tag_ids'] = tag_ids.ids

        records = super().create(vals_list)

        for record in records:
            if record.payment_term_id:
                raise ValidationError("You cannot create Sale Order with Payment Term.")

        return records
    
    def write(self, vals):
        for record in self:
            if ('payment_term_id' in vals and vals['payment_term_id']):
                raise ValidationError("You cannot modify Sale Order with Payment Term.")
        
        res = super().write(vals)

        return res
    
    def unlink(self):
        for record in self:
            if record.payment_term_id:
                raise ValidationError("You cannot delete Sale Order with Payment Term.")
        return super().unlink()
