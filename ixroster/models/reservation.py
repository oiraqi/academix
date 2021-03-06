from unicodedata import name
from xml.dom import ValidationErr
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Reservation(models.Model):
	_name = 'ixroster.reservation'
	_inherit = 'ix.calendarized'
	_description = 'Reservation'
	_order = 'start_time desc,end_time'

	@api.model
	def create(self, vals):
		record = super(Reservation, self).create(vals)
		if not record.event_id:
			partners = [record.create_uid.partner_id.id]
			if record.purpose == 'makeup' and record.section_id:
				for student in record.section_id.student_ids:
					partners.append(student.partner_id.id)
				name = 'Makeup ' + record.section_id.name
			else:
				name = record.description
			record.set_event(name , partners)
		return record

	purpose = fields.Selection(string='Purpose', selection=[('makeup', 'Make-up'), ('presentation', 'Presentation'), ('meeting', 'Meeting'), ('event', 'Event'), ('other', 'Other')], default='makeup', required=True)	
	section_id = fields.Many2one(comodel_name='ixroster.section', string='Section')
	description = fields.Char(string='Brief description')
	room_min_capacity = fields.Selection(string='Minimum Capacity', selection=[
		('5', '5'), ('10', '10'), ('15', '15'), ('20', '20'),
		('25', '25'), ('30', '30'), ('35', '35'), ('40', '40'),
		('45', '45'), ('50', '50'), ('75', '75'), ('100', '100'),], default='5', required=True)
	room_type = fields.Selection(string='Type', selection=[('classroom', 'Classroom'),
        ('lab', 'Lab'), ('general', 'General Purpose')], default='classroom', required=True)
	room_capacity = fields.Integer(related='room_id.capacity')
	
	@api.constrains('room_id', 'start_time', 'end_time')
	def check_conflict(self):
		for rec in self:
			if self.env['ixroster.reservation'].search_count([('room_id', '=', rec.room_id.id), ('start_time', '<', rec.end_time), ('end_time', '>', rec.start_time)]) > 1:
				raise ValidationError('Reservation conflict! Please select another room or change the timeslot.')
	
	def _make_reservation(self):
		return

	@api.onchange('section_id')
	def _onchange_section(self):
		for rec in self:
			if rec.section_id:
				if rec.section_id.nstudents > 100:
					raise ValidationError('More than 100!?!')
				if rec.section_id.nstudents == 0:
					rec.room_min_capacity = '5'
				elif rec.section_id.nstudents % 5 == 0:
					rec.room_min_capacity = str(rec.section_id.nstudents)
				else:
					rec.room_min_capacity = str((int(rec.section_id.nstudents / 5) + 1) * 5)

	@api.onchange('start_time', 'end_time', 'room_min_capacity', 'room_type')
	def room_search(self):		
		self.ensure_one()
		candidate_rooms = []
		if self.start_time and self.end_time:			
			available_rooms = self.env['ix.room'].available_rooms(self.start_time, self.end_time)
			candidate_rooms = self.env['ix.room'].search([('id', 'in', available_rooms),
				('capacity', '>=', self.room_min_capacity),
				('type', '=', self.room_type)], order='capacity')
			if not candidate_rooms:
				self.room_id = False
				candidate_rooms = []
			else:
				self.room_id = candidate_rooms[0]
				max_capacity = candidate_rooms[0].capacity + 5
				candidate_rooms = [room.id for room in candidate_rooms if room.capacity <= max_capacity]			
		return {'domain': {'room_id': [('id', 'in', candidate_rooms)]}}
	