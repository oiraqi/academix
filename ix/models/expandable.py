from odoo import models


class Expandable(models.AbstractModel):
    _name = 'ix.expandable'
    _description = 'Expandable Mixin'

    def _expand_to(self, action_id, domain=False, context=False, res_id=False):
        action = self.env['ir.actions.act_window']._for_xml_id(action_id)
        if domain:
            action['domain'] = domain
        if context:
            action['context'] = context
        if res_id:
            action['res_id'] = res_id
        return action
    