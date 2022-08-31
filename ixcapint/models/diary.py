from odoo import models, fields, api


STATES = [('draft', 'Draft'), 
		('submitted', 'Submitted by Student'), ('corrections_required', 'Corrections Required'), ('checked', 'Checked by Supervisor')]

STATES_DICT = dict(STATES)

class Diary(models.Model):
	_name = 'ixcapint.diary'
	_description = 'Diary'
	_inherit = ['ix.expandable', 'mail.thread']

	@api.model
	def create(self, vals):
		diary = super(Diary, self).create(vals)
		diary.message_subscribe([diary.project_id.supervisor_id.partner_id.id])
		return diary

	name = fields.Char('Title', required=True, readonly=True, states={'draft': [('readonly', False)], 'corrections_required': [('readonly', False)]})
	content = fields.Html(string='Content', required=True, readonly=True, states={'draft': [('readonly', False)], 'corrections_required': [('readonly', False)]})
	state = fields.Selection(string='State', selection=STATES,
		default='draft', required=True, tracking=True)
	submission_time = fields.Datetime(string='Submitted by Student At')
	checking_time = fields.Datetime(string='Checked by Supervisor At')
	project_id = fields.Many2one(comodel_name='ixcapint.project', string='Project', required=True)
	supervisor_id = fields.Many2one('ix.faculty', related='project_id.supervisor_id', store=True)
	student_id = fields.Many2one('ix.student', related='project_id.student_id', store=True)
	
	def submit_diary(self):
		self.ensure_one()
		state = self.state
		self.state = 'submitted'
		self.submission_time = fields.Datetime.now()
		self.message_post(body=f'State Changed: {STATES_DICT[state]} --> {STATES_DICT[self.state]}')

	def correct_diary(self):
		self.ensure_one()
		state = self.state
		self.state = 'corrections_required'
		self.message_post(body=f'State Changed: {STATES_DICT[state]} --> {STATES_DICT[self.state]}')
	
	def check_diary(self):
		self.ensure_one()
		state = self.state
		self.state = 'checked'
		self.checking_time = fields.Datetime.now()
		self.message_post(body=f'State Changed: {STATES_DICT[state]} --> {STATES_DICT[self.state]}')

	def open_diary(self):
		self.ensure_one()		
		return self._expand_to('ixcapint.action_diary', [('id', '=', self.id)], {'default_project_id': self.project_id.id}, self.id)

