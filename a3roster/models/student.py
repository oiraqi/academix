from odoo import fields, models

from odoo.exceptions import UserError


class Student(models.Model):
    _inherit = 'a3.student'

    section_ids = fields.Many2many('a3roster.section', 'a3roster_section_student_rel', 'student_id', 'section_id', 'Sections')
