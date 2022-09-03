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

from odoo import fields, models, api


class Student(models.Model):
    _name = 'ix.student'
    _inherit = 'ix.student'

    curriculum_id = fields.Many2one(comodel_name='ixcatalog.curriculum', string='Curriculum', required=True, tracking=True)
    program_id = fields.Many2one(comodel_name='ixcatalog.program', string='Program', required=True, tracking=True)
    program_sch = fields.Integer(related='curriculum_id.sch', string='Total Credits')
    level = fields.Selection(related='program_id.level', store=True)

    @api.onchange('school_id')
    def _onchange_school_id(self):
        for rec in self:
            rec.program_id = False