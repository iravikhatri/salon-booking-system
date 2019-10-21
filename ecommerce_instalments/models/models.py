# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError
import requests

class ResConfigSettingsInherited(models.TransientModel):
    _inherit = 'res.config.settings'

    yearly_interest_rate = fields.Float('Yearly Interest Rate', default=0)

    @api.multi
    def set_values(self):
        res = super(ResConfigSettingsInherited,self).set_values()
        ICPSudo = self.env['ir.default'].sudo()
        ICPSudo.set("res.config.settings", "yearly_interest_rate", self.yearly_interest_rate)
        return res

class ProductTemplateInehrtied(models.Model):
    _inherit = "product.template"

    @api.one
    @api.constrains('list_price','lst_price')
    def list_price_constrains(self):
        if self.list_price < 1 or self.lst_price < 1 :
            raise ValidationError(("Product price must be greater than zero"))

class SaleOrderInehrtied(models.Model):
    _inherit = "sale.order"

    instalments_details = fields.One2many(comodel_name='instalments.details', inverse_name='sale_order_instalments_details_ids', string='Instalments details', ondelete='cascade')

    total_instalment_amount = fields.Monetary('Total Amount')
    payment_period = fields.Integer('Payment Period')
    total_interest_rate = fields.Float('Total Interest Rate')
    monthly_payment = fields.Monetary('Monthly Payment')
    abacus_result = fields.Integer('Abacus Result')

    @api.one
    def abacus_decision(self):
        url = 'http://121.88.5.249:18400/predictions/odoo/'
        sale_number = self.name.replace('SO','')

        post_data =  {
            "order_number": int(sale_number),
            "amount": self.total_instalment_amount,
            "month": self.payment_period
        }

        response = requests.post(url, post_data)
        final_result = eval(response.text).get('approved')

        result_dict = {
            'abacus_result': final_result
        }

        if response.status_code == 200:
            self.sudo().write(result_dict)


class InstalmentsDetails(models.Model):
    _name = "instalments.details"

    sale_order_instalments_details_ids = fields.Many2one('sale.order', string='Sale Order IDs')
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.user.company_id.currency_id)

    serial_number = fields.Integer('Serial Number')
    monthly_date = fields.Date('Due Date')
    intial_principal = fields.Monetary('Intial Principal')
    monthly_payment = fields.Monetary('Monthly Payment')
    monthly_interest = fields.Monetary('Interest Amount')
    principal_amount = fields.Monetary('Principal  Amount')
    end_balance = fields.Monetary('End Balance')
    payment_recieved = fields.Date('Payment Recieved')
