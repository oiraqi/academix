from odoo import fields, models


class Building(models.Model):
    _name = 'a3roster.building'
    _description = 'Building'

    name = fields.Char(string='Name', required=True)
