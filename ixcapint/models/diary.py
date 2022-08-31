from odoo import models, fields


class Diary(models.Model):
	_name = 'ixcapint.diary'
	_description = 'Diary'
	_inherit = ['ix.expandable', 'mail.thread']

	name = fields.Char('Title', required=True, readonly=True, states={'draft': [('readonly', False)], 'corrections_requested': [('readonly', False)]})
	content = fields.Html(string='Content', required=True, readonly=True, states={'draft': [('readonly', False)], 'corrections_requested': [('readonly', False)]})
	state = fields.Selection(string='State', selection=[('draft', 'Draft'), 
		('submitted', 'Submitted by Student'), ('corrections_requested', 'Corrections Requested'), ('checked', 'Checked by Supervisor')],
		default='draft', required=True, tracking=True)
	submission_time = fields.Datetime(string='Submitted by Student At')
	checking_time = fields.Datetime(string='Checked by Supervisor At')
	project_id = fields.Many2one(comodel_name='ixcapint.project', string='Project', required=True)
	supervisor_id = fields.Many2one('ix.faculty', related='project_id.supervisor_id', store=True)
	student_id = fields.Many2one('ix.student', related='project_id.student_id', store=True)
	
	def submit_diary(self):
		self.ensure_one()
		self.state = 'submitted'
		self.submission_time = fields.Datetime.now()

	def correct_diary(self):
		self.ensure_one()
		self.state = 'corrections_requested'
	
	def check_diary(self):
		self.ensure_one()
		self.state = 'checked'
		self.checking_time = fields.Datetime.now()

	def open_diary(self):
		self.ensure_one()		
		return self._expand_to('ixcapint.action_diary', [('id', '=', self.context.get('active_id'))], {'default_project_id': self.project_id.id}, self.context.get('active_id'))

