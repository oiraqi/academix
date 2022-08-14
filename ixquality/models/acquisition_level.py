from odoo import models, fields


class AcquisitionLevel(models.Model):
	_name = 'ixquality.acquisition.level'
	_description = 'Acquisition Level'

	name = fields.Char('Name', required=True)
	value = fields.Integer(string='Value', required=True)	
	