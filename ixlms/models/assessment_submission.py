from tokenize import group
from odoo import models, fields, api


class AssessmentSubmission(models.Model):
	_name = 'ixlms.assessment.submission'
	_description = 'AssessmentSubmission'
	_inherit = 'mail.thread'

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
		submission.assessment_line_ids = [(0, 6, assessment_lines)]
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