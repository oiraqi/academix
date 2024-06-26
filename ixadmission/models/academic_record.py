from odoo import models, fields


class AcademicRecord(models.Model):
	_name = 'ixadmission.academic.record'
	_description = 'Academic Record'
	_order = 'rx_date'	

	lead_id = fields.Many2one(comodel_name='crm.lead', string='Lead', required=True)
	partner_id = fields.Many2one(comodel_name='res.partner', related='lead_id.partner_id', store=True)	
	institution_id = fields.Many2one(comodel_name='ixadmission.institution', string='Institution', required=True)
	education_system_id = fields.Many2one(comodel_name='ixadmission.education.system', related='institution_id.education_system_id', store=True)
	degree_id = fields.Many2one(comodel_name='ixadmission.degree', string='Degree', required=True)
	rx_date = fields.Date(string='Earned/Expected Date', required=True)
	
	
	