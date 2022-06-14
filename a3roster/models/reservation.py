from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Reservation(models.Model):
	_name = 'a3roster.reservation'
	_inherit = 'a3.calendarized'
	_description = 'Reservation'
	_order = 'start_time desc,end_time'

	@api.model
	def create(self, vals):
		record = super(Reservation, self).create(vals)
		record.set_event(record.section_id and record.section_id.name or record.description, partner_ids=[record.create_uid.partner_id.id])
		return record

	purpose = fields.Selection(string='Purpose', selection=[('makeup', 'Make-up'), ('presentation', 'Presentation'), ('meeting', 'Meeting'), ('event', 'Event'), ('other', 'Other')], default='makeup', required=True)	
	section_id = fields.Many2one(comodel_name='a3roster.section', string='Section')
	description = fields.Char(string='Brief description')
	room_min_capacity = fields.Selection(string='Minimum Capacity', selection=[
		('5', '5'), ('10', '10'), ('15', '15'), ('20', '20'),
		('25', '25'), ('30', '30'), ('35', '35'), ('40', '40'),
		('45', '45'), ('50', '50'), ('75', '75'), ('100', '100'),], default='15', required=True)
	room_type = fields.Selection(string='Type', selection=[('classroom', 'Classroom'),
        ('lab', 'Lab'), ('general', 'General Purpose')], default='classroom', required=True)
	room_capacity = fields.Integer(related='room_id.capacity')
	
	@api.constrains('room_id', 'start_time', 'end_time')
	def check_conflict(self):
		for rec in self:
			if self.env['a3roster.reservation'].search([('room_id', '=', rec.room_id.id), ('start_time', '<', rec.end_time), ('end_time', '>', rec.start_time )]):
				raise ValidationError('Reservation conflict! Please select another room or change the timeslot.')
	
	def _make_reservation(self):
		return