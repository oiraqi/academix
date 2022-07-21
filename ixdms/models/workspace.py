from odoo import models, fields


class Workspace(models.Model):
    _inherit = 'ixdms.node'
    _description = 'Workspace'

    workspace_id = fields.Many2one(comodel_name='ixdms.node', string='Workspace', compute='_workspace_id')
    admin_ids = fields.Many2many(
        comodel_name='res.users', relation='ixdms_admin_workspace_user_rel', string='Admins')

    def _workspace_id(self):
        for rec in self:
            if rec.scope != 'workspace':
                rec.workspace_id = False
            elif not rec.parent_id:
                rec.workspace_id = rec
            else:
                rec.workspace_id = rec.parent_id.workspace_id
    