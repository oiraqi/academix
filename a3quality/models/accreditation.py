from odoo import api, fields, models


class Accreditation(models.Model):
    _name = 'a3quality.accreditation'
    _description = 'Accreditation'
    _inherit = 'a3.school.owned'

    name = fields.Char(string='Name', required=True)
    program_ids = fields.Many2many('a3catalog.program', 'a3quality_program_accreditation_rel', 'accreditation_id', 'program_id', 'Accredited Programs')
