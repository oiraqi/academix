from odoo import models, fields, api

class LmsModule(models.Model):
    _inherit = 'ixlms.module'

    ilo_ids = fields.Many2many(comodel_name='ixcatalog.course.ilo', compute='_ilo_ids', string='Covered ILOs')

    @api.onchange('chapter_ids')
    def _ilo_ids(self):
        for rec in self:
            ilos = []
            for chapter in rec.chapter_ids:
                for ilo in chapter.ilo_ids:
                    if ilo.id not in ilos:
                        ilos.append(ilo.id)
            if len(ilos) > 0:
                rec.ilo_ids = ilos                
            else:
                rec.ilo_ids = False
    