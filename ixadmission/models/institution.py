from odoo import models, fields


class Institution(models.Model):
	_name = 'ixadmission.institution'
	_description = 'Institution'
	_inherits = {'res.partner': 'partner_id'}

	education_system_id = fields.Many2one(comodel_name='ixadmission.education.system', string='Education System', required=True)
	partner_id = fields.Many2one(comodel_name='res.partner', string='Partner', required=True)	
	company_type = fields.Selection(related='partner_id.company_type', store=True, readonly=False)
	
	