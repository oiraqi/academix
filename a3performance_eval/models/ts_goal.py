# -*- coding: utf-8 -*-
###############################################################################
#
#    Al Akhawayn University in Ifrane -- AUI
#    Copyright (C) 2022-TODAY AUI(<http://www.a3ma>).
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


class TSGoal(models.Model):
    _name='a3performance.eval.ts.goal'
    _inherit = 'a3performance.eval.goal'
    _description = 'A TS goal to set and achieve in a given evaluation process'
    _sql_constraints = [('a3performance.eval.ts_goal_process_id_kpi_ukey', 'unique(process_id,kpi)', 'Goal already set for this evaluation process')]

    process_id = fields.Many2one('a3performance.eval.process', string='TS Process', required=True)
    kpi = fields.Selection([('se_avg_score', 'Average Student Evaluation Score / 100'),
                            ('se_wavg_score', 'Weighted Average Student Evaluation Score / 100'),
                            ('se_prc_4', 'Percentage of Student Evaluation Scores >= 4'),
                            ('se_prc_45', 'Percentage of Student Evaluation Scores >= 4.5'),
                            ('co_number', 'Number of Classroom Observations'),
                            ('ac_number', 'Number of Actions'),
                            ('sp_number', 'Number of Supervised Projects')], 'KPI', required=True)
