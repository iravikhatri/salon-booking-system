# -*- coding: utf-8 -*-

import datetime
import calendar
import werkzeug.utils
from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale

class ThemeVivre(http.Controller):

    @http.route(['/booking'], type='http', auth='public', website=True)
    def appointment_booking(self):

        return request.render("theme_vivre.appointment_booking")

    @http.route(['/shop/choose/date'], type='http', auth='public', website=True)
    def booking_date_tab(self):

        return request.render("theme_vivre.choose_date")

    @http.route(['/getdetails'], type='json', auth="public", methods=['POST'], website=True, csrf=False)
    def product_details_view(self,**kw):

        data = kw.get('data')
        product_name = data.get('product_name')

        product_object = request.env['product.template'].sudo().search([('name', '=', product_name)])

        total_time = ""

        if product_object.appointment_time:
            if product_object.appointment_time < 2:
                total_time = '30 mins'
            else:
                hours = (product_object.appointment_time//2)
                minutes = (product_object.appointment_time/2) - hours
                if minutes:
                    total_time = f"{hours} hour(s) {str(minutes).replace('.','').replace('5','3')} mins"
                else:
                    total_time = f"{hours} hour(s)"
        else:
            total_time = f"{product_object.appointment_time} mins"

        product_price = ""

        currency_object = request.env.ref('base.main_company').currency_id

        if currency_object.position == "after":
            product_price = str(product_object.list_price) + ' ' + str(currency_object.symbol)
        else:
            product_price = str(currency_object.symbol) + ' ' + str(product_object.list_price)

        vals = {
            'description': product_object.description_sale,
            'name': product_object.name,
            'appointment_time': total_time,
            'price': product_price,
        }

        return vals


    @http.route('/quotationtimeslots', type='json', auth='public', methods=['POST'], website=True)
    def quotation_time_slots(self, **post):

        data = post.get('data')
        new_date = data.get("appoint_date")

        sale_object = request.env['sale.order'].sudo().search([ ('id', '=', request.session.get('sale_order_id') ) ])
        total_service_time = sale_object.total_appointment_time

        booking_date = datetime.datetime.strptime(new_date, '%m/%d/%Y')
        calculated_day = booking_date.strftime('%A')

        day_dist = {"Monday": '0', "Tuesday": '1', "Wednesday": '2', "Thursday": '3', "Friday": '4', "Saturday": '5',"Sunday": '6'}

        def get_room_avail_slot(day, date, total_time):
            # day: is the weekday like monday, tuesday.. etc
            rooms = request.env['room.booking'].sudo().search(
                [])  # initalizing the avail_room object
            room_list = []  # list of tuples of rooms, time_from and time_to available on given 'day'
            if rooms:
                for room in rooms:
                    for d in room.room_time_slot:
                        if str(d.name) == str(day):
                            room_list.append((room, d.time_from, d.time_to))
                if not room_list:
                    return {}
            else:
                return {}

            booking_info = request.env['booking.info'].sudo().search([('date', '=', date), '|', ('status', '=', 'sale'), ('status', '=', 'draft')])
            # dict of booked room   < 'key of room code' , '[booked slots]' >
            booking_list = {}
            if booking_info:
                for booked_room in booking_info:
                    if booked_room.room_code in booking_list: booking_list.update({booked_room.room_code: [time for time in booking_list[booked_room.room_code]] + [ [int(booked_room.time_from), int(booked_room.time_to)]]})
                    else:
                        booking_list.update(
                            {booked_room.room_code: [[int(booked_room.time_from), int(booked_room.time_to)]]})
            # dict of slot available for the room < 'key as room id', 'available slot according to the total_time' >
            availableSlot = {}
            for room in room_list:
                availableSlot.update(
                    {room[0].code: is_valid_room(room[1], room[2], booking_list.get(room[0].code), total_time)})
            return availableSlot

        def is_valid_room(time_from, time_to, bookedSlot, total_time):
            time = 0
            time_from = int(time_from)
            time_to = int(time_to)

            # calculating the booked Slot time
            for slot in bookedSlot or '':
                time += slot[1] - slot[0]

            # calculation remaining time(hours) in the room
            time = abs((time_to - time_from) - time)

            # if the room is valid for the further process or not
            # then return the available time slots
            # else return empty slot
            if time >= total_time:
                TotalSlot = [time_from, time_to]
                return createAvailableSlots(TotalSlot, bookedSlot, total_time)
            return []

        def getAvailableTimeSlot(availableSlots, total_time):
            # creating the available slots in the room
            # availableSlots = self.createAvailableSlots(TotalSlot, bookedSlot)
            timeSlots = []
            # creating the slot according to the limit
            for slot in availableSlots:
                diff = slot[1] - slot[0]
                start = slot[0]
                if total_time <= diff:
                    for _ in range((diff - total_time) + 1):
                        timeSlots.append([start, start + total_time])
                        start += 1
            return timeSlots

        def createAvailableSlots(TotalSlot, bookedSlot, total_time):
            # if the room is emply then return TotalSlot
            if not bookedSlot:
                return getAvailableTimeSlot([TotalSlot], total_time)
            slots = []
            # start and end point of the slot
            start = TotalSlot[0]
            end = TotalSlot[1]
            # sorting the booked slot according to the first element of the list of lists
            bookedSlot = sorted(bookedSlot)
            # creating the slot
            for slot in bookedSlot:
                slots.append([start, slot[0]])
                start = slot[1]
            if start < end:
                slots.append([start, end])
            return getAvailableTimeSlot(slots, total_time)

        total_available_time_slots = get_room_avail_slot(day_dist[calculated_day], booking_date, total_service_time)

        def dist_funtion(dt):
            distint_list = []  # distint list of total slots available [[2,5],[6,7],[1,4],[5,8]]
            for room_code in dt:  # getting key values of the dict
                # getting the list of slots associated with key
                for time_slot in list(dt[room_code]):
                    if time_slot in distint_list:
                        # removing the duplicate
                        dt[room_code].remove(time_slot)
                    else:
                        # creasting the distinct list
                        distint_list = distint_list + [time_slot]

        dist_funtion(total_available_time_slots)

        return total_available_time_slots

    @http.route(['/choose/date'], type='http', methods=['POST'], auth='public', website=True, csrf=False)
    def rooms_search_day(self, **post):

        if post.get("appoint_date") == '':
            vals = {
                'appoint_date_alert': 1
            }
            return request.render('theme_vivre.choose_date', vals)
        else:
            if post.get('select_time_slots') == None:
                vals = {
                    'select_time_slots_alert': 1
                }
                return request.render('theme_vivre.choose_date', vals)
            else:
                new_date = post.get("appoint_date")
                sale_object = request.env['sale.order'].sudo().search([ ('id', '=', request.session.get('sale_order_id') ) ])
                total_appointment_time = sale_object.total_appointment_time
                booking_date = datetime.datetime.strptime(new_date, '%m/%d/%Y')

                room_code, time_from, time_to = [int(x) for x in post.get('select_time_slots').split('-')]

                cal_room_code = request.env['room.booking'].sudo().search([('code', '=', room_code)])

                dist1 = {
                    'room_allotted': cal_room_code.id,
                    'date': booking_date,
                }

                dist2 = {
                    'time_from': str(time_from),
                    'time_to': str(time_to),
                }

                try:
                    sale_object.sudo().write(dist1)
                except Exception as e:
                    print(e, 'Some Error(s) 1')

                try:
                    sale_object.sudo().write({'time': [(0, 0, dist2)]})
                except Exception as e:
                    print(e, 'Some Error(s) 2')

                booking_data = {
                    'name': str(sale_object.name),
                    'customer_name': str(sale_object.partner_id.name),
                    'date': sale_object.date,
                    'time_from': str(time_from),
                    'time_to': str(time_to),
                    'room_code': str(sale_object.room_allotted.code),
                    'sales_person': str(sale_object.user_id.name),
                    'status': str(sale_object.state),
                    'total_appointment_time': str(total_appointment_time),
                }

                booking_info_object = request.env['booking.info'].sudo().search([('name', '=', sale_object.name)])

                if len(booking_info_object.ids):
                    booking_info_object.sudo().write(booking_data)

                return werkzeug.utils.redirect('/shop/checkout?express=1')


class WebsiteSales(WebsiteSale):

    @http.route(['/shop/cart/updates'], type='json', auth="public", methods=['POST'], website=True, csrf=False)
    def cart_update(self,**kw):

        add_qty=1
        set_qty=0

        data = kw.get('data')
        product_id = data.get('product_id')

        """This route is called when adding a product to cart (no options)."""
        sale_order = request.website.sale_get_order(force_create=True)
        if sale_order.state != 'draft':
            request.session['sale_order_id'] = None
            sale_order = request.website.sale_get_order(force_create=True)

        product_custom_attribute_values = None
        if kw.get('product_custom_attribute_values'):
            product_custom_attribute_values = json.loads(kw.get('product_custom_attribute_values'))

        no_variant_attribute_values = None
        if kw.get('no_variant_attribute_values'):
            no_variant_attribute_values = json.loads(kw.get('no_variant_attribute_values'))

        sale_order._cart_update(
            product_id=int(product_id),
            add_qty=add_qty,
            set_qty=set_qty,
            product_custom_attribute_values=product_custom_attribute_values,
            no_variant_attribute_values=no_variant_attribute_values
        )

        sale_object = request.website.sale_get_order()
        total_quantity = 0

        for record in sale_object.order_line:
            total_quantity += int(record.product_uom_qty)

        vals = {
            'total_quantity': total_quantity
        }

        return vals
