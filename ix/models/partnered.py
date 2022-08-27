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
import string


class Partnered(models.AbstractModel):
    _name = 'ix.partnered'
    _inherits = {'res.partner': 'partner_id'}

    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    firstname = fields.Char(string='First Name', required=True)
    lastname = fields.Char(string='Last Name', required=True)

    @api.onchange('firstname')
    @api.depends('firstname')
    def _firstname(self):
        for rec in self:
            if rec.firstname:
                firstname = string.capwords(rec.firstname.strip())
                if rec.firstname != firstname:
                    rec.firstname = firstname

    @api.onchange('lastname')
    @api.depends('lastname')
    def _lastname(self):
        for rec in self:
            if rec.lastname:
                lastname = string.capwords(rec.lastname.strip())
                if rec.lastname != lastname:
                    rec.lastname = lastname
    
    @api.onchange('firstname', 'lastname')
    @api.depends('firstname', 'lastname')
    def _update_name(self):
        for rec in self:
            if rec.firstname and rec.lastname:
                rec.name = string.capwords(rec.lastname.strip()) + ', ' + string.capwords(rec.firstname.strip())
 