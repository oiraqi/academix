from odoo import api, fields, models


class Classroom(models.Model):
    _name = 'a3roster.classroom'
    _description = 'Classroom'

    name = fields.Char(string='Name & Building', compute='_compute_name', store=True)
    name_only = fields.Char(string='Name', required=True)
    building_id = fields.Many2one(comodel_name='a3roster.building', string='Building')

    @api.depends('name_only', 'building_id')
    @api.onchange('name_only', 'building_id')
    def _compute_name(self):
        for rec in self:
            if rec.name_only and rec.building_id:
                rec.name = rec.name_only + ' / ' + rec.building_id.name
            else:
                rec.name = False
