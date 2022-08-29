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


class CourseIloSO(models.Model):
    _name = 'ixquality.course.ilo.so'
    _description = 'Course ILO & SO Mapping'
    _sql_constraints = [('ixquality_ilo_so_course_program_so_ukey', 'unique(course_program_id, ilo_id, so_id)', 'Mapping already exists')]

    ilo_id = fields.Many2one(comodel_name='ixcatalog.course.ilo', string='ILO', required=True)
    lms_course_ilo_id = fields.Many2one(comodel_name='ixlms.course.ilo', string='ILO')
    so_id = fields.Many2one(comodel_name='ixquality.student.outcome', string='SO', required=True)
    course_program_id = fields.Many2one(comodel_name='ixquality.course.program', string='Course/Program', required=True)    
    level = fields.Selection(string='Level', selection=[('introduce', 'Introduce'), ('reinforce', 'Reinforce'), ('emphasize', 'Emphasize')], default='introduce', required=True)
    course_id = fields.Many2one(comodel_name='ix.course', related='course_program_id.course_id', store=True)
    program_id = fields.Many2one(comodel_name='ixcatalog.program', related='course_program_id.program_id', store=True)
    
    