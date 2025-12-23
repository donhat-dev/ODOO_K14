from odoo import http
from odoo.http import request
from odoo.http import Response
import json

import logging

_logger = logging.getLogger(__name__)

class TrainingCenterController(http.Controller):

    @http.route(
        '/training_order/<int:order_id>/details',
        type='http',
        auth='public',
        methods=['GET'],
        cors='*',
        csrf=False,
    )
    def details_training_order(self, order_id, **kwargs):
        order = request.env['training.order'].sudo().search([('id', '=', order_id)], limit=1)

        data = order.read(['id', 'display_name'])

        return request.render(
            'training_center.training_order_template',
            {
                'orders_data': data,
            }
        )

    @http.route(
        '/training_order/<int:order_id>',
        type='http',
        auth='public',
        methods=['GET'],
        cors='*',
        csrf=False,
    )
    def training_order(self, order_id, **kwargs):
        # params = request.httprequest.params
        fields = kwargs.get('fields', 'id,display_name')

        order = request.env['training.order'].sudo().search([('id', '=', order_id)], limit=1)

        data = order.read(fields.split(','))

        return request.make_json_response(
            data=data,
            status=200
        )
    
    @http.route(
        '/training_order/<int:order_id>',
        type='http',
        auth='public',
        methods=['PUT'],
        cors='*',
        csrf=False,
    )
    def update_training_order(self, order_id, **kwargs):

        order = request.env['training.order'].sudo().search([('id', '=', order_id)], limit=1)
        update_data = {}
        fields_list = order.fields_get().keys()
        for key, value in kwargs.items():
            if key not in fields_list:
                continue
            update_data[key] = value
        
        order.sudo().write(update_data)

        return request.make_json_response(
            data="Success",
            status=200
        )
    

    @http.route(
        '/training_order',
        type='http',
        auth='public',
        methods=['POST'],
        cors='*',
        csrf=False,
    )
    def create_training_order(self):
        try:
            data = request.httprequest.data

            if not data:
                return request.make_json_response(
                    data="No data provided",
                    status=400
                )

            body = json.loads(data)

            training_order_obj = request.env['training.order'].sudo()

            fields_list = training_order_obj.fields_get().keys()
            create_data = {}
            for key, value in body.items():
                if key in fields_list:
                    create_data[key] = value
            
            new_order = training_order_obj.sudo().create(create_data)

            _logger.info("Created new training order with ID: %s", new_order.id)
            return request.make_json_response(
                data={"id": new_order.id},
                status=200
            )
        except Exception as e:
            _logger.error("Error creating training order: %s", str(e))
            return request.make_json_response(
                data=str(e),
                status=500
            )
