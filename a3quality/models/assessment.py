from odoo import models, fields


class Assessment(models.Model):
	_name = 'a3quality.assessment'
	_description = 'Assessment'
	_inherit = 'a3.school.owned'
	_sql_constraints = [('a3quality_assessment_portfolio_program_ukey', 'unique(portfolio_id, program_id)', 'Duplicate assessment of the same program in the same portfolio!')]

	name = fields.Char('Name', required=True)
	portfolio_id = fields.Many2one('a3quality.portfolio', 'Portfolio', required=True)	
	program_id = fields.Many2one('a3catalog.program', 'Program', required=True)
	nstudents = fields.Integer('Student Population', required=True)
	kpi = fields.Integer(string='ILO Achievement Threshold (%)', default=80)
	assessment_line_ids = fields.One2many(comodel_name='a3quality.assessment.line', inverse_name='assessment_id', string='Assessment Lines')
	course_id = fields.Many2one(comodel_name='a3.course', string='Course', required=True)
	section_id = fields.Many2one('a3roster.section', related='portfolio_id.section_id')
	faculty_id = fields.Many2one(comodel_name='a3.faculty', related='section_id.instructor_id', store=True)	
	