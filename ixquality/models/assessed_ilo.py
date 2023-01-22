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


class AssessedIlo(models.Model):
	_name = 'ixquality.assessed.ilo'
	_description = 'Assessed ILO'
	_sql_constraints = [('ilo_assessment_line_ukey', 'unique(ilo_id, assessment_line_id)', 'Duplicate ILO assessment!')]

	lms_course_ilo_id = fields.Many2one(comodel_name='ixlms.course.ilo', string='LMS Course ILO', required=True)
	assessment_line_id = fields.Many2one(comodel_name='ixlms.assessment.line', string='LMS Assessment Line', required=True)
	assessment_id = fields.Many2one(comodel_name='ixlms.assessment', related='assessment_line_id.assessment_id')
	course_id = fields.Many2one(comodel_name='ixlms.course', related='assessment_id.lms_course_id', store=True)
	lms_course_id = fields.Many2one(comodel_name='ixlms.course', related='assessment_id.lms_course_id', store=True)
	program_id = fields.Many2one(comodel_name='ixcatalog.program', related='assessment_line_id.student_id.program_id', store=True)
	student_id = fields.Many2one(comodel_name='ix.student', related='assessment_line_id.student_id')
	acquisition_level_id = fields.Many2one(comodel_name='ixquality.acquisition.level', string='Acquisition Level')
	acquisition_level = fields.Selection(string='Acquisition Level', selection=[
		('0', 'Not acquired'), ('1', '60%'), ('2', '70%'),  ('3', '80%'), ('4', '90%'), ('5', 'Fully Acquired')], default='0')
	ilo_idx_description = fields.Char(related='lms_course_ilo_id.idx_description')
		