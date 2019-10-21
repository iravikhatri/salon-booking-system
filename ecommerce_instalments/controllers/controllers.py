# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import datetime
from dateutil.relativedelta import *
from odoo.addons.website_sale.controllers.main import WebsiteSale

class WebsiteSaleInherited(WebsiteSale):
	def checkout_form_validate(self, mode, all_form_values, data):
		error, error_message = super(WebsiteSaleInherited, self).checkout_form_validate(mode, all_form_values, data)

		if 'email' in error:
			error.pop('email')
		else:
			return error, error_message

		if error_message != None:
			error_message.clear()

		return error, error_message

class EcommerceInstalments(http.Controller):

	@http.route('/emi/calculation', type='json', auth='public', methods=['POST'], website=True)
	def emi_cal(self, **post):

		def currency_format(real_price):
			currency_object = request.env.ref('base.main_company').currency_id
			price = ""
			if currency_object.position == "after":
				price = str(real_price) + str(currency_object.symbol)
			else:
				price = str(currency_object.symbol) + str(real_price)
			return price

		def emicalculation(total_ammount, interest_rate, payment_period):

			try:
				calculated_interest_rate = 1

				if interest_rate:
					calculated_interest_rate = interest_rate/100.0

				monthly_EMI = (total_ammount*pow((calculated_interest_rate/12)+1,
						(payment_period))*calculated_interest_rate/12)/(pow(calculated_interest_rate/12+1,
						(payment_period)) - 1)
				monthly_EMI = round(monthly_EMI,2)

				newDict = dict()
				newDict['s_no'] = [i for i in range(1,payment_period+1)]
				newDict['m_payment'] = [monthly_EMI for i in range(payment_period)]
				newDict['initialPayment'] = [total_ammount]
				newDict['interest'] = []
				newDict['principle'] = []
				newDict['end_balance'] = []
				newDict['Dates'] = []
				monthly_interest = round(calculated_interest_rate*100/12,3)

				for i in range(payment_period):
					newDict['Dates'].append(datetime.date.today() + relativedelta(months=+(i+1)))
					x = newDict['initialPayment'][-1]
					interest = (x*monthly_interest)/100
					interest = round(interest,2)
					newDict['interest'].append(interest)
					principle = monthly_EMI - interest
					newDict['principle'].append(round(principle,3))
					end_bal = x - round(principle,3)
					end_bal = round(end_bal,3)
					newDict['end_balance'].append(end_bal)
					newDict['initialPayment'].append(end_bal)
				newDict['initialPayment'].pop()
				newDict['end_balance'][-1] = 0

				newDict['total_interest_amount'] = currency_format(round(sum(newDict['interest']),2))
				newDict['total_interest_rate'] = interest_rate
				newDict['monthly_EMI'] = currency_format(monthly_EMI)

				return newDict
			except Exception as e:
				raise

		data = post.get('data')

		payment_time_period = data.get('payment_time_period')
		yearly_interest_rate = request.env['ir.default'].sudo().get("res.config.settings", "yearly_interest_rate")
		total_amount = request.env['sale.order'].sudo().search([('name', '=', request.website.sale_get_order().name)]).amount_total

		return emicalculation(total_amount, yearly_interest_rate, payment_time_period)


	@http.route('/emidata', type='json', auth='public', methods=['POST'], website=True)
	def emidata(self, **post):

		def currency_format(real_price):
			currency_object = request.env.ref('base.main_company').currency_id
			price = ""
			if currency_object.position == "after":
				price = str(real_price) + str(currency_object.symbol)
			else:
				price = str(currency_object.symbol) + str(real_price)
			return price

		def emicalculation(total_ammount, interest_rate, payment_period):

			try:
				calculated_interest_rate = 1

				if interest_rate:
					calculated_interest_rate = interest_rate/100.0

				monthly_EMI = (total_ammount*pow((calculated_interest_rate/12)+1,
						(payment_period))*calculated_interest_rate/12)/(pow(calculated_interest_rate/12+1,
						(payment_period)) - 1)
				monthly_EMI = round(monthly_EMI,2)

				newDict = dict()
				newDict['s_no'] = [i for i in range(1,payment_period+1)]
				newDict['m_payment'] = [monthly_EMI for i in range(payment_period)]
				newDict['initialPayment'] = [total_ammount]
				newDict['interest'] = []
				newDict['principle'] = []
				newDict['end_balance'] = []
				newDict['Dates'] = []
				monthly_interest = round(calculated_interest_rate*100/12,3)

				for i in range(payment_period):
					newDict['Dates'].append(datetime.date.today() + relativedelta(months=+(i+1)))
					x = newDict['initialPayment'][-1]
					interest = (x*monthly_interest)/100
					interest = round(interest,2)
					newDict['interest'].append(interest)
					principle = monthly_EMI - interest
					newDict['principle'].append(round(principle,3))
					end_bal = x - round(principle,3)
					end_bal = round(end_bal,3)
					newDict['end_balance'].append(end_bal)
					newDict['initialPayment'].append(end_bal)
				newDict['initialPayment'].pop()
				newDict['end_balance'][-1] = 0

				newDict['total_interest_amount'] = currency_format(round(sum(newDict['interest']),2))
				newDict['total_interest_rate'] = interest_rate
				newDict['monthly_EMI'] = currency_format(monthly_EMI)

				return newDict
			except Exception as e:
				raise

		data = post.get('data')

		sale_order_object = request.env['sale.order'].sudo().search([('name', '=', request.website.sale_get_order().name)])

		payment_time_period = data.get('payment_time_period')
		total_amount = sale_order_object.amount_total
		yearly_interest_rate = request.env['ir.default'].sudo().get("res.config.settings", "yearly_interest_rate")

		emidata = emicalculation(total_amount, yearly_interest_rate, payment_time_period)

		for num in emidata.get('s_no'):
			vals = {
				'serial_number': num,
				'monthly_date':  emidata.get('Dates')[num-1],
				'intial_principal': emidata.get('initialPayment')[num-1],
				'monthly_payment': emidata.get('m_payment')[num-1],
				'monthly_interest': emidata.get('interest')[num-1],
				'principal_amount': emidata.get('principle')[num-1],
				'end_balance': emidata.get('end_balance')[num-1]
			}

			if len(sale_order_object):
				sale_order_object.sudo().write({'instalments_details': [(0, 0, vals)]})

		if len(sale_order_object):
			sale_order_object.sudo().write({
				'total_instalment_amount': total_amount,
				'payment_period': payment_time_period,
				'total_interest_rate': yearly_interest_rate,
				'monthly_payment': emidata.get('m_payment')[0],
			})
