from odoo import models, fields, api


class Faculty(models.Model):
    _inherit = 'a3.faculty'

    office_hour_ids = fields.One2many(comodel_name='a3roster.office.hour', inverse_name='faculty_id', string='Office Hours')
    