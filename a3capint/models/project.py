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
TYPES = {   'CAP': 'Capstone',
            'INT': 'Internship',
            'CMB': 'Combined',
            'MP': 'Master Project',
            'MT': 'Master Thesis',
        }


class Project(models.Model):
    _name = 'a3capint.project'
    _inherit = ['a3.school.activity', 'a3.calendarized', 'mail.thread']
    _description = 'A capstone, internship, combined, master project or thesis'
    _sql_constraints = [('student_year_semester_type_ukey', 'unique(student_id, year, semester, type)', 'Project already exists')]

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

    @api.model
    def create(self, vals):
        project = super(Project, self).create(vals)
        project.message_subscribe([project.student_id.partner_id.id, project.supervisor_id.partner_id.id])
        return project

    @api.onchange('year', 'semester', 'type')
    @api.depends('year', 'semester', 'type')
    def _compute_code(self):
        for rec in self:
            if rec.state != 'draft':
                rec.code = rec.prefix + rec.type + '-' + rec.student_id.sid
            else:
                rec.code = ''

    supervisor_id = fields.Many2one('a3.faculty', string='Supervisor', required=True,
                                    default=lambda self: self.env['a3.faculty'].search(
                                        [('user_id', '=', self.env.user.id)]),
                                    readonly=True, states={'draft': [('readonly', False)]})

    @api.onchange('student_id', 'supervisor_id')
    def _set_school(self):
        for rec in self:
            if rec.student_id:
                rec.school_id = rec.student_id.school_id
            elif rec.supervisor_id:
                rec.school_id = rec.supervisor_id.school_id
    
    is_supervisor = fields.Boolean(compute='_compute_is_supervisor', string='Supervisor?')
    
    @api.onchange('supervisor_id')
    @api.depends('supervisor_id')
    def _compute_is_supervisor(self):
        for rec in self:
            rec.is_supervisor = rec.supervisor_id.user_id == self.env.user
    

    initial_idea = fields.Html(string='Initial Idea', required=True,
                               readonly=True, states={'draft': [('readonly', False)]})
    final_abstract = fields.Html(string='Final Abstract',
                                 readonly=True, states={'ongoing': [('readonly', False)], 'defense': [('readonly', False)]})

    tag_ids = fields.Many2many(
        comodel_name='a3capint.tag', string='Keywords', required=True)

    internal_examiner_ids = fields.Many2many('a3.faculty', string='Internal Examiners',
                                readonly=True, states={'ongoing': [('readonly', False)]})

    external_examiner_ids = fields.Many2many('res.partner', string='External Examiners',
                                           readonly=True, states={'ongoing': [('readonly', False)]})

    evaluation_ids = fields.One2many('a3capint.evaluation', 'project_id', 'Evaluations',
                                     readonly=True, states={'defense': [('readonly', False)]})

    final_report = fields.Binary(string='Final Report')

    state = fields.Selection([
        ('draft', 'Draft Proposal'), ('supervisor', 'Approved by The Supervisor'),
        ('ongoing', 'Approved by The Coordinator - Ongoing'), ('defense',
                                                               'Scheduled for Defense'), ('done', 'Completed')
    ], string='State', default='draft', required=True, tracking=True)

    def supervisor_approve(self):
        self.write({'state': 'supervisor'})

    def coordinator_approve(self):
        self.write({'state': 'ongoing'})

    def schedule_defense(self):
        for rec in self:
            if not rec.start_time or not rec.end_time:
                raise ValidationError('Start Time and End Time must be set!')
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
            attendee_ids.append(self.env.user.partner_id.id)
            rec.set_event(rec.name, rec.start_time, rec.end_time, rec.room_id.name, False, [(6, 0, attendee_ids)])
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
