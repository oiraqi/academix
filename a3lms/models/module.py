from odoo import models, fields


class Module(models.Model):
	_name = 'a3lms.module'
	_description = 'Module'
	_order = 'sequence'

	name = fields.Char('Name', required=True)
	sequence = fields.Integer(string='Sequence', required=True)	
	weight = fields.Integer(string='Points', required=True, default=0)
	course_id = fields.Many2one(comodel_name='a3lms.course', string='LMS Course', required=True)
	assessment_ids = fields.One2many(comodel_name='a3lms.assessment', inverse_name='module_id', string='Assessments')
	total_assessment_weights = fields.Float(compute='_total_assessment_weights')

	def _total_assessment_weights(self):
		for rec in self:
			assessments = self.env['a3ls.assessment'].search([('course_id', '=', rec.course_id.id), ('module_id', '=', rec.id)])
			if assessments:
				rec.total_assessment_weights = sum([assessment.weight for assessment in assessments])
			else:
				rec.total_assessment_weights = 0