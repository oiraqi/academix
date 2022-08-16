from odoo import models, fields


class Event(models.Model):
	_name = 'calendar.event'
	_inherit = ['calendar.event', 'ix.activity']
	_description = 'Event'

	allday = fields.Boolean('All Day', default=True)
	meta = fields.Selection(string='Type', selection=[('add_drop', 'Add/Drop'), ('w', 'Last day to drop a course with W'), ('grade_submission', 'Grade Submission')])
	
	