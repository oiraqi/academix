from odoo import models, fields


class FacultyShare(models.Model):
	_name = 'ixdms.faculty.share'
	_description = 'Faculty Share'
	_inherit = 'ix.school.owned'
	_sql_constraints = [('share_ukey', 'unique(node_id, school_id, discipline_id)', 'Duplicate shares!')]

	node_id = fields.Many2one(comodel_name='ixdms.node', string='Node', required=True)
	discipline_id = fields.Many2one(comodel_name='ix.discipline', string='Discipline')
	