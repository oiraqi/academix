from odoo import models, fields


class Event(models.Model):
    _inherit = 'calendar.event'
	
    
    project_id = fields.Many2one(comodel_name='a3capint.project', string='Project')
    