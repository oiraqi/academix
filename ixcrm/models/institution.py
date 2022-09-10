from odoo import models, fields


class Institution(models.Model):
	_name = 'ixcrm.institution'
	_description = 'Institution'
	_inherits = {'res.partner': 'partner_id'}

	name = fields.Char('Name', required=True)
	education_system_id = fields.Many2one(comodel_name='ixcrm.education.system', string='Education System', required=True)
	partner_id = fields.Many2one(comodel_name='res.partner', string='Partner', required=True)	
	
	