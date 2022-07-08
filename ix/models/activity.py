# -*- coding: utf-8 -*-
###############################################################################
#
#    Al Akhawayn University in Ifrane -- AUI
#    Copyright (C) 2022-TODAY AUI(<http://www.aui.ma>).
#
#    Author: Omar Iraqi Houssaini | https://github.com/oiraqi
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

from odoo import models, fields, api
from datetime import date


class Activity(models.AbstractModel):
    _name = 'ix.activity'
    _order = 'year desc,sequence desc'

    term_id = fields.Many2one('ix.term', string='Term', required=True)
    year = fields.Integer(related='term_id.year', store=True)
    session_id = fields.Many2one(comodel_name='ix.session', related='term_id.session_id', store=True)
    sequence = fields.Integer(related='term_id.session_id.sequence', store=True)    
    prefix = fields.Char(compute='_fix')
    suffix = fields.Char(compute='_fix')    

    @api.onchange('term_id')
    def _fix(self):
        for rec in self:
            if rec.term_id:
                rec.prefix = rec.term_id.code + '-'
                rec.suffix = '-' + rec.term_id.code
            else:
                rec.prefix = ''
                rec.suffix = ''

    document_ids = fields.One2many(
        'ir.attachment', string='Documents', compute='_document_ids')
    document_count = fields.Integer(compute='_document_ids')

    def _document_ids(self):
        for rec in self:
            document_ids = self.sudo().env['ir.attachment'].search(
                [('res_model', '=', self._name), ('res_id', '=', rec.id)])
            if document_ids:
                rec.document_ids = document_ids
                rec.document_count = len(document_ids)
            else:
                rec.document_ids = False
                rec.document_count = 0
