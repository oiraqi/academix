from odoo import models, fields, api


class Session(models.Model):
	_name = 'ix.session'
	_description = 'Session'
	_order = 'sequence'
	_sql_constraints = [('sequence_ukey', 'unique(sequence)', 'Sequence already exists')]

	name = fields.Char('Name', required=True)
	code = fields.Char(string='Code', required=True)
	sequence = fields.Integer(string='Sequence', required=True)
	max_ncourses = fields.Integer(string='Max Number of Courses', required=True)	
	
	@api.model
	def get_first_session(self):
		sessions = self.search([], order='sequence')
		if sessions:
			return sessions[0]
		return False

	@api.model
	def get_session(self, sequence):
		sessions = self.search([('sequence', '=', sequence)])
		if sessions:
			return sessions[0]
		return False
	
	def get_next(self):
		self.ensure_one()
		sessions = self.env['ix.session'].search([('sequence', '>', self.sequence)], order='sequence')
		if sessions:
			return sessions[0]
		return False
