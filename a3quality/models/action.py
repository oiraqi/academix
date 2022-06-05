from odoo import api, models, fields


class Action(models.Model):
	_name = 'a3quality.action'
	_description = 'Action'

	name = fields.Char('Title', required=True)
	description = fields.Html(string='Description', required=True)	
	portfolio_id = fields.Many2one(comodel_name='a3quality.portfolio', string='Portfolio')
	assessment_line_id = fields.Many2one(comodel_name='a3quality.assessment.line', string='Assessment Line')
	ilo_id = fields.Many2one(comodel_name='a3catalog.course.ilo', string='ILO')
	assessment_criteria = fields.Text(string='Assessment Criteria')
	assessment_methodology = fields.Text(string='Assessment Methodology')
	assessment_results = fields.Text(string='Assessment Results')

	@api.depends('assessment_line_id')
	@api.onchange('assessment_line_id')
	def _assessment_line(self):
		for rec in self:
			if rec.assessment_line_id:
				rec.portfolio_id = rec.assessment_line_id.assessment_id.portfolio_id
				rec.ilo_id = rec.assessment_line_id.ilo_id

	state = fields.Selection([
        ('planned', 'Planned'), ('implemented', 'Implemented'),
        ('assessed', 'Assessed')], string='State', default='planned', required=True, track=True)
