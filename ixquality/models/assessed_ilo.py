from odoo import models, fields


class AssessedIlo(models.Model):
	_name = 'ixquality.assessed.ilo'
	_description = 'Assessed ILO'
	_sql_constraints = [('ilo_assessment_line_ukey', 'unique(ilo_id, assessment_line_id)', 'Duplicate ILO assessment!')]

	ilo_id = fields.Many2one(comodel_name='ixcatalog.course.ilo', string='Course ILO', required=True)
	assessment_line_id = fields.Many2one(comodel_name='ixlms.assessment.line', string='LMS Assessment Line', required=True)
	acquisition_level_id = fields.Many2one(comodel_name='ixquality.acquisition.level', string='Acquisition Level')
	assessment_ilo_ids = fields.Many2many(comodel_name='ixcatalog.course.ilo', related='assessment')
	idx_description = fields.Char(related='ilo_id.idx_description')
		