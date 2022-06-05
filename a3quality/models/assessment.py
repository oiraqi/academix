from odoo import api, models, fields
from odoo.exceptions import UserError


class Assessment(models.Model):
	_name = 'a3quality.assessment'
	_description = 'Assessment'
	_inherit = 'a3.school.owned'
	_sql_constraints = [('a3quality_assessment_portfolio_program_ukey', 'unique(portfolio_id, program_id)', 'Duplicate assessment of the same program in the same portfolio!')]

	portfolio_id = fields.Many2one('a3quality.portfolio', 'Portfolio', required=True)	
	program_id = fields.Many2one('a3catalog.program', 'Program', required=True)
	nstudents = fields.Integer('Student Population', required=True)

	@api.constrains('nstudents')
	def _nstudents(self):
		for rec in self:
			if rec.nstudents <= 0:
				raise UserError('The student population (size) must be > 0')
			if rec.nstudents > 50:
				raise UserError('The student population is unusually large')

	kpi = fields.Selection(string='Minimum ILO Acquisition %', selection=[
		('70', '70'), ('75', '75'), ('80', '80'),
		('85', '85'), ('90', '90'), ('95', '95'), ('100', '100')], default='80', required=True)
	used_assessment_technique_ids = fields.Many2many(comodel_name='a3quality.assessment.technique', compute='_uat_ids')

	@api.onchange('portfolio_id')
	def _uat_ids(self):
		for rec in self:
			if not rec.portfolio_id or \
				(not rec.portfolio_id.useful_assessment_technique_ids and \
					not rec.not_recommended_assessment_technique_ids):
				rec.used_assessment_technique_ids = False
				continue
			
			used_assessment_technique_ids = []
			
			for uat in rec.portfolio_id.useful_assessment_technique_ids:
				used_assessment_technique_ids.append(uat.id)
			
			for uat in rec.portfolio_id.not_recommended_assessment_technique_ids:
				used_assessment_technique_ids.append(uat.id)
			
			rec.used_assessment_technique_ids = used_assessment_technique_ids

	assessment_line_ids = fields.One2many(comodel_name='a3quality.assessment.line', inverse_name='assessment_id', string='Assessment Lines')

	@api.onchange('program_id')
	def _onchange_program_id(self):
		for rec in self:
			rec.assessment_line_ids = False

	course_id = fields.Many2one(comodel_name='a3.course', string='Course', required=True)
	section_id = fields.Many2one('a3roster.section', related='portfolio_id.section_id')
	faculty_id = fields.Many2one(comodel_name='a3.faculty', related='section_id.instructor_id', store=True)
	ilo_so_ids = fields.One2many(comodel_name='a3quality.course.ilo.so', compute='_ilo_so_ids', string='ILO/SO Mapping')
	assessed_so_ids = fields.One2many(comodel_name='a3quality.student.outcome', compute='_ilo_so_ids', string='Covered/Assessed SOs')
	
	def _ilo_so_ids(self):
		for rec in self:
			records = self.env['a3quality.course.ilo.so'].search([('course_id', '=', rec.course_id.id), ('program_id', '=', rec.program_id.id)])
			if not records:
				rec.ilo_so_ids = False
				rec.assessed_so_ids = False
				continue
			rec.ilo_so_ids = records
			rec.assessed_so_ids = [record.so_id.id for record in records]
