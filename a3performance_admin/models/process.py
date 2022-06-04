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

from odoo import models, fields
from datetime import date


class Process(models.Model):
    _inherit = 'a3performance.eval.process'
    
    committee_state_datetime = fields.Datetime()

    # Committee section
    committee_recommendation = fields.Selection(
        [('promote', 'Promote'), ('not_promote', "Don't promote")], 'Recommendation',
        readonly=True, states={'committee': [('readonly', False)]},
        groups='a3.group_committee_member,a3.group_dean,a3.group_vpaa')
    committee_feedback = fields.Html("Feedback",
                                     readonly=True, states={'committee': [('readonly', False)]},
                                     groups='a3.group_committee_member,a3.group_dean,a3.group_vpaa')

    # Dean section
    dean_recommendation = fields.Selection(
        [('promote', 'Promote'), ('not_promote', "Don't promote")], 'Recommendation',
        readonly=True, states={'dean': [('readonly', False)]},
        groups='a3.group_dean,a3.group_vpaa')
    dean_new_rank = fields.Selection([('D', 'Lecturer'), ('C', 'Assistant Professor'), (
        'B', 'Associate Professor'), ('A', 'Full Professor')], 'New Rank',
        readonly=True, states={'dean': [('readonly', False)]},
        attrs="{'invisible': [('dean_recommendation', '=', 'not_promote')], 'required': [('dean_recommendation', '=', 'promote')]}",
        groups='a3.group_dean,a3.group_vpaa')
    dean_new_srank_id = fields.Many2one('a3performance.srank', string='New Sub-Rank',
                                        readonly=True, states={'dean': [('readonly', False)]},
                                        attrs="{'invisible': [('dean_recommendation', '=', 'not_promote')], 'required': [('dean_recommendation', '=', 'promote')]}",
                                        groups='a3.group_dean,a3.group_vpaa')
    dean_feedback = fields.Html("Feedback",
                                readonly=True, states={'dean': [('readonly', False)]},
                                groups='a3.group_dean,a3.group_vpaa')

    # VPAA section
    vpaa_decision = fields.Selection(
        [('promote', 'Promote'), ('not_promote', "Don't promote")], 'Decision',
        readonly=True, states={'vpaa': [('readonly', False)]})
    vpaa_new_rank = fields.Selection([('D', 'Lecturer'), ('C', 'Assistant Professor'), (
        'B', 'Associate Professor'), ('A', 'Full Professor')], 'New Rank',
        readonly=True, states={'vpaa': [('readonly', False)]},
        attrs="{'invisible': [('vpaa_decision', '=', 'not_promote')], 'required': [('vpaa_decision', '=', 'promote')]}")
    vpaa_new_srank_id = fields.Many2one('a3performance.srank', string='New Sub-Rank',
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
