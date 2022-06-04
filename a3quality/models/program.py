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


class Program(models.Model):
    _inherit = 'a3catalog.program'

    so_ids = fields.One2many(comodel_name='a3quality.student.outcome', inverse_name='program_id', string='Student Outcomes')
    accreditation_ids = fields.Many2many('a3quality.accreditation', 'a3quality_program_accreditation_rel', 'program_id', 'accreditation_id', 'Accreditations')
    course_program_ids = fields.One2many(comodel_name='a3quality.course.program', inverse_name='program_id', string='Assessed Courses')    
    