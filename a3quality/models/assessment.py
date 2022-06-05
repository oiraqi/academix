from odoo import models, fields


class Assessment(models.Model):
	_name = 'a3quality.assessment'
	_description = 'Assessment'
	_sql_constraints = [('a3quality_assessment_portfolio_program_ukey', 'unique(section_id, program_id)', 'Duplicate assessment of the same program in the same portfolio!')]

	name = fields.Char('Name', required=True)
	portfolio_id = fields.Many2one('a3quality.portfolio', 'Portfolio', required=True)	
	program_id = fields.Many2one('a3catalog.program', 'Program', required=True)
	nstudents = fields.Integer('Student Population', required=True)
	kpi = fields.Integer(string='Achievement Threshold per ILO (%), e.g., 80')
	assessment_line_ids = fields.One2many(comodel_name='a3quality.assessment.line', inverse_name='assessment_id', string='Assessment Lines')	
	section_id = fields.Many2one('a3roster.section', related='portfolio_id.section_id')
	faculty_id = fields.Many2one(comodel_name='a3.faculty', related='section_id.instructor_id', store=True)
	course_id = fields.Many2one(comodel_name='a3.course', related='section_id.course_id', store=True)
	school_id = fields.Many2one(comodel_name='a3.school', related='section_id.school_id', store=True)
	