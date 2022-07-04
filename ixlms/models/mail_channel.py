from odoo import models, fields

class MailChannel(models.Model):
    _inherit = 'mail.channel'

    course_id = fields.Many2one(comodel_name='ixlms.course', string='LMS Course')

    def _resolve_action(self, action_id, domain, context=False):
        action = self.env['ir.actions.act_window']._for_xml_id(action_id)
        action['domain'] = domain
        if context:
            action['context'] = context		
        return action

    def ix_channel_open(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_url',
            'target': 'new',
            'url': f'/chat/{self.id}/{self.uuid}',
        }