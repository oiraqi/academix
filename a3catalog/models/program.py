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

from odoo import api, fields, models


class Program(models.Model):
    _name = 'a3catalog.program'
    _description = 'Academic Program'
    _inherit = 'a3.school.owned'

    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code', required=True)
    description = fields.Html(string='Description', required=True)    
    level = fields.Selection(
        [('u', 'Undergraduate'), ('g', 'Graduate')], 'Level', default='u', required=True)
    component_ids = fields.Many2many('a3catalog.component', 'a3catalog_program_component_rel', 'program_id', 'component_id', string='Components')
    sch = fields.Integer(compute='_compute_sch_ncomponents', string='SCH')
    ncomponents = fields.Integer(compute='_compute_sch_ncomponents', string='Number of Components')
    
    @api.onchange('component_ids')
    @api.depends('component_ids')
    def _compute_sch_ncomponents(self):
        for rec in self:
            rec.sch = sum(component.sch for component in rec.component_ids if not component.parent_id)
            rec.ncomponents = sum(1 for component in rec.component_ids if not component.parent_id)
