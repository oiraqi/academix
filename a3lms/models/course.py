from odoo import models, fields


class Course(models.Model):
	_name = 'a3lms.course'
	_description = 'LMS Course'
	_inherit = ['a3.activity']
	_inherits = {'a3.course': 'course_id', 'a3roster.section': 'section_id'}

	section_id = fields.Many2one(comodel_name='a3roster.section', string='Section', required=True)	
	name = fields.Char(related='section_id.name')	
	course_id = fields.Many2one(comodel_name='a3.course', related='section_id.course_id')	
	