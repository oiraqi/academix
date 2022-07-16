from odoo import models, fields


class StudentShare(models.Model):
	_name = 'ixdms.student.share'
	_description = 'Student Share'
	_inherit = 'ix.school.owned'
	_sql_constraints = [('share_ukey', 'unique(share_id, school_id, program_id)', 'Duplicate shares!')]

	share_id = fields.Many2one(comodel_name='ixdms.share', string='Node', required=True)
	program_id = fields.Many2one(comodel_name='ixcatalog.program', string='Program')
		