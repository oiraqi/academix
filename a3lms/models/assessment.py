from odoo import models, fields, api


class Assessment(models.Model):
	_name = 'a3lms.assessment'
	_description = 'LMS Assessment'
	_inherit = 'a3.expandable'
	_order = 'due_time,module_id'

	name = fields.Char('Name', required=True)
	description = fields.Html(string='Description')
	
	course_id = fields.Many2one(comodel_name='a3lms.course', string='LMS Course', required=True)
	section_id = fields.Many2one(comodel_name='a3roster.section', string='course_id.section_id', store=True)
	module_id = fields.Many2one(comodel_name='a3lms.module', string='Module', required=True)
	technique_id = fields.Many2one(comodel_name='a3lms.weighted.technique', string='Technique', required=True)
	points = fields.Integer(string='Points', default=0)
	percentage = fields.Float(string='%', default=0.0)	
	technique_ids = fields.One2many(comodel_name='a3lms.weighted.technique', related='course_id.technique_ids')
	module_ids = fields.One2many(comodel_name='a3lms.module', related='course_id.module_ids')

	submission_type = fields.Selection(string='Submission Type', selection=[('online', 'Online'), ('paper', 'Paper'), ('nosub', 'No Submission / Self-assessment')], default='online')
	is_file_req = fields.Boolean(string='File Required', default=False)
	is_url_req = fields.Boolean(string='URL Required', default=False)
	is_text_req = fields.Boolean(string='Inline Text Required', default=False)
	teamwork = fields.Boolean(string='Teamwork', default=False)	
	teamset_id = fields.Many2one(comodel_name='a3lms.teamset', string='Team Set')

	timeline = fields.Selection(string='Timeline', selection=[('common', 'Common'), ('dedicated', 'Dedicated')], default='common', required=True)
	

	due_time = fields.Datetime(string='Due')
	from_time = fields.Datetime(string='Open from')
	to_time = fields.Datetime(string='Until')

	timeline_ids = fields.One2many(comodel_name='a3lms.assessment.timeline', inverse_name='assessment_id', string='Dedicated Timelines')
	
	graded = fields.Boolean(string='Graded', default=True)
	
	@api.onchange('graded')
	def _graded(self):
		for rec in self:
			if not rec.graded:
				rec.points = 0
				rec.percentage = 0.0
	
	bonus = fields.Float(string='Class-wide Bonus (%)', default=0.0)

	@api.model
	def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
		if 'bonus' in fields:
			fields.remove('bonus')
		return super(Assessment, self).read_group(domain, fields, groupby, offset, limit, orderby, lazy)

	penalty_per_late_day = fields.Float(string='Penalty per Late Day (%)', default=0.0)	

	assessment_line_ids = fields.One2many(comodel_name='a3lms.assessment.line', inverse_name='assessment_id', string='Assessment Lines')
	ngraded = fields.Char(string='Submissions', compute='_stats')
	
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
			rec.ngraded = '12/15'

	def get_assessment_lines(self):
		self.ensure_one()
		domain = [('assessment_id', '=', self.id)]
		return self._resolve_action('a3lms.action_assessment_line', domain)

	def get_submissions(self):
		self.ensure_one()
		domain = [('assessment_id', '=', self.id)]
		context = {'default_assessment_id': self.id}
		return self._resolve_action('a3lms.action_assessment_submission', domain, context)


	