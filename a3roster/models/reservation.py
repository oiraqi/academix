from odoo import models, fields


class Reservation(models.Model):
	_name = 'a3.reservation'
	_inherit = 'a3.calendarized'
	_description = 'Reservation'

	name = fields.Char('Name', required=True)
	section_id = fields.Many2one(comodel_name='a3roster.section', string='Section')
	room_min_capacity = fields.Integer(string='Minimum capacity', required=True)
	room_type = fields.Selection(string='Type', selection=[('classroom', 'Classroom'), ('office', 'Office'),
        ('lab', 'Lab'), ('general', 'General Purpose')], default='classroom', required=True)
	