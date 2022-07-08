# -*- coding: utf-8 -*-
###############################################################################
#
#    Al Akhawayn University in Ifrane -- AUI
#    Copyright (C) 2022-TODAY AUI(<http://www.ixma>).
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
from odoo.exceptions import UserError
from datetime import date

class Process(models.Model):
    _name = 'ixperformance.process'
    _description = 'Evaluation Process'
    _inherit = ['ix.faculty.owned', 'mail.thread']
    _order = 'from_year,from_sequence'
    _sql_constraints = [('from_to_ukey', 'unique(from_term_id, to_term_id)', 'An evaluation process for the selected period already exists')]

    name = fields.Char('Evaluation Process', compute='_set_name', store=True)
    hiring_date = fields.Date(related='faculty_id.hiring_date')
    rank = fields.Selection([('D', 'Lecturer'), ('C', 'Assistant Professor'), (
        'B', 'Associate Professor'), ('A', 'Full Professor')], 'Rank', default=lambda self: self.env['ix.faculty'].search(
            [('partner_id', '=', self.env.user.partner_id.id)]).rank, required=True)

    @api.onchange('rank')
    def _onchange_rank(self):
        for rec in self:
            if rec.rank:
                records = self.env['ixperformance.srank'].search([('rank', '=', rec.rank)])
                if records:
                    rec.srank_id = records[0]
                else:
                    rec.srank_id = False
            else:
                rec.srank_id = False

    srank_id = fields.Many2one('ixperformance.srank', string='Sub-Rank', default=lambda self: self.env['ix.faculty'].search(
            [('partner_id', '=', self.env.user.partner_id.id)]).srank_id, required=True)
    state = fields.Selection([('faculty', 'Faculty'), ('f2c', 'Submitted'),
                             ('committee', 'Committee'), ('c2d',
                              'Submitted'), ('dean', 'Dean / Director'),
                             ('d2v', 'Submitted'), ('vpaa', 'VPAA'), ('done', 'Done')],
                             'Progress', default='faculty', required=True, tracking=True)
    type = fields.Selection(
        [('srank', 'Sub-Rank'), ('rank', 'Rank')], 'Evaluation Type', default='srank', required=True,
        readonly=True, states={'faculty': [('readonly', False)]})
    from_term_id = fields.One2many('ix.term', 'From Term', required=True,
                               readonly=True, states={'faculty': [('readonly', False)]})
    from_year = fields.Integer(related='from_term_id.year', store=True)
    from_sequence = fields.Integer(related='from_term_id.session_id.sequence', store=True)
    
    to_term_id = fields.One2many('ix.term', 'To Term', required=True,
                               readonly=True, states={'faculty': [('readonly', False)]})
    period = fields.Char('Period under Evaluation', compute='_set_name')
    previous_process_id = fields.Many2one('ixperformance.process', string='Previous Evaluation', compute='_previous_process_id')

    def _previous_process_id(self):
        for rec in self:
            records = self.env['ixperformance.process'].search([('faculty_id.user_id', '=', self.env.user.id), ('state', '=', 'done')], order='from_year desc,from_sequence desc')
            if records:
                rec.previous_process_id = records[0]
            else:
                rec.previous_process_id = False

    overall_self_evaluation = fields.Html('Overall Self-Evaluation',
                                  readonly=True, states={'faculty': [('readonly', False)]})

     
    @api.constrains('from_term_id', 'to_term_id')
    def _check_period(self):
        for rec in self:
            if rec.from_term_id.year > rec.to_term_id.year or (rec.from_term_id.year == rec.to_term_id.year and rec.from_term_id.sequence > rec.to_term_id.sequence):
                raise UserError(
                    'From Term should be before To Term')

    @api.depends('from_term_id', 'to_term_id')
    @api.onchange('from_term_id', 'to_term_id')
    def _set_name(self):
        for rec in self:
            if rec.from_term_id and rec.to_term_id:
                rec.period = rec.from_term_id.code + '-' + rec.to_term_id.code
                rec.name = rec.period + '-' + 'Eval'
                if rec.faculty_id:
                    rec.name += ' - ' + rec.faculty_id.name
            else:
                rec.period = ''
                rec.name = ''    
    
    # Committee section
    committee_state_datetime = fields.Datetime()    
    committee_recommendation = fields.Selection(
        [('promote', 'Promote'), ('not_promote', "Don't promote")], 'Recommendation',
        readonly=True, states={'committee': [('readonly', False)]},
        groups='ixperformance.group_committee_member,ix.group_dean,ix.group_vpaa')
    committee_feedback = fields.Html("Feedback",
                                     readonly=True, states={'committee': [('readonly', False)]},
                                     groups='ixperformance.group_committee_member,ix.group_dean,ix.group_vpaa')

    # Dean section
    dean_recommendation = fields.Selection(
        [('promote', 'Promote'), ('not_promote', "Don't promote")], 'Recommendation',
        readonly=True, states={'dean': [('readonly', False)]},
        groups='ix.group_dean,ix.group_vpaa')
    dean_new_rank = fields.Selection([('D', 'Lecturer'), ('C', 'Assistant Professor'), (
        'B', 'Associate Professor'), ('A', 'Full Professor')], 'New Rank',
        readonly=True, states={'dean': [('readonly', False)]},
        attrs="{'invisible': [('dean_recommendation', '=', 'not_promote')], 'required': [('dean_recommendation', '=', 'promote')]}",
        groups='ix.group_dean,ix.group_vpaa')
    dean_new_srank_id = fields.Many2one('ixperformance.srank', string='New Sub-Rank',
                                        readonly=True, states={'dean': [('readonly', False)]},
                                        attrs="{'invisible': [('dean_recommendation', '=', 'not_promote')], 'required': [('dean_recommendation', '=', 'promote')]}",
                                        groups='ix.group_dean,ix.group_vpaa')
    dean_feedback = fields.Html("Feedback",
                                readonly=True, states={'dean': [('readonly', False)]},
                                groups='ix.group_dean,ix.group_vpaa')

    # VPAA section
    vpaa_decision = fields.Selection(
        [('promote', 'Promote'), ('not_promote', "Don't promote")], 'Decision',
        readonly=True, states={'vpaa': [('readonly', False)]})
    vpaa_new_rank = fields.Selection([('D', 'Lecturer'), ('C', 'Assistant Professor'), (
        'B', 'Associate Professor'), ('A', 'Full Professor')], 'New Rank',
        readonly=True, states={'vpaa': [('readonly', False)]},
        attrs="{'invisible': [('vpaa_decision', '=', 'not_promote')], 'required': [('vpaa_decision', '=', 'promote')]}")
    vpaa_new_srank_id = fields.Many2one('ixperformance.srank', string='New Sub-Rank',
                                        readonly=True, states={'vpaa': [('readonly', False)]},
                                        attrs="{'invisible': [('vpaa_decision', '=', 'not_promote')], 'required': [('vpaa_decision', '=', 'promote')]}")
    vpaa_feedback = fields.Html("Feedback",
                                readonly=True, states={'vpaa': [('readonly', False)]})

    
    # Workflow section
    def faculty_to_f2c(self):
        self.write({'state': 'f2c'})

    def f2c_to_faculty(self):
        self.write({'state': 'faculty'})

    def f2c_to_committee(self):
        self.ensure_one()
        self.write(
            {'state': 'committee', 'committee_state_date': fields.Datetime.now()})

    def committee_to_f2c(self):
        self.ensure_one()
        self.write({'state': 'f2c'})

    def committee_to_c2d(self):
        self.write({'state': 'c2d'})

    def c2d_to_committee(self):
        self.write({'state': 'committee'})

    def c2d_to_dean(self):
        # verify all required fields, e.g., committee feedback, have been filled
        self.write({'state': 'dean'})

    def dean_to_c2d(self):
        self.write({'state': 'c2d'})

    def dean_to_d2v(self):
        # verify all required fields, e.g., dean_new_srank_id or dean_new_rank, have been filled
        self.write({'state': 'd2v'})

    def d2v_to_dean(self):
        self.write({'state': 'dean'})

    def d2v_to_vpaa(self):
        self.write({'state': 'vpaa'})

    def vpaa_to_d2v(self):
        self.write({'state': 'd2v'})

    def vpaa_to_done(self):
        # verify all required fields, e.g., dean_new_srank_id or dean_new_rank, have been filled
        self.ensure_one()
        self.write({'state': 'done'})
    