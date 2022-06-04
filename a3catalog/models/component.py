from odoo import api, fields, models


class Component(models.Model):
    _name = 'a3catalog.component'
    _description = 'Program Component'
    _inherit = 'a3.school.owned'

    name = fields.Char(string='Name', required=True)
    sch = fields.Integer(string='SCH', required=True)
    
    level = fields.Selection(
        [('u', 'Undergraduate'), ('g', 'Graduate')], 'Level', default='u', required=True)
    sequence = fields.Integer(string='Sequence', default=1)
    program_ids = fields.Many2many(
        'a3catalog.program', 'a3catalog_program_component_rel', 'component_id', 'program_id', string='Programs')
    parent_id = fields.Many2one(
        comodel_name='a3catalog.component', string='Parent Component')
    child_ids = fields.One2many(
        comodel_name='a3catalog.component', inverse_name='parent_id', string='Sub-components')
    course_ids = fields.Many2many(
        'a3.course', 'a3catalog_component_course_rel', 'component_id', 'course_id', string='Courses')
    hide_children = fields.Boolean(
        compute='_compute_hide_children', string='hide_children')

    @api.depends('child_ids')
    def _compute_hide_children(self):
        for rec in self:
            if rec.child_ids or self.env.ref('a3.group_setup') in self.sudo().env.user.groups_id or self.env.ref('a3.group_coordinator') in self.sudo().env.user.groups_id:
                rec.hide_children = False
            else:
                rec.hide_children = True

    hide_courses = fields.Boolean(
        compute='_compute_hide_courses', string='hide_courses')

    @api.depends('course_ids')
    def _compute_hide_courses(self):
        for rec in self:
            if rec.course_ids or self.env.ref('a3.group_setup') in self.sudo().env.user.groups_id or self.env.ref('a3.group_coordinator') in self.sudo().env.user.groups_id:
                rec.hide_courses = False
            else:
                rec.hide_courses = True
