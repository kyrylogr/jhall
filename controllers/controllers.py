# -*- coding: utf-8 -*-
from odoo import http

# class Jhall(http.Controller):
#     @http.route('/jhall/jhall/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/jhall/jhall/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('jhall.listing', {
#             'root': '/jhall/jhall',
#             'objects': http.request.env['jhall.jhall'].search([]),
#         })

#     @http.route('/jhall/jhall/objects/<model("jhall.jhall"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('jhall.object', {
#             'object': obj
#         })