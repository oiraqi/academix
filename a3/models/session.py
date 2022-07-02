from odoo import models, fields


class Session(models.Model):
	_name = 'ix.session'
	_description = 'Session'
	_sql_constraints = [('sequence_ukey', 'unique(sequence)', 'Sequence already exists')]

	name = fields.Char('Name', required=True)
	code = fields.Char(string='Code', required=True)	
	sequence = fields.Integer(string='Sequence', required=True)	
	