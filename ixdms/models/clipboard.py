from odoo import models, fields


class Clipboard(models.Model):
	_name = 'ixdms.clipboard'
	_description = 'Clipboard'
	_sql_constraints = [('owner_ukey', 'unique(create_uid)', 'One entry per user')]

	node_id = fields.Many2one(comodel_name='ixdms.node', string='Node', required=True)
	operation = fields.Selection(string='Operation', selection=[('copy', 'Copy'), ('cut', 'Cut')], required=True)
	processed = fields.Boolean(default=False)	
	