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


class Discipline(models.Model):
    _name = 'a3.discipline'
    _order = 'code'
    _sql_constraints = [('code_ukey', 'unique(code)', 'Code already exists')]

    code = fields.Char('Code', required=True)
    name = fields.Char('Name', required=True)
    school_id = fields.Many2one('a3.school', string='School', required=True)
    faculty_ids = fields.Many2many('a3.faculty', 'a3_faculty_discipline_rel', 'discipline_id', 'faculty_id', 'Faculty')
    undergrad_manager_ids = fields.Many2many('a3.faculty', 'a3_discipline_undergrad_manager_rel', 'discipline_id', 'manager_id', 'Undergraduate Course Managers')
    grad_manager_ids = fields.Many2many('a3.faculty', 'a3_discipline_grad_manager_rel', 'discipline_id', 'manager_id', 'Graduate Course Managers')
    
    
