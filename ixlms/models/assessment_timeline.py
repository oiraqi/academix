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


class AssessmentTimeline(models.Model):
	_name = 'ixlms.assessment.timeline'
	_description = 'Assessment Timeline'

	assessment_id = fields.Many2one(comodel_name='ixlms.assessment', string='Assessment')
	lms_course_id = fields.Many2one(comodel_name='ixlms.course', string='LMS Course')
	section_id = fields.Many2one(comodel_name='ixroster.section', string='Section')
	targetted_student_ids = fields.Many2many(comodel_name='ix.student', string='Students')
	targetted_team_ids = fields.Many2many(comodel_name='ixlms.team', string='Teams')
	due_time = fields.Datetime(string='Due')
	from_time = fields.Datetime(string='Open from')
	to_time = fields.Datetime(string='Until')
	student_ids = fields.One2many(comodel_name='ix.student', related='lms_course_id.student_ids')
	team_ids = fields.One2many(comodel_name='ixlms.team', related='assessment_id.teamset_id.team_ids')
	
		