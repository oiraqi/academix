from odoo import api, fields, models


class School(models.Model):
    _inherit = 'a3.school'

    program_ids = fields.One2many(comodel_name='a3catalog.program', inverse_name='school_id', string='Programs')
    
