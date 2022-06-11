from odoo import models, fields


class Reservation(models.Model):
	_name = 'a3.reservation'

	name = fields.Char('Name', required=True)
	