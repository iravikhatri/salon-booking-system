# -*- coding: utf-8 -*-

from odoo import models, fields, api

class WebsitePageInherated(models.Model):
    _inherit = 'website.page'

    is_explore_page = fields.Boolean('Is a explore page')
    is_policy_page = fields.Boolean('Is a policy page')