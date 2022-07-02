from odoo import models, fields, api


class Faculty(models.Model):
    _inherit = 'ix.faculty'

    office_hour_ids = fields.One2many(comodel_name='ixroster.office.hour', inverse_name='faculty_id', string='Office Hours')
    