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

class Lead(models.Model):
    _inherit = 'crm.lead'    
    
    institution_id = fields.Many2one(comodel_name='ixadmission.institution', string='Institution')
    education_system_id = fields.Many2one(comodel_name='ixadmission.education.system', related='institution_id.education_system_id', store=True)
    degree_id = fields.Many2one(comodel_name='ixadmission.degree', string='Degree')
    rx_date = fields.Date(string='Earned/Expected Date')
    