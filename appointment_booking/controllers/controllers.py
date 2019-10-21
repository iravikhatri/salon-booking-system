from odoo.http import request
import calendar

from datetime import date, timedelta
import datetime

import logging

from odoo import http, tools, _
# from odoo.addons.base.ir.ir_qweb.fields import nl2br
# from odoo.addons.website.models.website import slug
# from odoo.addons.website.controllers.main import QueryURL
# from odoo.exceptions import ValidationError
# from odoo.addons.website_sale.controllers.main import WebsiteSale
# from werkzeug.exceptions import Forbidden, NotFound
# import werkzeug.utils

from odoo.addons.website_sale.controllers.main import TableCompute
from odoo.addons.website_sale.controllers.main import WebsiteSale

from odoo.addons.website_sale.controllers.main import PPG
from odoo.addons.website_sale.controllers.main import PPR

_logger = logging.getLogger(__name__)

PPG = 21  # Products Per Page
PPR = 3  # Products Per Row


class CustomCalendar(http.Controller):

    # rooms day controller part start

    @http.route(['/rooms/day/search'], type='http', methods=['POST'], auth='public', website=True, csrf=False)
    def rooms_search_day(self, **post):
        search_date = post.get('calendar_date_search')

        if search_date:

            new_date = search_date.replace('/', ' ')
            date_object = datetime.datetime.strptime(new_date, '%m %d %Y')

            request.session['current_date'] = date_object
            current_date = date_object.strftime('%Y-%m-%d')

            title_current_date = request.session['current_date'].strftime('%d-%b-%Y')

            data = {
                'current_date': current_date,
                'title_current_date': title_current_date
            }

        else:
            request.session['current_date'] = date.today()
            current_date = request.session['current_date'].strftime('%Y-%m-%d')
            title_current_date = request.session['current_date'].strftime('%d-%b-%Y')

            data = {
                'current_date': current_date,
                'title_current_date': title_current_date
            }

        return request.render("appointment_booking.calendar_room_day", data)

    @http.route(['/rooms/day'], type='http', auth='public', website=True)
    def rooms_day(self):

        request.session['current_date'] = date.today()
        current_date = request.session['current_date'].strftime('%Y-%m-%d')
        title_current_date = request.session['current_date'].strftime('%d-%b-%Y')

        data = {
            'current_date': current_date,
            'title_current_date': title_current_date
        }

        return request.render("appointment_booking.calendar_room_day", data)

    @http.route(['/rooms/day/next'], type='http', auth='public', website=True)
    def rooms_next_day(self):
        yesterday = request.session['current_date'] + timedelta(1)
        request.session['current_date'] = yesterday
        current_date = yesterday.strftime('%Y-%m-%d')

        title_current_date = request.session['current_date'].strftime('%d-%b-%Y')

        data = {
            'current_date': current_date,
            'title_current_date': title_current_date
        }

        return request.render("appointment_booking.calendar_room_day", data)

    @http.route(['/rooms/day/previous'], type='http', auth='public', website=True)
    def rooms_previous_day(self):
        yesterday = request.session['current_date'] - timedelta(1)
        request.session['current_date'] = yesterday
        current_date = yesterday.strftime('%Y-%m-%d')

        title_current_date = request.session['current_date'].strftime('%d-%b-%Y')

        data = {
            'current_date': current_date,
            'title_current_date': title_current_date
        }

        return request.render("appointment_booking.calendar_room_day", data)

    @http.route(['/rooms/week/search'], type='http', methods=['POST'], auth='public', website=True, csrf=False)
    def rooms_search_week(self, **post):

        search_date = post.get('calendar_date_search')

        if search_date:
            month, day, year = (int(x) for x in search_date.split('/'))
            total_weeks = calendar.monthcalendar(year, month)

            for num_week, current_week in enumerate(total_weeks):
                for current_day in current_week:
                    if day == current_day:
                        current_num_week = num_week

            current_week = total_weeks[current_num_week]
            start_week_val = 1

            if current_week[0] != 0:
                start_week_val = current_week[0]

            data = {
                'current_date': search_date,
                'current_month': month,
                'current_year': year,
                'current_week': current_week,
                'start_week': start_week_val,
                'end_week': max(current_week),
            }

            string_date = search_date.replace('/', ' ')
            datetime_object = datetime.datetime.strptime(string_date, '%m %d %Y')
            week_num_list = []

            for i in current_week:
                if i != 0:
                    week_num_list.append(i)

            week_num_list_num = len(week_num_list)
            request.session['next_date'] = datetime_object + timedelta(week_num_list_num)
            request.session['previous_date'] = datetime_object - timedelta(week_num_list_num)

        else:
            today = datetime.date.today()
            today_date = today - datetime.timedelta(days=today.weekday())
            current_date = today_date.strftime('%Y-%m-%d')
            year, month, day = (int(x) for x in current_date.split('-'))
            total_weeks = calendar.monthcalendar(year, month)

            current_num_week = 0

            for num_week, current_week in enumerate(total_weeks):
                for current_day in current_week:
                    if day == current_day:
                        current_num_week = num_week

            current_week = total_weeks[current_num_week]
            start_week_val = 1

            if current_week[0] != 0:
                start_week_val = current_week[0]

            data = {
                'current_date': current_date,
                'current_month': month,
                'current_year': year,
                'current_week': current_week,
                'start_week': start_week_val,
                'end_week': max(current_week),
            }

            week_num_list = []

            for i in current_week:
                if i != 0:
                    week_num_list.append(i)

            week_num_list_num = len(week_num_list)
            request.session['next_date'] = today_date + timedelta(week_num_list_num)
            request.session['previous_date'] = today_date - timedelta(week_num_list_num)

        return request.render("appointment_booking.calendar_room_week", data)

    @http.route(['/rooms/week'], type='http', auth='public', website=True)
    def rooms_week(self):

        today_date = datetime.date.today()
        current_date = today_date.strftime('%Y-%m-%d')
        year, month, day = (int(x) for x in current_date.split('-'))
        total_weeks = calendar.monthcalendar(year, month)

        current_num_week = 0

        for num_week, current_week in enumerate(total_weeks):
            for current_day in current_week:
                if day == current_day:
                    current_num_week = num_week

        current_week = total_weeks[current_num_week]
        start_week_val = 1

        if current_week[0] != 0:
            start_week_val = current_week[0]

        data = {
            'current_date': current_date,
            'current_month': month,
            'current_year': year,
            'current_week': current_week,
            'start_week': start_week_val,
            'end_week': max(current_week),
        }

        print('data', data)

        week_num_list = []

        for i in current_week:
            if i != 0:
                week_num_list.append(i)

        week_num_list_num = len(week_num_list)
        request.session['next_date'] = today_date + timedelta(week_num_list_num)
        request.session['previous_date'] = today_date - timedelta(week_num_list_num)

        return request.render("appointment_booking.calendar_room_week", data)

    @http.route(['/rooms/week/next'], type='http', auth='public', website=True)
    def rooms_next_week(self):

        current_date = request.session['next_date'].strftime('%Y-%m-%d')
        year, month, day = (int(x) for x in current_date.split('-'))
        total_weeks = calendar.monthcalendar(year, month)

        current_num_week = 0

        for num_week, current_week in enumerate(total_weeks):
            for current_day in current_week:
                if day == current_day:
                    current_num_week = num_week

        current_week = total_weeks[current_num_week]
        start_week_val = 1

        if current_week[0] != 0:
            start_week_val = current_week[0]

        data = {
            'current_date': current_date,
            'current_month': month,
            'current_year': year,
            'current_week': current_week,
            'start_week': start_week_val,
            'end_week': max(current_week),
        }

        week_num_list = []

        for i in current_week:
            if i != 0:
                week_num_list.append(i)

        week_num_list_num = len(week_num_list)

        request.session['next_date'] = request.session['next_date'] + timedelta(week_num_list_num)
        request.session['previous_date'] = request.session['previous_date'] + timedelta(week_num_list_num)

        return request.render("appointment_booking.calendar_room_week", data)

    @http.route(['/rooms/week/previous'], type='http', auth='public', website=True)
    def rooms_previous_week(self):

        next_week = request.session['previous_date']
        request.session['previous_date'] = next_week
        current_date = next_week.strftime('%Y-%m-%d')
        year, month, day = (int(x) for x in current_date.split('-'))
        total_weeks = calendar.monthcalendar(year, month)

        current_num_week = 0

        for num_week, current_week in enumerate(total_weeks):
            for current_day in current_week:
                if day == current_day:
                    current_num_week = num_week

        current_week = total_weeks[current_num_week]
        start_week_val = 1

        if current_week[0] != 0:
            start_week_val = current_week[0]

        data = {
            'current_date': current_date,
            'current_month': month,
            'current_year': year,
            'current_week': current_week,
            'start_week': start_week_val,
            'end_week': max(current_week),
        }

        week_num_list = []

        for i in current_week:
            if i != 0:
                week_num_list.append(i)

        week_num_list_num = len(week_num_list)

        request.session['previous_date'] = request.session['previous_date'] - timedelta(week_num_list_num)
        request.session['next_date'] = request.session['next_date'] - timedelta(week_num_list_num)

        return request.render("appointment_booking.calendar_room_week", data)

    @http.route(['/salespersons/day/search'], type='http', methods=['POST'], auth='public', website=True, csrf=False)
    def salesperson_search_day(self, **post):
        search_date = post.get('calendar_date_search')

        if search_date:

            new_date = search_date.replace('/', ' ')
            date_object = datetime.datetime.strptime(new_date, '%m %d %Y')
            request.session['current_date'] = date_object
            current_date = date_object.strftime('%Y-%m-%d')
            title_current_date = request.session['current_date'].strftime('%d-%b-%Y')

            data = {
                'current_date': current_date,
                'title_current_date': title_current_date
            }

        else:
            request.session['current_date'] = date.today()
            current_date = request.session['current_date'].strftime('%Y-%m-%d')
            title_current_date = request.session['current_date'].strftime('%d-%b-%Y')

            data = {
                'current_date': current_date,
                'title_current_date': title_current_date
            }

        return request.render("appointment_booking.calendar_salespersons_day", data)

    @http.route(['/salespersons/day'], type='http', auth='public', website=True)
    def salesperson_day(self):
        request.session['current_date'] = date.today()
        current_date = request.session['current_date'].strftime('%Y-%m-%d')
        title_current_date = request.session['current_date'].strftime(
            '%d-%b-%Y')

        data = {
            'current_date': current_date,
            'title_current_date': title_current_date
        }

        return request.render("appointment_booking.calendar_salespersons_day", data)

    @http.route(['/salespersons/day/next'], type='http', auth='public', website=True)
    def salesperson_next_day(self):
        yesterday = request.session['current_date'] + timedelta(1)
        request.session['current_date'] = yesterday
        current_date = yesterday.strftime('%Y-%m-%d')

        title_current_date = request.session['current_date'].strftime(
            '%d-%b-%Y')

        data = {
            'current_date': current_date,
            'title_current_date': title_current_date
        }

        return request.render("appointment_booking.calendar_salespersons_day", data)

    @http.route(['/salespersons/day/previous'], type='http', auth='public', website=True)
    def salesperson_previous_day(self):
        yesterday = request.session['current_date'] - timedelta(1)
        request.session['current_date'] = yesterday
        current_date = yesterday.strftime('%Y-%m-%d')

        title_current_date = request.session['current_date'].strftime(
            '%d-%b-%Y')

        data = {
            'current_date': current_date,
            'title_current_date': title_current_date
        }

        return request.render("appointment_booking.calendar_salespersons_day", data)

    @http.route(['/salespersons/week/search'], type='http', methods=['POST'], auth='public', website=True, csrf=False)
    def rooms_search_week(self, **post):

        search_date = post.get('calendar_date_search')

        if search_date:
            month, day, year = (int(x) for x in search_date.split('/'))
            total_weeks = calendar.monthcalendar(year, month)

            for num_week, current_week in enumerate(total_weeks):
                for current_day in current_week:
                    if day == current_day:
                        current_num_week = num_week

            current_week = total_weeks[current_num_week]
            start_week_val = 1

            if current_week[0] != 0:
                start_week_val = current_week[0]

            data = {
                'current_date': search_date,
                'current_month': month,
                'current_year': year,
                'current_week': current_week,
                'start_week': start_week_val,
                'end_week': max(current_week),
            }

            string_date = search_date.replace('/', ' ')
            datetime_object = datetime.datetime.strptime(string_date, '%m %d %Y')
            week_num_list = []

            for i in current_week:
                if i != 0:
                    week_num_list.append(i)

            week_num_list_num = len(week_num_list)
            request.session['next_date'] = datetime_object + timedelta(week_num_list_num)
            request.session['previous_date'] = datetime_object - timedelta(week_num_list_num)

        else:
            today = datetime.date.today()
            today_date = today - datetime.timedelta(days=today.weekday())
            current_date = today_date.strftime('%Y-%m-%d')
            year, month, day = (int(x) for x in current_date.split('-'))
            total_weeks = calendar.monthcalendar(year, month)

            current_num_week = 0

            for num_week, current_week in enumerate(total_weeks):
                for current_day in current_week:
                    if day == current_day:
                        current_num_week = num_week

            current_week = total_weeks[current_num_week]
            start_week_val = 1

            if current_week[0] != 0:
                start_week_val = current_week[0]

            data = {
                'current_date': current_date,
                'current_month': month,
                'current_year': year,
                'current_week': current_week,
                'start_week': start_week_val,
                'end_week': max(current_week),
            }

            week_num_list = []

            for i in current_week:
                if i != 0:
                    week_num_list.append(i)

            week_num_list_num = len(week_num_list)
            request.session['next_date'] = today_date + timedelta(week_num_list_num)
            request.session['previous_date'] = today_date - timedelta(week_num_list_num)

        return request.render("appointment_booking.calendar_salespersons_week", data)

    @http.route(['/salespersons/week'], type='http', auth='public', website=True)
    def salesperson_week(self):

        today_date = datetime.date.today()
        current_date = today_date.strftime('%Y-%m-%d')
        year, month, day = (int(x) for x in current_date.split('-'))
        total_weeks = calendar.monthcalendar(year, month)

        current_num_week = 0

        for num_week, current_week in enumerate(total_weeks):
            for current_day in current_week:
                if day == current_day:
                    current_num_week = num_week

        current_week = total_weeks[current_num_week]

        start_week_val = 1

        if current_week[0] != 0:
            start_week_val = current_week[0]

        data = {
            'current_date': current_date,
            'current_month': month,
            'current_year': year,
            'current_week': current_week,
            'start_week': start_week_val,
            'end_week': max(current_week),
        }

        week_num_list = []

        for i in current_week:
            if i != 0:
                week_num_list.append(i)

        week_num_list_num = len(week_num_list)

        request.session['next_date'] = today_date + timedelta(week_num_list_num)
        request.session['previous_date'] = today_date - timedelta(week_num_list_num)

        return request.render("appointment_booking.calendar_salespersons_week", data)

    @http.route(['/salespersons/week/next'], type='http', auth='public', website=True)
    def salesperson_next_week(self):

        current_date = request.session['next_date'].strftime('%Y-%m-%d')
        year, month, day = (int(x) for x in current_date.split('-'))
        total_weeks = calendar.monthcalendar(year, month)

        current_num_week = 0

        for num_week, current_week in enumerate(total_weeks):
            for current_day in current_week:
                if day == current_day:
                    current_num_week = num_week

        current_week = total_weeks[current_num_week]

        start_week_val = 1

        if current_week[0] != 0:
            start_week_val = current_week[0]

        data = {
            'current_date': current_date,
            'current_month': month,
            'current_year': year,
            'current_week': current_week,
            'start_week': start_week_val,
            'end_week': max(current_week),
        }

        week_num_list = []

        for i in current_week:
            if i != 0:
                week_num_list.append(i)

        week_num_list_num = len(week_num_list)

        request.session['next_date'] = request.session['next_date'] + timedelta(week_num_list_num)
        request.session['previous_date'] = request.session['previous_date'] + timedelta(week_num_list_num)

        return request.render("appointment_booking.calendar_salespersons_week", data)

    @http.route(['/salespersons/week/previous'], type='http', auth='public', website=True)
    def salesperson_previous_week(self):

        next_week = request.session['previous_date']
        request.session['previous_date'] = next_week
        current_date = next_week.strftime('%Y-%m-%d')
        year, month, day = (int(x) for x in current_date.split('-'))
        total_weeks = calendar.monthcalendar(year, month)

        current_num_week = 0

        for num_week, current_week in enumerate(total_weeks):
            for current_day in current_week:
                if day == current_day:
                    current_num_week = num_week

        current_week = total_weeks[current_num_week]

        start_week_val = 1

        if current_week[0] != 0:
            start_week_val = current_week[0]

        data = {
            'current_date': current_date,
            'current_month': month,
            'current_year': year,
            'current_week': current_week,
            'start_week': start_week_val,
            'end_week': max(current_week),
        }

        week_num_list = []

        for i in current_week:
            if i != 0:
                week_num_list.append(i)

        week_num_list_num = len(week_num_list)

        request.session['previous_date'] = request.session['previous_date'] - timedelta(week_num_list_num)
        request.session['next_date'] = request.session['next_date'] - timedelta(week_num_list_num)

        return request.render("appointment_booking.calendar_salespersons_week", data)
