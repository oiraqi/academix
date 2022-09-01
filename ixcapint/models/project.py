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


TYPES = {   'CAP': 'Capstone',
            'INT': 'Internship',
            'CMB': 'Combined',
            'MP': 'Master Project',
            'MT': 'Master Thesis',
        }

STATES = [('draft', 'Draft Proposal'), ('supervisor', 'Approved by The Supervisor'),
            ('ongoing', 'Approved by The Coordinator - Ongoing'),
            ('defense', 'Scheduled for Defense'), ('done', 'Completed')]
STATES_DICT = dict(STATES)

class Project(models.Model):
    _name = 'ixcapint.project'
    _inherit = ['ix.school.activity', 'ix.calendarized', 'mail.thread']
    _description = 'A capstone, internship, combined, master project or thesis'
    _sql_constraints = [('student_term_type_ukey', 'unique(student_id, term_id, type)', 'Project already exists')]

    name = fields.Char('Title', required=True, readonly=True,
                       states={'draft': [('readonly', False)]})

    student_id = fields.Many2one('ix.student', string='Student', required=True, readonly=True,
                                 default=lambda self: self.env['ix.student'].sudo().search(
                                     [('user_id', '=', self.env.user.id)]),
                                 states={'draft': [('readonly', False)]})

    type = fields.Selection([('CAP', 'Capstone'), ('INT',
                            'Internship'), ('CMB', 'Combined'),
                             ('MP', 'Master Project'), ('MT', 'Master Thesis')],
                            'Type', default='capstone', required=True,
                            readonly=True, states={'draft': [('readonly', False)]})

    code = fields.Char(compute='_compute_code', string='Code')

    @api.model
    def create(self, vals):
        project = super(Project, self).create(vals)
        project.message_subscribe([project.student_id.partner_id.id, project.supervisor_id.partner_id.id])
        return project

    @api.onchange('term_id', 'type')
    @api.depends('term_id', 'type')
    def _compute_code(self):
        for rec in self:
            if rec.state != 'draft':
                rec.code = rec.prefix + rec.type + '-' + rec.student_id.sid
            else:
                rec.code = ''

    supervisor_id = fields.Many2one('ix.faculty', string='Supervisor', required=True,
                                    default=lambda self: self.env['ix.faculty'].sudo().search(
                                        [('user_id', '=', self.env.user.id)]),
                                    readonly=True, states={'draft': [('readonly', False)]})

    cosupervisor_ids = fields.Many2many('ix.faculty', relation='ixcapint_project_cosupervisor_rel', string='Co-supervisors',                                    
                                    readonly=True, states={'draft': [('readonly', False)]})

    @api.onchange('student_id', 'supervisor_id')
    def _set_school(self):
        for rec in self:
            if rec.student_id:
                rec.school_id = rec.student_id.school_id
            elif rec.supervisor_id:
                rec.school_id = rec.supervisor_id.school_id
    
    is_supervisor = fields.Boolean(compute='_compute_is_supervisor', string='Supervisor?')
    is_cosupervisor = fields.Boolean(compute='_compute_is_cosupervisor', string='Co-supervisor?')
    
    @api.onchange('supervisor_id')
    @api.depends('supervisor_id')
    def _compute_is_supervisor(self):
        for rec in self:
            rec.is_supervisor = rec.supervisor_id.sudo().user_id == self.env.user

    @api.onchange('cosupervisor_ids')
    @api.depends('cosupervisor_ids')
    def _compute_is_cosupervisor(self):
        for rec in self:
            rec.is_cosupervisor = False
            for cosupervisor in rec.cosupervisor_ids:
                if cosupervisor.sudo().user_id == self.env.user:
                    rec.is_cosupervisor = True
                    break
    

    initial_idea = fields.Html(string='Initial Idea', required=True,
                               readonly=True, states={'draft': [('readonly', False)]})
    final_abstract = fields.Html(string='Final Abstract',
                                 readonly=True, states={'ongoing': [('readonly', False)], 'defense': [('readonly', False)]})

    tag_ids = fields.Many2many(
        comodel_name='ixcapint.tag', string='Keywords',
            readonly=True, states={'draft': [('readonly', False)]})

    diary_ids = fields.One2many(comodel_name='ixcapint.diary', inverse_name='project_id', string='Diaries')    

    internal_examiner_ids = fields.Many2many('ix.faculty', string='Internal Examiners',
                                readonly=True, states={'ongoing': [('readonly', False)]})

    external_examiner_ids = fields.Many2many('res.partner', string='External Examiners',
                                           readonly=True, states={'ongoing': [('readonly', False)]})

    evaluation_ids = fields.One2many('ixcapint.evaluation', 'project_id', 'Evaluations',
                                     readonly=True, states={'defense': [('readonly', False)]}, groups='ix.group_faculty,ixcapint.group_capint_coordinator')

    final_report = fields.Binary(string='Final Report')

    state = fields.Selection(STATES, string='State', default='draft', required=True, tracking=True)

    def supervisor_approve(self):
        self.ensure_one()
        state = self.state
        self.state = 'supervisor'
        self.message_post(body=f'State changed: {STATES_DICT[state]} --> {STATES_DICT[self.state]}')

    def coordinator_approve(self):
        self.ensure_one()
        state = self.state
        self.state = 'ongoing'
        self.message_post(body=f'State changed: {STATES_DICT[state]} --> {STATES_DICT[self.state]}')

    def schedule_defense(self):
        for rec in self:
            if not rec.start_time or not rec.end_time:
                raise ValidationError('Defense start time and end time must be set!')
            if (not rec.room_id or not rec.building_id) and not rec.videocall_location:
                raise ValidationError('Room and Building must be set, or at least the conference URL!')
            if not rec.internal_examiner_ids:
                raise ValidationError('At least, one internal examiner must be set!')
            if rec.type in ['MP', 'MT'] and not rec.external_examiner_ids:
                raise ValidationError('At least, one external examiner must be set!')
            
            attendee_ids = [internal_examiner.partner_id.id for internal_examiner in rec.internal_examiner_ids]
            rec.message_subscribe(attendee_ids)            

            attendee_ids.append(rec.supervisor_id.id)
            for external_examiner in rec.external_examiner_ids:
                attendee_ids.append(external_examiner.id)
            if self.env.user.partner_id.id not in attendee_ids:
                attendee_ids.append(self.env.user.partner_id.id)
            rec.set_event(rec.name, attendee_ids)
            rec.event_id.project_id = rec

            message = 'The defense of the ' + TYPES[rec.type] + ' ' + rec.name + ' by the student ' + rec.student_id.name + ' has been scheduled: ' + fields.Datetime.to_string(rec.start_time) + ' - ' + fields.Datetime.to_string(rec.end_time)
            message += '<br/>Supervisor: ' + rec.supervisor_id.name
            for internal_examiner in rec.internal_examiner_ids:
                message += '<br/>Internal Examiner: ' + internal_examiner.name
            for external_examiner in rec.external_examiner_ids:
                message += '<br/>External Examiner: ' + external_examiner.name
            rec.message_post(body=message)
        
        self.write({'state': 'defense'})

    def mark_done(self):
        self.write({'state': 'done'})
