from odoo import api, fields, models


class Program(models.Model):
    _name = 'a3catalog.program'
    _description = 'Academic Program'
    _inherit = 'a3.school.owned'

    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code', required=True)
    description = fields.Html(string='Description', required=True)    
    level = fields.Selection(
        [('u', 'Undergraduate'), ('g', 'Graduate')], 'Level', default='u', required=True)
    component_ids = fields.Many2many('a3catalog.component', 'a3catalog_program_component_rel', 'program_id', 'component_id', string='Components')
    sch = fields.Integer(compute='_compute_sch_ncomponents', string='SCH')
    ncomponents = fields.Integer(compute='_compute_sch_ncomponents', string='Number of Components')
    
    @api.onchange('component_ids')
    @api.depends('component_ids')
    def _compute_sch_ncomponents(self):
        for rec in self:
            rec.sch = sum(component.sch for component in rec.component_ids if not component.parent_id)
            rec.ncomponents = sum(1 for component in rec.component_ids if not component.parent_id)
