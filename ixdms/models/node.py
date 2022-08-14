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
from odoo.exceptions import AccessError, UserError


class Node(models.Model):
    _name = 'ixdms.node'
    _description = 'Node'
    _inherit = ['mail.thread', 'ix.expandable']
    _order = 'type,name'
    
    @api.constrains('name', 'parent_id', 'type', 'scope')
    def _check(self):        
        for rec in self:
            criteria = [('name', '=', rec.name), ('type', '=', rec.type), ('scope', '=', rec.scope)]
            if rec.parent_id:
                criteria.append(('parent_id', '=', rec.parent_id.id))
            else:
                criteria.append(('parent_id', '=', False))
            if self.search_count(criteria) > 1:
                if rec.scope == 'workspace' and not rec.parent_id:
                    message = 'Another workspace with the same name already exists!'
                elif rec.type == '1' and not rec.parent_id:
                    message = 'Another fodler with the same name already exists!'
                elif rec.type == '1':
                    message = 'Another fodler with the same name and location already exists!'
                else:
                    message = 'Another document with the same name and location already exists!'
                raise AccessError(message)

    name = fields.Char('Name', required=True)
    type = fields.Selection(string='Type', selection=[(
        '1', 'Folder'), ('2', 'Document')], default='2', required=True)
    scope = fields.Selection(string='Scope', selection=[('my', 'My'), ('share', 'Share'), ('workspace', 'Workspace')], default="my", required=True)
    active = fields.Boolean(default=True, tracking=True)    
    
    def deactivate(self):
        self.ensure_one()        
        for child in self.child_ids:
            child.deactivate()
        self.active = False
    
    def activate(self):
        if self.parent_id and not self.parent_id.active:
            raise UserError('You can\'t unarchive a folder or a document whose parent is archived!')
        self.active = True
        for child in self.child_ids:
            child.activate()

    scheduled_for_shredding = fields.Boolean(default=False, tracking=True)

    def schedule_for_shredding(self):
        self.ensure_one()
        if self.active:
            raise UserError('Can\'t schedule an active folder or document for shredding')
        for child in self.child_ids:
            child.schedule_for_shredding()
        self.scheduled_for_shredding = True

    def rescue(self):
        self.ensure_one()
        if self.parent_id and self.parent_id.scheduled_for_shredding:
            raise UserError('You can\'t rescue a folder or a document whose parent is scheduled for shredding!')
        self.scheduled_for_shredding = False
        for child in self.child_ids:
            child.rescue()


    tag_ids = fields.Many2many(comodel_name='ixdms.tag', string='Tags')
    ntags = fields.Integer(compute='_ntags')

    def _ntags(self):
        for rec in self:
            rec.ntags = len(rec.tag_ids)

    file = fields.Binary(string='File')
    url = fields.Char(string='URL')
    text = fields.Html(string='Text')
    parent_id = fields.Many2one(comodel_name='ixdms.node', string='Parent')
    child_ids = fields.One2many(
        comodel_name='ixdms.node', inverse_name='parent_id', string='Content')
    nchildren = fields.Integer(string='Sub-Folders', compute='_nchildren')

    def _nchildren(self):
        for rec in self:
            rec.nchildren = len(rec.child_ids)

    folder_ids = fields.One2many(comodel_name='ixdms.node', inverse_name='parent_id', domain=[
                                 ('type', '=', '1')], string='Sub-Folders')
    nfolders = fields.Integer(string='Sub-Folders', compute='_nfolders')

    def _nfolders(self):
        for rec in self:
            rec.nfolders = len(rec.folder_ids)

    document_ids = fields.One2many(comodel_name='ixdms.node', inverse_name='parent_id', domain=[
                                   ('type', '=', '2')], string='Documents')
    ndocuments = fields.Integer(string='Documents', compute='_ndocuments')

    def _ndocuments(self):
        for rec in self:
            rec.ndocuments = len(rec.document_ids)

    is_owner = fields.Boolean(compute='_is_owner')

    def _is_owner(self):
        for rec in self:
            rec.is_owner = rec.create_uid == self.env.user

    read_user_ids = fields.Many2many(
        comodel_name='res.users', relation='ixdms_read_node_user_rel', string='Read Access Users')
    write_user_ids = fields.Many2many(
        comodel_name='res.users', relation='ixdms_write_node_user_rel', string='Write Access Users')

    implied_read_user_ids = fields.Many2many(
        comodel_name='res.users', compute='_implied', string='Implied Read Access Users')
    implied_write_user_ids = fields.Many2many(
        comodel_name='res.users', compute='_implied', string='Implied Write Access Users')

    
    shared = fields.Boolean(compute='_implied')
    write_allowed = fields.Boolean(compute='_implied')

    def _implied(self):
        for rec in self:
            implied_read_user_ids = []
            implied_write_user_ids = []            
            shared = False

            rec._rec_implied(implied_read_user_ids, implied_write_user_ids)

            if len(implied_read_user_ids) > 0:
                rec.implied_read_user_ids = implied_read_user_ids
                shared = True
            else:
                rec.implied_read_user_ids = False
            if len(implied_write_user_ids) > 0:
                rec.implied_write_user_ids = implied_write_user_ids
                shared = True
            else:
                rec.implied_write_user_ids = False            
            
            rec.shared = shared or len(rec.read_user_ids) > 0 or len(rec.write_user_ids) > 0 or len(
                rec.student_share_ids) > 0 or len(rec.faculty_share_ids) > 0
            rec.write_allowed = self.env.user == rec.create_uid or self.env.user in rec.write_user_ids or self.env.user in rec.implied_write_user_ids            
            

    def _rec_implied(self, implied_read_user_ids, implied_write_user_ids):
        if not self.parent_id:
            return

        try:
            self.parent_id.read_user_ids
        except AccessError:
            return

        for read_user in self.parent_id.read_user_ids:
            if read_user.id not in implied_read_user_ids:
                implied_read_user_ids.append(read_user.id)

        for write_user in self.parent_id.write_user_ids:
            if write_user.id not in implied_write_user_ids:
                implied_write_user_ids.append(write_user.id)

        return self.parent_id._rec_implied(implied_read_user_ids, implied_write_user_ids)

    
    def open(self):
        self.ensure_one()
        domain = [('id', '=', self.id)]
        context = {'default_parent_id': self.id}        
        if self.type == '2':
            context.update({'create': False})
        return self._expand_to('ixdms.action_node_open', domain, context, self.id)

    def move_up(self):
        self.ensure_one()
        if self.parent_id and self.parent_id.scope not in ['share', 'workspace']:
            self.parent_id = self.parent_id.parent_id
    
    def cut(self):
        self.ensure_one()
        rec = self.env['ixdms.clipboard'].search([('create_uid', '=', self.env.user.id)])
        if rec:
            rec.write({
                'node_id': self.id,    
                'processed': False
            })
        else:
            self.env['ixdms.clipboard'].create({'node_id': self.id})

    
    def paste(self):
        self.ensure_one()
        rec = self.env['ixdms.clipboard'].search([('create_uid', '=', self.env.user.id), ('processed', '=', False)])
        if not rec:
            raise UserError('Nothing to paste!')
        walker = self
        while walker and walker.id != rec.node_id.id:
            walker = walker.parent_id
        if walker:
            raise UserError('Can\'t be passed here!')
        
        rec.node_id.parent_id = self
        rec.processed = True

    channel_id = fields.Many2one(comodel_name='mail.channel', string='Channel')

    def get_channel(self):
        self.ensure_one()
        if not self.channel_id:
            self.channel_id = self.sudo().env['mail.channel'].create({'name': self.name, 'public': 'private'})
        return {
            'type': 'ir.actions.act_url',
            'target': 'new',
            'url': f'/chat/{self.channel_id.id}/{self.channel_id.uuid}',
        }
    