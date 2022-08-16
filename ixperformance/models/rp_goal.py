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

from odoo import models, fields


class RPGoal(models.Model):
    _name = 'ixperformance.rp.goal'
    _inherit = 'ixperformance.goal'
    _description = 'An RP goal to set and achieve in a given evaluation process'
    _sql_constraints = [('process_id_kpi_ukey', 'unique(process_id,kpi)', 'Goal already set for this evaluation process')]

    kpi = fields.Selection([('ar_imp_number', 'Number of Impact Factor Journal Articles'),
                            ('ar_idx_number', 'Number of Indexed Journal Articles'),
                            ('bk_number', 'Number of Books'),
                            ('ch_number', 'Number of Book Chapters'),
                            ('cp_number', 'Number of Papers in Proceedings'),
                            ('pr_number', 'Number of Presentations'),
                            ('sp_number', 'Number of Supervised PhD Theses'),
                            ('sm_number', 'Number of Supervised Master Projects/Theses')], 'KPI', required=True)
