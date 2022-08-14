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

class LmsAssessmentLine(models.Model):
    _inherit = 'ixlms.assessment.line'

    assessed_ilo_ids = fields.One2many(comodel_name='ixquality.assessed.ilo', inverse_name='assessment_line_id', string='Assessed ILOs')

    def create_assessed_ilos(self):
        self.ensure_one()
        assessed_ilo_ids = [assessed_ilo_id.ilo_id.id for assessed_ilo_id in self.assessed_ilo_ids]
        for ilo in self.assessment_id.ilo_ids:
            if ilo.id not in assessed_ilo_ids:
                self.env['ixquality.assessed.ilo'].create({            
                    'assessment_line_id': self.id,
                    'ilo_id': ilo.id,
                })

    