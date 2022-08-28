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
from odoo.exceptions import ValidationError
import string


class Partnered(models.AbstractModel):
    _name = 'ix.partnered'
    _inherits = {'res.partner': 'partner_id'}

    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    firstname = fields.Char(string='First Name')
    lastname = fields.Char(string='Last Name')

    @api.constrains('name')
    def _check_name(self):
        for rec in self:
            if not rec.name or len(rec.name.split(', ')) != 2:
                raise ValidationError('Name shall be formatted as: Lastname, Firstname')

    @api.onchange('name')
    @api.depends('name')
    def _update_firstname_lastname(self):
        for rec in self:
            if rec.name:
                last_first = rec.name.split(',')
                if len(last_first) != 2:
                    raise ValidationError('Name shall be formatted as: Lastname, Firstname')
                
                lastname = string.capwords(last_first[0].strip())
                firstname = string.capwords(last_first[1].strip())
                name = lastname + ', ' + firstname
                if rec.name != name:
                    rec.name = name
                if rec.firstname != firstname:
                    rec.firstname = firstname
                if rec.lastname != lastname:
                    rec.lastname = lastname
    
    @api.onchange('firstname', 'lastname')
    @api.depends('firstname', 'lastname')
    def _update_name(self):
        for rec in self:
            if rec.firstname:
                firstname = string.capwords(rec.firstname.strip())
                if rec.firstname != firstname:
                    rec.firstname = firstname
            if rec.lastname:
                lastname = string.capwords(rec.lastname.strip())
                if rec.lastname != lastname:
                    rec.lastname = lastname
            if rec.firstname and rec.lastname:
                name = string.capwords(rec.lastname.strip()) + ', ' + string.capwords(rec.firstname.strip())
                if rec.name != name:
                    rec.name = name
 