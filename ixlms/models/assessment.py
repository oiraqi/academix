from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Assessment(models.Model):
	_name = 'ixlms.assessment'
	_description = 'LMS Assessment'
	_inherit = 'ix.expandable'
	_order = 'due_time,module_id'

	def write(self, vals):
		outcome = super(Assessment, self).write(vals)
		if 'grade_scale' in vals:
			for rec in self:
				for assessment_line in rec.assessment_line_ids:
					try:
						if assessment_line.grade and float(assessment_line.grade):
							assessment_line.grade = str((assessment_line.egrade - rec.bonus + assessment_line.penalty) * rec.grade_scale / 100)
					except TypeError:
						continue
		return outcome


	name = fields.Char('Name', required=True)
	description = fields.Html(string='Description')
	
	course_id = fields.Many2one(comodel_name='ixlms.course', string='LMS Course', required=True)
	section_id = fields.Many2one(comodel_name='ixroster.section', string='course_id.section_id', store=True)
	module_id = fields.Many2one(comodel_name='ixlms.module', string='Module', required=True)
	technique_id = fields.Many2one(comodel_name='ixlms.weighted.technique', string='Technique', required=True)
	graded = fields.Boolean(string='Graded', required=True, default=True)
	grade_weighting = fields.Selection(related='course_id.grade_weighting')
	points = fields.Integer(string='Points', required=True, default=0)
	percentage = fields.Float(string='%', required=True, default=0.0)
	grade_scale = fields.Integer(string='Graded over', required=True, default=100)

	@api.constrains('grade_scale')
	def _check_grade_scale(self):
		for rec in self:
			if rec.grade_scale <= 0:
				raise ValidationError('Grade scale must strictly positive!')

	@api.onchange('graded')
	def _graded(self):
		for rec in self:
			if not rec.graded:
				rec.points = 0
				rec.percentage = 0.0
				rec.grade_scale = 0

	@api.onchange('grade_weighting', 'points', 'percentage')
	def _percentage_points_grade_scale(self):
		for rec in self:
			if rec.grade_weighting == 'percentage':
				if rec.percentage > 0:
					rec.graded = True
				rec.grade_scale = 100
			elif rec.grade_weighting == 'points':
				if rec.points > 0:
					rec.graded = True				
					rec.grade_scale = rec.points
				elif rec.graded and rec.grade_scale == 0:
					rec.grade_scale = 100
				

	
	@api.constrains('points')
	def _check_points(self):
		for rec in self:
			if rec.points < 0:
				raise ValidationError('The assessment points must be >= 0')

	@api.constrains('percentage')
	def _check_percentage(self):
		for rec in self:
			if rec.percentage < 0 or rec.percentage > 100:
				raise ValidationError('The assessment % must be between 0 and 100%')

			rec.course_id.check_sum_percentages()
	
	technique_ids = fields.One2many(comodel_name='ixlms.weighted.technique', related='course_id.technique_ids')
	module_ids = fields.One2many(comodel_name='ixlms.module', related='course_id.module_ids')

	submission_type = fields.Selection(string='Submission Type', selection=[('online', 'Online'), ('paper', 'Paper'), ('nosub', 'No Submission / Self-assessment')], required=True, default='online')
	is_file_req = fields.Boolean(string='File Required', default=False)
	is_url_req = fields.Boolean(string='URL Required', default=False)
	is_text_req = fields.Boolean(string='Inline Text Required', default=False)

	@api.constrains('allowed_attempts')
	def _check_allowed_attempts(self):
		for rec in self:
			if rec.allowed_attempts <= 0:
				raise ValidationError('At least one submission attempt should be allowed!')

	teamwork = fields.Boolean(string='Teamwork', required=True, default=False)
	teamset_id = fields.Many2one(comodel_name='ixlms.teamset', string='Team Set')

	timeline = fields.Boolean(string='Common Timeline', default=True, required=True)
	due_time = fields.Datetime(string='Due')
	from_time = fields.Datetime(string='Open from')
	to_time = fields.Datetime(string='Until')

	timelines = fields.Boolean(string='Specific Timelines', default=False)

	timeline_ids = fields.One2many(comodel_name='ixlms.assessment.timeline', inverse_name='assessment_id', string='Specific Timelines')
		
	bonus = fields.Float(string='Class-wide Bonus (%)', default=0.0)

	@api.constrains('bonus')
	def _check_bonus(self):
		for rec in self:
			if rec.bonus < 0:
				raise ValidationError('The assessment bonus must be >= 0')

	@api.model
	def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
		if 'bonus' in fields:
			fields.remove('bonus')
		return super(Assessment, self).read_group(domain, fields, groupby, offset, limit, orderby, lazy)

	penalty_per_late_day = fields.Float(string='Penalty per Late Day (%)', default=0.0)

	@api.constrains('penalty_per_late_day')
	def _check_penalty(self):
		for rec in self:
			if rec.penalty_per_late_day < 0:
				raise ValidationError('The assessment penalty per late day must be >= 0')

	assessment_line_ids = fields.One2many(comodel_name='ixlms.assessment.line', inverse_name='assessment_id', string='Assessment Lines')
	ngraded = fields.Char(string='Submissions', compute='_stats')
	submission_ids = fields.One2many(comodel_name='ixlms.assessment.submission', inverse_name='assessment_id', string='Submisions')	
	nsubmissions = fields.Integer(string='Submissions', compute='_stats')
	
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
			rec.nsubmissions = len(rec.submission_ids)

	def get_assessment_lines(self):
		self.ensure_one()
		student_ids = [assessment_line.student_id.id for assessment_line in self.assessment_line_ids]
		for student in self.course_id.student_ids:
			if student.id not in student_ids:
				self.env['ixlms.assessment.line'].create({
					'assessment_id': self.id,
					'student_id': student.id
				})
		domain = [('assessment_id', '=', self.id)]
		return self._resolve_action('ixlms.action_assessment_line', domain)

	def get_submissions(self):
		self.ensure_one()
		domain = [('assessment_id', '=', self.id)]
		context = {'default_assessment_id': self.id}
		return self._resolve_action('ixlms.action_assessment_submission', domain, context)

	def get_grade_distribution(self):
		self.ensure_one()
		domain = [('assessment_id', '=', self.id)]
		return self._resolve_action('ixlms.action_assessment_line_dist', domain)
