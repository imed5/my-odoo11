# -*- coding: utf-8 -*-
from odoo import http

# class InvoiceStampDuty(http.Controller):
#     @http.route('/invoice_stamp_duty/invoice_stamp_duty/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/invoice_stamp_duty/invoice_stamp_duty/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('invoice_stamp_duty.listing', {
#             'root': '/invoice_stamp_duty/invoice_stamp_duty',
#             'objects': http.request.env['invoice_stamp_duty.invoice_stamp_duty'].search([]),
#         })

#     @http.route('/invoice_stamp_duty/invoice_stamp_duty/objects/<model("invoice_stamp_duty.invoice_stamp_duty"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('invoice_stamp_duty.object', {
#             'object': obj
#         })