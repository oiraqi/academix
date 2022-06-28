from tokenize import group
from odoo import models, fields, api


class AssessmentSubmission(models.Model):
	_name = 'a3lms.assessment.submission'
	_description = 'AssessmentSubmission'
	_inherit = 'mail.thread'

	@api.model
	def create(self, vals):
		submission = super(AssessmentSubmission, self).create(vals)
		assessment_line_id = self.env['a3lms.assessment.line'].search([('student_id.user_id', '=', submission.create_uid.id)])
		assessment_lines = [assessment_line_id.id]
		if submission.assessment_id.teamwork:
			submitter = assessment_line_id.student_id
			teams = self.env['a3lms.team'].search([('teamset_id', '=', submission.assessment_id.teamset_id.id),
				('member_ids', 'in', submitter.id)])
			if teams:
				for member in teams[0]:
					assessment_line_id = self.env['a3lms.assessment.line'].search([('student_id', '=', member.id)])
					if assessment_line_id.id not in assessment_lines:
						assessment_lines.append(assessment_line_id.id)
		submission.assessment_line_ids = assessment_lines
		return submission

	assessment_id = fields.Many2one(comodel_name='a3lms.assessment', string='Assessment', required=True)
	assessment_line_ids = fields.Many2many('a3lms.assessment.line', 'a3lms_assessment_line_submission', 'submission_id', 'assessment_line_id', 'Assessment Lines')
	
	is_file_req = fields.Boolean(related='assessment_id.is_file_req')
	is_url_req = fields.Boolean(related='assessment_id.is_url_req')
	is_text_req = fields.Boolean(related='assessment_id.is_text_req')	
	team_id = fields.Many2one(comodel_name='a3lms.team', string='Team')	
	file = fields.Binary(string='File', tracking=True)
	url = fields.Char(string='URL', tracking=True)
	text = fields.Html(string='Text', tracking=True)
	
	grade = fields.Float(string='Grade', group='a3.group_faculty')
	#readonly grade
	rgrade = fields.Float(string='Grade', compute='_rgrade')
	
	def _rgrade(self):
		for rec in self:
			rec.rgrade = rec.sudo().grade