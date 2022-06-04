from odoo import fields, models


class Student(models.Model):
    _inherit = 'a3.student'

    program_id = fields.Many2one(comodel_name='a3catalog.program', string='Program')
    advisor_id = fields.Many2one(comodel_name='a3.faculty', string='Advisor')    
