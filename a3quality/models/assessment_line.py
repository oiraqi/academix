from odoo import api, models, fields


class AssessmentLine(models.Model):
	_name = 'a3quality.assessment.line'
	_description = 'AssessmentLine'

	assessment_id = fields.Many2one('a3quality.assessment', 'Assessment', required=True)
	course_id = fields.Many2one(comodel_name='a3.course', required=True)
	faculty_id = fields.Many2one(comodel_name='a3.faculty', related='assessment_id.faculty_id', store=True)	
	ilo_id = fields.Many2one('a3catalog.course.ilo', 'ILO', required=True)
	so_ids = fields.One2many('a3quality.student.outcome', compute='_so_ids', string='SOs')
	assessment_technique_ids = fields.Many2many(comodel_name='a3quality.assessment.technique', string='Techniques', required=True)
	used_assessment_technique_ids = fields.Many2many(comodel_name='a3quality.assessment.technique', related='assessment_id.used_assessment_technique_ids')
	targetted = fields.Float('Targetted', required=True, default=80)
	achieved = fields.Float('Achieved', required=True)
	action_id = fields.Many2one('a3quality.action', 'Action')

	@api.onchange('ilo_id', 'assessment_id')
	def _so_ids(self):
		for rec in self:
			if not rec.ilo_id or not rec.assessment_id:
				rec.so_ids = False
				continue
			
			records = self.env['a3quality.course.ilo.so'].search([
				('course_program_id.program_id', '=', rec.assessment_id.program_id.id),
				('course_ilo_ids', 'in', rec.ilo_id)])
			if not records:
				rec.so_ids = False
			else:
				rec.so_ids = [record.so_id.id for record in records]
