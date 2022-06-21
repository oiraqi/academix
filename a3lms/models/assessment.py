from odoo import models, fields


class Assessment(models.Model):
	_name = 'a3lms.assessment'
	_description = 'LMS Assessment'
	_inherit = 'a3.calendarized'
	_order = 'start_time,module_id'

	name = fields.Char('Name', required=True)
	course_id = fields.Many2one(comodel_name='a3lms.course', string='LMS Course', required=True)
	module_id = fields.Many2one(comodel_name='a3lms.module', string='Module', required=True)
	technique_id = fields.Many2one(comodel_name='a3lms.assessment.technique', string='Assessment Technique', required=True)
	weight = fields.Float(string='Weight (%)')
	assessment_technique_ids = fields.One2many(comodel_name='a3lms.assessment.technique', related='course_id.assessment_technique_ids')
	module_ids = fields.One2many(comodel_name='a3lms.module', related='course_id.module_ids')
				