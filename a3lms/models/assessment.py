from odoo import models, fields


class Assessment(models.Model):
	_name = 'a3lms.assessment'
	_description = 'LMS Assessment'
	_inherit = 'a3.expandable'
	_order = 'due_time,module_id'

	name = fields.Char('Name', required=True)
	description = fields.Html(string='Description')
	submission_type = fields.Selection(string='Submission Type', selection=[('nosub', 'No Submission'), ('online', 'Online'), ('paper', 'Paper')], default='online')
	course_id = fields.Many2one(comodel_name='a3lms.course', string='LMS Course', required=True)
	section_id = fields.Many2one(comodel_name='a3roster.section', string='course_id.section_id', store=True)
	module_id = fields.Many2one(comodel_name='a3lms.module', string='Module', required=True)
	technique_id = fields.Many2one(comodel_name='a3lms.weighted.technique', string='Technique', required=True)
	points = fields.Integer(string='Points', default=0)
	percentage = fields.Float(string='%', default=0.0)
	technique_ids = fields.One2many(comodel_name='a3lms.weighted.technique', related='course_id.technique_ids')
	module_ids = fields.One2many(comodel_name='a3lms.module', related='course_id.module_ids')
	due_time = fields.Datetime(string='Due')
	from_time = fields.Datetime(string='Open from')
	to_time = fields.Datetime(string='Until')
	bonus = fields.Float(string='Class-wide Bonus (%)', default=0.0)
	penalty_per_late_day = fields.Float(string='Penalty per Late Day (%)', default=0.0)

	assessment_line_ids = fields.One2many(comodel_name='a3lms.assessment.line', inverse_name='assessment_id', string='Assessment Lines')
	submissions = fields.Char(string='Submissions', compute='_stats')
	
	max_grade = fields.Float(string='Max Grade', compute='_stats')
	min_grade = fields.Float(string='Min Grade', compute='_stats')
	avg_grade = fields.Float(string='Avg. Grade', compute='_stats')
	stdev = fields.Float(string='σ', compute='_stats')

	def _stats(self):
		for rec in self:
			rec.max_grade = 100
			rec.min_grade = 0
			rec.avg_grade = 50
			rec.stdev = 10
			rec.submissions = '12/15'

	def get_assessment_lines(self):
		self.ensure_one()
		domain = [('assessment_id', '=', self.id)]
		self._resolve_action('a3lms.action_assessment_line', domain)


	