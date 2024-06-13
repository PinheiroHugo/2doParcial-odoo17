# -*- coding: utf-8 -*-
# from odoo import http


# class GestionEscolar(http.Controller):
#     @http.route('/gestion_escolar/gestion_escolar', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/gestion_escolar/gestion_escolar/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('gestion_escolar.listing', {
#             'root': '/gestion_escolar/gestion_escolar',
#             'objects': http.request.env['gestion_escolar.gestion_escolar'].search([]),
#         })

#     @http.route('/gestion_escolar/gestion_escolar/objects/<model("gestion_escolar.gestion_escolar"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('gestion_escolar.object', {
#             'object': obj
#         })

