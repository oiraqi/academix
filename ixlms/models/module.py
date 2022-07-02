from odoo import models, fields, api


class Module(models.Model):
	_name = 'ixlms.module'
	_description = 'Module'
	_order = 'sequence'

	name = fields.Char('Name', required=True)
	sequence = fields.Integer(string='Sequence')
	points = fields.Integer(string='Points', compute='_points')
	percentage = fields.Float(string='%', compute='_percentage')
	course_id = fields.Many2one(comodel_name='ixlms.course', string='LMS Course', required=True)
	assessment_ids = fields.One2many(comodel_name='ixlms.assessment', inverse_name='module_id', string='Assessments')
	chapter_ids = fields.One2many(comodel_name='ixlms.chapter', inverse_name='module_id', string='Chapters & Timeline')

	@api.onchange('assessment_ids')
	def _points(self):
		for rec in self:			
			if rec.assessment_ids:
				rec.points = sum([assessment.points for assessment in rec.assessment_ids])
			else:
				rec.points = 0

	@api.onchange('assessment_ids')
	def _percentage(self):
		for rec in self:			
			if rec.assessment_ids:
				rec.percentage = sum([assessment.percentage for assessment in rec.assessment_ids])
			else:
				rec.percentage = 0