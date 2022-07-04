from odoo import models, fields, api

class MailChannel(models.Model):
    _inherit = 'mail.channel'

    cname = fields.Char(string='Channel Name')    
    course_id = fields.Many2one(comodel_name='ixlms.course', string='LMS Course')

    @api.onchange('cname', 'course_id')
    def _cname(self):
        for rec in self:
            if rec.course_id and rec.course_id.name and rec.cname:
                rec.name = rec.course_id.name
                if rec.cname:
                    rec.name += '-' + rec.cname

    def ix_channel_open(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_url',
            'target': 'new',
            'url': f'/chat/{self.id}/{self.uuid}',
        }