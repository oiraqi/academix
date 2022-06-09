from odoo import models, fields


class Calendarized(models.AbstractModel):
	_name = 'a3.calendarized'
	_description = 'Calendarized'

	event_id = fields.Many2one(comodel_name='calendar.event', string='Event')
	event_start = fields.Datetime(related='event_id.start')
	event_stop = fields.Datetime(related='event_id.stop')
	