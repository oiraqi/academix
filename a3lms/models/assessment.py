from odoo import models, fields


class Assessment(models.Model):
	_name = 'a3lms.assessment'
	_description = 'LMS Assessment'
	_order = 'due_time,module_id'

	name = fields.Char('Name', required=True)
	description = fields.Html(string='Description')
	submission_type = fields.Selection(string='Submission Type', selection=[('nosub', 'No Submission'), ('online', 'Online'), ('paper', 'Paper')], default='online')
	course_id = fields.Many2one(comodel_name='a3lms.course', string='LMS Course', required=True)
	module_id = fields.Many2one(comodel_name='a3lms.module', string='Module', required=True)
	technique_id = fields.Many2one(comodel_name='a3lms.assessment.technique', string='Technique', required=True)
	points = fields.Integer(string='Points', default=0)
	percentage = fields.Float(string='%', default=0.0)
	assessment_technique_ids = fields.One2many(comodel_name='a3lms.assessment.technique', related='course_id.assessment_technique_ids')
	module_ids = fields.One2many(comodel_name='a3lms.module', related='course_id.module_ids')
	due_time = fields.Datetime(string='Due')
	from_time = fields.Datetime(string='Available from')
	to_time = fields.Datetime(string='Until')
	bonus = fields.Float(string='Class-wide Bonus', default=0.0)
	