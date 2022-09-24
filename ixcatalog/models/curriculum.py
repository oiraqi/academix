from odoo import models, fields, api


class Curriculum(models.Model):
	_name = 'ixcatalog.curriculum'
	_description = 'Curriculum'
	_order = 'school_id,program_id,starting_term_id'

	name = fields.Char('Name', compute="_compute_name_code", store=True)
	code = fields.Char('Code', compute="_compute_name_code", store=True)

	@api.onchange('program_id', 'starting_term_id')
	def _compute_name_code(self):
		for rec in self:
			if rec.program_id and rec.starting_term_id:
				rec.name = rec.program_id.name + ' / ' + rec.starting_term_id.name
				rec.code = rec.program_id.code + '-' + rec.starting_term_id.code
			else:
				rec.name = ''
				rec.code = ''
	
	school_id = fields.Many2one(comodel_name='ix.school', string='School', required=True)
	program_id = fields.Many2one(comodel_name='ixcatalog.program', string='Program', required=True)
	starting_term_id = fields.Many2one(comodel_name='ix.term', string='Starting Term', required=True)	
	level = fields.Selection(related='program_id.level', store=True)	
	component_ids = fields.Many2many('ixcatalog.component', 'ixcatalog_program_component_rel', 'program_id', 'component_id', string='Components')
	sch = fields.Integer(compute='_compute_sch_ncomponents', string='SCH')
	ncomponents = fields.Integer(compute='_compute_sch_ncomponents', string='Number of Components')
	
    
	@api.onchange('component_ids')
	@api.depends('component_ids')
	def _compute_sch_ncomponents(self):
		for rec in self:
			rec.sch = sum(component.sch for component in rec.component_ids if not component.parent_id)
			rec.ncomponents = sum(1 for component in rec.component_ids if not component.parent_id)
	