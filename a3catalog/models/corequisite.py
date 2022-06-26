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


class Corequisite(models.Model):
    _name = 'a3catalog.corequisite'
    _description = 'Course Corequisite'
    _sql_constraints = [('course_corequisite_ukey', 'unique(course_id, corequisite_id)', 'The same corequisite has been added several times!')]

    name = fields.Char(string='corequisite_id.name')
    course_id = fields.Many2one('a3.course', string='Course', required=True)
    corequisite_id = fields.Many2one('a3.course', string='Corequisite', required=True)
    sequence = fields.Integer(default='1', required=True)
