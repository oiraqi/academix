# -*- coding: utf-8 -*-
###############################################################################
#
#    Al Akhawayn University in Ifrane -- AUI
#    Copyright (C) 2022-TODAY AUI(<http://www.aui.ma>).
#
#    Author: Omar Iraqi Houssaini | https://github.com/oiraqi
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

from odoo import models, fields, api
from odoo.exceptions import ValidationError


SEMESTERS = {'1': 'FA', '2': 'SP', '3': 'SU'}


class Project(models.Model):
    _name = 'a3capint.project'
    _inherit = ['a3.school.activity', 'mail.thread']
    _description = 'A capstone, internship, combined, master project or thesis'

    name = fields.Char('Title', required=True, readonly=True,
                       states={'draft': [('readonly', False)]})

    student_id = fields.Many2one('a3.student', string='Student', required=True, readonly=True,
                                 default=lambda self: self.env['a3.student'].search(
                                     [('user_id', '=', self.env.user.id)]),
                                 states={'draft': [('readonly', False)]})

    type = fields.Selection([('CAP', 'Capstone'), ('INT',
                            'Internship'), ('CMB', 'Combined'),
                             ('MP', 'Master Project'), ('MT', 'Master Thesis')],
                            'Type', default='capstone', required=True,
                            readonly=True, states={'draft': [('readonly', False)]})

    code = fields.Char(compute='_compute_code', string='Code')

    @api.onchange('year', 'semester', 'type')
    @api.depends('year', 'semester', 'type')
    def _compute_code(self):
        for rec in self:
            if rec.state != 'draft':
                rec.code = rec.prefix + rec.type + str(rec.id)
            else:
                rec.code = ''

    supervisor_id = fields.Many2one('a3.faculty', string='Supervisor', required=True,
                                    default=lambda self: self.env['a3.faculty'].search(
                                        [('user_id', '=', self.env.user.id)]),
                                    readonly=True, states={'draft': [('readonly', False)]})
    
    is_supervisor = fields.Boolean(compute='_compute_is_supervisor', string='is_supervisor')
    
    @api.onchange('supervisor_id')
    @api.depends('supervisor_id')
    def _compute_is_supervisor(self):
        for rec in self:
            rec.is_supervisor = rec.supervisor_id.user_id == self.env.user
    

    initial_idea = fields.Html(string='Initial Idea', required=True,
                               readonly=True, states={'draft': [('readonly', False)]})
    final_abstract = fields.Html(string='Final Abstract',
                                 readonly=True, states={'defense': [('readonly', False)]})

    tag_ids = fields.Many2many(
        comodel_name='a3capint.tag', string='Keywords', required=True)

    reader_id = fields.Many2one('a3.faculty', string='Second Reader',
                                readonly=True, states={'ongoing': [('readonly', False)]})

    external_examiner_id = fields.Many2one('res.partner', string='External Examiner',
                                           readonly=True, states={'ongoing': [('readonly', False)]})

    date_time_defense = fields.Datetime('Date & Time of Defense',
                                        readonly=True, states={'ongoing': [('readonly', False)]})

    evaluation_ids = fields.One2many('a3capint.evaluation', 'project_id', 'Evaluations',
                                     readonly=True, states={'defense': [('readonly', False)]})

    final_report = fields.Binary(string='Final Report')

    state = fields.Selection([
        ('draft', 'Draft Proposal'), ('supervisor', 'Approved by The Supervisor'),
        ('ongoing', 'Approved by The Coordinator - Ongoing'), ('defense',
                                                               'Scheduled for Defense'), ('done', 'Completed')
    ], string='State', default='draft', required=True, track=True)

    def supervisor_approve(self):
        self.write({'state': 'supervisor'})

    def coordinator_approve(self):
        self.write({'state': 'ongoing'})

    def schedule_defense(self):
        for rec in self:
            if not rec.reader_id:
                raise ValidationError('The second reader must be set!')

        self.write({'state': 'defense'})

    def mark_done(self):
        self.write({'state': 'done'})
