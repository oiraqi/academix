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


class SDGoal(models.Model):
    _name='ixperformance.sd.goal'
    _inherit = 'ixperformance.goal'
    _description = 'An SD goal to set and achieve in a given evaluation process'
    _sql_constraints = [('process_id_kpi_ukey', 'unique(process_id,kpi)', 'Goal already set for this evaluation process')]

    kpi = fields.Selection([('ca_number', 'Number of Significant Committee Activities'),
                            ('pd_number', 'Number of Professional Development Activities'),
                            ('sr_number', 'Number of Services')], 'KPI', required=True)
