from odoo import models, fields, api


class Curriculum(models.Model):
	_name = 'ixcatalog.curriculum'
	_description = 'Curriculum'

	name = fields.Char('Name', required=True)
	code = fields.Char('Code', required=True)
	sequence = fields.Integer('Sequence', required=True)	
	program_id = fields.Many2one(comodel_name='ixcatalog.program', string='Program', required=True)
	level = fields.Selection(related='program_id.level', store=True)
	school_id = fields.Many2one(comodel_name='ix.school', related='program_id.school_id', store=True)
	component_ids = fields.Many2many('ixcatalog.component', 'ixcatalog_program_component_rel', 'program_id', 'component_id', string='Components')
	sch = fields.Integer(compute='_compute_sch_ncomponents', string='SCH')
	ncomponents = fields.Integer(compute='_compute_sch_ncomponents', string='Number of Components')
	
    
	@api.onchange('component_ids')
	@api.depends('component_ids')
	def _compute_sch_ncomponents(self):
		for rec in self:
			rec.sch = sum(component.sch for component in rec.component_ids if not component.parent_id)
			rec.ncomponents = sum(1 for component in rec.component_ids if not component.parent_id)
	