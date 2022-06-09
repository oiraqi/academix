from odoo import models, fields


class Event(models.Model):
    _inherit = 'calendar.event'
	
    
    student_id = fields.Many2one(comodel_name='a3.student', string='Student')
    