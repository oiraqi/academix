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

class Lead(models.Model):
    _name = 'crm.lead'
    _inherit = ['crm.lead', 'ix.school.owned']

    name = fields.Char(string='')
    
    program_id = fields.Many2one(comodel_name='ixcatalog.program', string='Program')
    term_id = fields.Many2one(comodel_name='ix.term', string='Term')

    @api.onchange('school_id', 'program_id', 'term_id', 'partner_id')
    def _onchange_school_program_term_partner(self):
        for rec in self:
            name = ''
            if rec.school_id:
                name = rec.school_id.code
            if rec.program_id:
                if name:
                    name += '-' + rec.program_id.code
                else:
                    name = rec.program_id.code
            if rec.term_id:
                if name:
                    name += '-' + rec.term_id.code
                else:
                    name = rec.term_id.code
            if rec.partner_id:
                if name:
                    name += '-' + rec.partner_id.name
                else:
                    name = rec.partner_id.name
            if name:
                rec.name = name

    