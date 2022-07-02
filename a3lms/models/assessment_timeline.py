from odoo import models, fields


class AssessmentTimeline(models.Model):
	_name = 'ixlms.assessment.timeline'
	_description = 'Assessment Timeline'

	assessment_id = fields.Many2one(comodel_name='ixlms.assessment', string='Assessment')
	targetted_student_ids = fields.Many2many(comodel_name='ix.student', string='Students')
	targetted_team_ids = fields.Many2many(comodel_name='ixlms.team', string='Teams')
	due_time = fields.Datetime(string='Due')
	from_time = fields.Datetime(string='Open from')
	to_time = fields.Datetime(string='Until')
	student_ids = fields.One2many(comodel_name='ix.student', related='assessment_id.course_id.student_ids')
	team_ids = fields.One2many(comodel_name='ixlms.team', related='assessment_id.teamset_id.team_ids')
	
		