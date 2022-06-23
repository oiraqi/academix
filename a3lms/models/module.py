from odoo import models, fields, api


class Module(models.Model):
	_name = 'a3lms.module'
	_description = 'Module'
	_order = 'sequence'

	name = fields.Char('Name', required=True)
	sequence = fields.Integer(string='Sequence', required=True)	
	points = fields.Integer(string='Points', compute='_points')
	percentage = fields.Float(string='%', default=0.0)
	course_id = fields.Many2one(comodel_name='a3lms.course', string='LMS Course', required=True)
	assessment_ids = fields.One2many(comodel_name='a3lms.assessment', inverse_name='module_id', string='Assessments')

	def _points(self):
		for rec in self:			
			if rec.assessment_ids:
				rec.points = sum([assessment.points for assessment in rec.assessment_ids])
			else:
				rec.points = 0