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

from odoo import models
from odoo.exceptions import AccessError

import logging

_logger = logging.getLogger(__name__)

class IrActionsServer(models.Model):
    """ This is to fix a bug at the level of Odoo 15.0
    """
    _inherit = 'ir.actions.server'
	
    def run(self):
        """ Runs the server action. For each server action, the
        :samp:`_run_action_{TYPE}[_multi]` method is called. This allows easy
        overriding of the server actions.

        The `_multi` suffix means the runner can operate on multiple records,
        otherwise if there are multiple records the runner will be called once
        for each

        :param dict context: context should contain following keys

                             - active_id: id of the current object (single mode)
                             - active_model: current model that should equal the action's model

                             The following keys are optional:

                             - active_ids: ids of the current records (mass mode). If active_ids
                               and active_id are present, active_ids is given precedence.

        :return: an action_id to be executed, or False is finished correctly without
                 return action
        """
        res = False
        for action in self.sudo():
            action_groups = action.groups_id
            if action_groups:
                if not (action_groups & self.env.user.groups_id):
                    raise AccessError(_("You don't have enough access rights to run this action."))
            #else:
            #    try:
            #        self.env[action.model_name].check_access_rights("write")
            #    except AccessError:
            #        _logger.warning("Forbidden server action %r executed while the user %s does not have access to %s.",
            #            action.name, self.env.user.login, action.model_name,
            #        )
            #        raise

            eval_context = self._get_eval_context(action)
            #records = eval_context.get('record') or eval_context['model']
            #records |= eval_context.get('records') or eval_context['model']
            #if records:
            #    try:
            #        records.check_access_rule('write')
            #    except AccessError:
            #        _logger.warning("Forbidden server action %r executed while the user %s does not have access to %s.",
            #            action.name, self.env.user.login, records,
            #        )
            #        raise

            runner, multi = action._get_runner()
            if runner and multi:
                # call the multi method
                run_self = action.with_context(eval_context['env'].context)
                res = runner(run_self, eval_context=eval_context)
            elif runner:
                active_id = self._context.get('active_id')
                if not active_id and self._context.get('onchange_self'):
                    active_id = self._context['onchange_self']._origin.id
                    if not active_id:  # onchange on new record
                        res = runner(action, eval_context=eval_context)
                active_ids = self._context.get('active_ids', [active_id] if active_id else [])
                for active_id in active_ids:
                    # run context dedicated to a particular active_id
                    run_self = action.with_context(active_ids=[active_id], active_id=active_id)
                    eval_context["env"].context = run_self._context
                    res = runner(run_self, eval_context=eval_context)
            else:
                _logger.warning(
                    "Found no way to execute server action %r of type %r, ignoring it. "
                    "Verify that the type is correct or add a method called "
                    "`_run_action_<type>` or `_run_action_<type>_multi`.",
                    action.name, action.state
                )
        return res or False