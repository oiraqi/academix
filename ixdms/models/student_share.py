from odoo import models, fields


class StudentShare(models.Model):
	_name = 'ixdms.student.share'
	_description = 'Student Share'
	_inherit = 'ix.school.owned'
	_sql_constraints = [('share_ukey', 'unique(node_id, school_id, program_id)', 'Duplicate shares!')]

	node_id = fields.Many2one(comodel_name='ixdms.node', string='Node', required=True)
	program_id = fields.Many2one(comodel_name='ixcatalog.program', string='Program')
		