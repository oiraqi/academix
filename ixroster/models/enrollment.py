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

class Enrollment(models.Model):
    _name = 'ixroster.enrollment'
    _inherit = 'mail.thread'
    _description = 'Enrollment'
    _sql_constraints = [('student_section_ukey', 'unique(student_id, section_id)',
                         'Student already enrolled in this section')]
    _order = 'section_id,state,student_id'

    name = fields.Char('Name', compute='_set_name')
    student_id = fields.Many2one(
        comodel_name='ix.student', string='Student', required=True)
    section_id = fields.Many2one(
        comodel_name='ixroster.section', string='Section', required=True)
    state = fields.Selection(string='State', selection=[('created', 'Created'), ('enrolled', 'Enrolled'),
                                                        ('dropped', 'Dropped'), ('withdrawn', 'Withdrawn'), ('completed', 'Completed')], default='created', required=True, tracking=True)
    dstate = fields.Selection(string='Drop State', selection=[(
        'draft', 'Draft'), ('confirmed', 'Confirmed')], default='draft')
    dtriggered = fields.Boolean(default=False)
    can_drop = fields.Boolean(compute='_can_drop_withdraw')
    wstate = fields.Selection(string='W State', selection=[('draft', 'Draft'), ('wreq', 'Request To Withdraw'), (
        'wadv', 'W Approved by Advisor'), ('winst', 'W Approved by Instructor')], default='draft', tracking=True)
    wtriggered = fields.Boolean(default=False)
    can_withdraw = fields.Boolean(compute='_can_drop_withdraw')
    wfstate = fields.Selection(string='WF State', selection=[('draft', 'Draft'), ('wfreq', 'WF Request'), ('wfdean', 'WF Approved by the Dean/Director'), ('wfreg', 'WF Processed')],
                               default='draft', tracking=True)
    wftriggered = fields.Boolean(default=False)
    wpstate = fields.Selection(string='WP State', selection=[('draft', 'Draft'), ('wpreq', 'WP Request'), ('wpdean', 'WP Approved by the Dean/Director'), ('wpreg', 'WP Processed')],
                               default='draft', tracking=True)
    wptriggered = fields.Boolean(default=False)
    ipstate = fields.Selection(string='IP State', selection=[('draft', 'Draft'), ('ipreq', 'IP Request'), ('ipdean', 'IP Approved by the Dean/Director'), ('ipreg', 'IP Processed')],
                               default='draft', tracking=True)
    iptriggered = fields.Boolean(default=False)
    wdtime = fields.Datetime()

    def _can_drop_withdraw(self):
        current_term = self.env['ix.term'].get_current()
        if not current_term:
            self.write({'can_drop': False, 'can_withdraw': False})
            return
        
        add_drop = self.env['calendar.event'].search([('term_id', '=', current_term.id), ('meta', '=', 'add_drop')])
        if not add_drop:
            self.write({'can_drop': False, 'can_withdraw': False})
            return
        today = fields.Date.today()
        if today >= add_drop.start_date and today <= add_drop.stop_date:
            self.write({'can_drop': True, 'can_withdraw': False})
        else:
            withdraw = self.env['calendar.event'].search([('term_id', '=', current_term.id), ('meta', '=', 'w')])
            if not withdraw or today <= add_drop.stop_date or today > withdraw.stop_date:
                self.write({'can_drop': False, 'can_withdraw': False})
            else:
                self.write({'can_drop': False, 'can_withdraw': True})            

    # Related fields
    school_id = fields.Many2one(
        comodel_name='ix.school', string='School', related='section_id.school_id', store=True)
    discipline_id = fields.Many2one(comodel_name='ix.discipline', string='Discipline',
                                    related='section_id.course_id.discipline_id', store=True)
    course_id = fields.Many2one(
        comodel_name='ix.course', string='Course', related='section_id.course_id', store=True)
    instructor_id = fields.Many2one(
        comodel_name='ix.faculty', string='Instructor', related='section_id.instructor_id', store=True)
    term_id = fields.Many2one(
        comodel_name='ix.term', string='Term', related='section_id.term_id', store=True)
    sid = fields.Char(related="student_id.sid")
    program_id = fields.Many2one(
        comodel_name='ixcatalog.program', related='student_id.program_id', store=True)
    attendance_mode = fields.Selection(related='student_id.attendance_mode')
    email = fields.Char(related='student_id.email')
    timeslot = fields.Char('Timeslot', related='section_id.timeslot')
    room_id = fields.Many2one('ix.room', related='section_id.room_id')            

    @api.constrains('student_id', 'section_id')
    def _check_student_section(self):
        for rec in self:
            if rec.state != 'created':
                raise ValidationError(
                    'Can\'t change a student/section mapping once enrolled!')

            if rec.student_id and rec.section_id:
                # From a performance perspective, we should start with the cheap is_open check,
                # then the time conflict check, and only then, the prerequisites check.
                # However, for a more pertinent feedback to the user, we deem it's worth it to start
                # with the more expensive prerequisites and corequisites check.
                self.env['ixroster.enrollment'].check_prerequisites(
                    rec.student_id, rec.section_id.course_id)
                self.env['ixroster.enrollment'].check_corequisites(
                    rec.student_id, rec.section_id.course_id)
                if not rec.section_id.is_open:
                    raise ValidationError('Section closed!')
                self.env['ixroster.enrollment'].check_time_conflict(
                    rec.student_id, rec.section_id)

    @api.model
    def check_prerequisites(self, student, course):
        # Template method. Will be overriden in ixlms
        return

    @api.model
    def check_corequisites(self, student, course):
        fulfilled = False
        for corequisite in course.corequisite_ids:
            if self.search([('student_id', '=', student.id), ('section_id.course_id', '=', corequisite.corequisite_id.id), ('state', 'in', ['enrolled', 'completed'])]):
                fulfilled = True
                break
            if not fulfilled:            
                raise ValidationError('Unfulfilled corequisite: ' + corequisite.corequisite_id.name)

    @api.model
    def check_time_conflict(self, student, section):
        current_enrollments = self.search([('student_id', '=', student.id), (
            'term_id', '=', section.term_id.id), ('state', '=', 'enrolled')])
        for enrollment in current_enrollments:
            if (section.monday == enrollment.section_id.monday or \
                section.tuesday == enrollment.section_id.tuesday or \
                section.wednesday == enrollment.section_id.wednesday or \
                section.thursday == enrollment.section_id.thursday or \
                section.friday == enrollment.section_id.friday) and \
                section.start_timeslot <= enrollment.section_id.end_timeslot and \
                section.end_timeslot >= enrollment.section_id.start_timeslot:
                raise ValidationError(
                    'Time Conflict with ' + enrollment.section_id.name + ': ' + enrollment.section_id.timeslot)

    @api.onchange('student_id', 'section_id')
    def _set_name(self):
        for rec in self:
            if rec.student_id and rec.section_id:
                rec.name = rec.student_id.name + ' / ' + rec.section_id.name
            else:
                rec.name = ''

    def enroll(self):
        if self.state == 'created':
            self.state = 'enrolled'

    def drop(self):        
        self.dtriggered = True

    def req_w(self):
        self.wtriggered = True

    def file_wp(self):
        self.wptriggered = True

    def file_wf(self):
        self.wftriggered = True

    def file_ip(self):
        self.iptriggered = True

    def confirm_drop(self):
        self.write({'stae': 'dropped', 'wdtime': fields.Datetime.now()})

    def cancel_drop(self):
        self.dtriggered = False

    def confirm_wrequest(self):
        self.wstate = 'wreq'

    def cancel_wrequest(self):
        self.wtriggered = False

    def app_w_adv(self):
		# Declare it here. Overwritten by the Advising module
        return

    def app_w_ins(self):
        # Don't trust the interface, perform the server-side check!
        # If someone is playing with us, drop silently
        if self.env.ref('ix.group_faculty') in self.env.user.groups_id and self.section_id.instructor_id.user_id == self.env.user:
            self.write({
                'wstate': 'winst',
                'state': 'withdrawn',
                'wdtime': fields.Datetime.now()
            })

    def confirm_wprequest(self):
        # Don't trust the interface, perform the server-side check!
        # If someone is playing with us, drop silently
        if self.env.ref('ix.group_faculty') in self.env.user.groups_id and self.section_id.instructor_id.user_id == self.env.user:
            self.wpstate = 'wpreq'

    def cancel_wprequest(self):
        self.wptriggered = False

    def app_wp_dean(self):
        # Don't trust the interface, perform the server-side check!
        # If someone is playing with us, drop silently
        if self.env.ref('ix.group_dean') in self.env.user.groups_id and self.section_id.school_id.dean_id.user_id == self.env.user:
            self.wpstate = 'wpdean'

    def app_wp_reg(self):
        # Don't trust the interface, perform the server-side check!
        # If someone is playing with us, drop silently
        if self.env.ref('ixroster.group_registrar') in self.env.user.groups_id:
            self.write({
                'wpstate': 'wpreg',
                'state': 'withdrawn',
                'wdtime': fields.Datetime.now()
            })

    def confirm_wfrequest(self):
        # Don't trust the interface, perform the server-side check!
        # If someone is playing with us, drop silently
        if self.env.ref('ix.group_faculty') in self.env.user.groups_id and self.section_id.instructor_id.user_id == self.env.user:
            self.wfstate = 'wfreq'

    def cancel_wfrequest(self):
        self.wftriggered = False

    def app_wf_dean(self):
        # Don't trust the interface, perform the server-side check!
        # If someone is playing with us, drop silently
        if self.env.ref('ix.group_dean') in self.env.user.groups_id and self.section_id.school_id.dean_id.user_id == self.env.user:
            self.wfstate = 'wfdean'

    def app_wf_reg(self):
        # Don't trust the interface, perform the server-side check!
        # If someone is playing with us, drop silently
        if self.env.ref('ixroster.group_registrar') in self.env.user.groups_id:
            self.write({
                'wfstate': 'wfreg',
                'state': 'withdrawn',
                'wdtime': fields.Datetime.now()
            })

    def confirm_iprequest(self):
        # Don't trust the interface, perform the server-side check!
        # If someone is playing with us, drop silently
        if self.env.ref('ix.group_faculty') in self.env.user.groups_id and self.section_id.instructor_id.user_id == self.env.user:
            self.ipstate = 'ipreq'

    def cancel_iprequest(self):
        self.iptriggered = False

    def app_ip_dean(self):
        # Don't trust the interface, perform the server-side check!
        # If someone is playing with us, drop silently
        if self.env.ref('ix.group_dean') in self.env.user.groups_id and self.section_id.school_id.dean_id.user_id == self.env.user:
            self.ipstate = 'ipdean'

    def app_ip_reg(self):
        # Don't trust the interface, perform the server-side check!
        # If someone is playing with us, drop silently
        if self.env.ref('ixroster.group_registrar') in self.env.user.groups_id:
            self.write({
                'ipstate': 'ipreg',
                'state': 'withdrawn',
                'wdtime': fields.Datetime.now()
            })
