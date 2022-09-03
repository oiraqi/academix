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

from odoo import fields, models


class Program(models.Model):
    _name = 'ixcatalog.program'
    _description = 'Academic Program'
    _inherit = 'ix.school.owned'

    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code', required=True)
    description = fields.Html(string='Description', required=True)    
    level = fields.Selection(
        [('u', 'Undergraduate'), ('g', 'Graduate')], 'Level', default='u', required=True)
    curriculum_ids = fields.One2many(comodel_name='ixcatalog.curriculum', inverse_name='program_id', string='Curricula')
    ncurricula = fields.Integer(compute='_ncurricula', string='Number of Curricula')
    manager_ids = fields.Many2many('ix.faculty', 'ixcatalog_program_ix_faculty', 'program_id', 'manager_id', string='Managers')
    
    def _ncurricula(self):
        for rec in self:
            if rec.curriculum_ids:
                rec.ncurricula = len(rec.curriculum_ids)
            else:
                rec.ncurricula = 0