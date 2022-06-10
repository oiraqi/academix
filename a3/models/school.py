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

from odoo import models, fields


class School(models.Model):
    _name = 'a3.school'
    _order = 'code'
    _sql_constraints = [('code_ukey', 'unique(code)', 'School already exists')]

    name = fields.Char('Name', required=True)
    code = fields.Char('Code', required=True)
    mission = fields.Html(string='Mission')
    dean_id = fields.Many2one('a3.staff', string='Dean')
    discipline_ids = fields.One2many('a3.discipline', 'school_id', string='Disciplines')
    building_ids = fields.One2many(comodel_name='a3.building', inverse_name='school_id', string='Buildings')
    
    color = fields.Integer('Color')
