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

class LmsAssessment(models.Model):
    _inherit = 'ixlms.assessment'

    course_ilo_ids = fields.One2many('ixcatalog.course.ilo', related='course_id.ilo_ids')
    ilo_ids = fields.Many2many(comodel_name='ixcatalog.course.ilo', string='Assessed ILOs')

    good_performance = fields.Binary(string='Good Performance')
    avg_performance = fields.Binary(string='Avg. Performance')
    poor_performance = fields.Binary(string='Poor Performance')

    def get_ilo_achievement(self):
        self.ensure_one()
        domain = [('assessment_id', '=', self.id)]        
        return self._expand_to('ixquality.action_assessed_ilo', domain)