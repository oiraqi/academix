from odoo import models, fields


class AssessmentTimeline(models.Model):
	_name = 'a3lms.assessment.timeline'
	_description = 'Assessment Timeline'

	assessment_id = fields.Many2one(comodel_name='a3lms.assessment', string='Assessment')
	targetted_student_ids = fields.Many2many(comodel_name='a3.student', string='Students')
	targetted_team_ids = fields.Many2many(comodel_name='a3lms.team', string='Teams')
	due_time = fields.Datetime(string='Due')
	from_time = fields.Datetime(string='Open from')
	to_time = fields.Datetime(string='Until')
	student_ids = fields.One2many(comodel_name='a3.student', related='assessment_id.course_id.student_ids')
	team_ids = fields.One2many(comodel_name='a3lms.team', related='assessment_id.teamset_id.team_ids')
	
		