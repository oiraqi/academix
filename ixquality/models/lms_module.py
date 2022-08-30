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

class LmsModule(models.Model):
    _inherit = 'ixlms.module'

    lms_course_ilo_ids = fields.Many2many(comodel_name='ixlms.course.ilo', compute='_ilo_ids', string='Covered ILOs')

    @api.onchange('chapter_ids')
    def _ilo_ids(self):
        for rec in self:
            ilos = []
            for chapter in rec.chapter_ids:
                for ilo in chapter.lms_course_ilo_ids:
                    if ilo.id not in ilos:
                        ilos.append(ilo.id)
            if len(ilos) > 0:
                rec.lms_course_ilo_ids = ilos                
            else:
                rec.lms_course_ilo_ids = False
    