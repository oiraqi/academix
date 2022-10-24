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


class AssessmentSubmission(models.Model):
	_name = 'ixlms.assessment.submission'
	_description = 'Assessment Submission'
	_inherit = ['mail.thread', 'ix.expandable']

	@api.model
	def create(self, vals):
		submission = super(AssessmentSubmission, self).create(vals)
		assessment_line_id = self.env['ixlms.assessment.line'].search([('assessment_id', '=', submission.assessment_id.id), ('student_id.user_id', '=', submission.create_uid.id)])
		assessment_lines = [assessment_line_id.id]
		if submission.assessment_id.teamwork:
			submitter = assessment_line_id.student_id
			teams = self.env['ixlms.team'].search([('teamset_id', '=', submission.assessment_id.teamset_id.id),
				('member_ids', 'in', submitter.id)])
			if teams:
				self.team_id = teams[0]
				for member in teams[0]:
					assessment_line_id = self.env['ixlms.assessment.line'].search([('student_id', '=', member.id)])
					if assessment_line_id.id not in assessment_lines:
						assessment_lines.append(assessment_line_id.id)
		submission.assessment_line_ids = [(6, 0, assessment_lines)]
		return submission

	assessment_id = fields.Many2one(comodel_name='ixlms.assessment', string='Assessment', required=True)
	assessment_line_ids = fields.Many2many('ixlms.assessment.line', 'ixlms_assessment_line_submission', 'submission_id', 'assessment_line_id', 'Assessment Lines')
	
	is_file_req = fields.Boolean(related='assessment_id.is_file_req')
	is_url_req = fields.Boolean(related='assessment_id.is_url_req')
	is_text_req = fields.Boolean(related='assessment_id.is_text_req')	
	team_id = fields.Many2one(comodel_name='ixlms.team', string='Team')
	file = fields.Binary(string='File', tracking=True)
	url = fields.Char(string='URL', tracking=True)
	text = fields.Html(string='Text', tracking=True)
	grade_scale = fields.Integer(string='Graded over', related='assessment_id.grade_scale')
	
	grade = fields.Float(string='Grade', groups='ix.group_faculty')
	#readonly grade
	rgrade = fields.Float(string='Grade', compute='_rgrade')
	
	def _rgrade(self):
		for rec in self:
			rec.rgrade = rec.sudo().grade

	def get_submission(self):
		self.ensure_one()
		domain = [('id', '=', self.id)]
		return self._expand_to('ixlms.action_assessment_submission', domain)