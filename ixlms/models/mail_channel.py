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

class MailChannel(models.Model):
    _inherit = 'mail.channel'

    cname = fields.Char(string='Channel Name')    
    lms_course_id = fields.Many2one(comodel_name='ixlms.course', string='LMS Course')    

    @api.onchange('cname', 'lms_course_id')
    def _cname(self):
        for rec in self:
            if rec.lms_course_id and rec.lms_course_id.name and rec.cname:
                rec.name = rec.lms_course_id.name
                if rec.cname:
                    rec.name += '-' + rec.cname

    def ix_channel_open(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_url',
            'target': 'new',
            'url': f'/chat/{self.id}/{self.uuid}',
        }