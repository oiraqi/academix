from odoo import models, fields


class Event(models.Model):
	_name = 'calendar.event'
	_inherit = ['calendar.event', 'ix.activity']
	_description = 'Event'

	allday = fields.Boolean('All Day', default=True)
	