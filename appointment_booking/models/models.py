from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
import calendar


class BookingDashBoard(models.Model):
	_name = 'booking.dashboard'

	name = fields.Integer()


class RoomBooking(models.Model):
	_name = 'room.booking'

	name = fields.Char('Room Name', index=True)
	code = fields.Char('Room Code', copy=False)
	room_time_slot = fields.One2many(comodel_name='room.time.slot', inverse_name='room_booking_time_slot_ids', string='Time Slot', copy=True)

	@api.one
	@api.constrains('room_time_slot')
	def day_constrains(self):
		number_start = 0
		number_end = 6
		for record in self.room_time_slot:
			for rec in self.room_time_slot:
				if record.name == rec.name and str(record.name) != str(number_start) and str(record.name) != str(
						number_end):
					raise ValidationError("""Sorry, you cannot be repeat a day more than one time and days must be in ascending order... \nAscending order such as monday, tuesday to sunday""")
			number_start += 1
			number_end -= 1

		for record in self.room_time_slot:
			if int(record.time_to) <= int(record.time_from):
				raise ValidationError("Sorry, the end time must be greater than start time...")

	@api.one
	@api.constrains('code')
	def room_code_constrains(self):
		ob = self.env['room.booking'].search([])
		for record in ob:
			if str(record.code) == str(self.code) and record.id != self.id:
				raise ValidationError("Sorry, room code must be different, please fill another room code...")


class RoomTimeSlot(models.Model):
	_name = 'room.time.slot'

	sale_order_time_slot_ids = fields.Many2one('sale.order', string='Sale Order IDs')
	room_booking_time_slot_ids = fields.Many2one('room.booking', string='Room Booking IDs')
	name = fields.Selection(
		[('0', 'Monday'), ('1', 'Tuesday'), ('2', 'Wednesday'), ('3', 'Thursday'),
		 ('4', 'Friday'), ('5', 'Saturday'), ('6', 'Sunday')], string='Day', required=True, default="0")

	time_from = fields.Selection(
		[('0', '00:00'), ('1', '00:30'), ('2', '01:00'), ('3', '01:30'), ('4', '02:00'),
		 ('5', '02:30'), ('6', '03:00'), ('7', '03:30'), ('8', '04:00'), ('9', '04:30'),
		 ('10', '05:00'), ('11', '05:30'), ('12', '06:00'), ('13', '06:30'), ('14', '07:00'),
		 ('15', '07:30'), ('16', '08:00'), ('17', '08:30'), ('18', '09:00'), ('19', '09:30'),
		 ('20', '10:00'), ('21', '10:30'), ('22', '11:00'), ('23', '11:30'), ('24', '12:00'),
		 ('25', '12:30'), ('26', '13:00'), ('27', '13:30'), ('28', '14:00'), ('29', '14:30'),
		 ('30', '15:00'), ('31', '15:30'), ('32', '16:00'), ('33', '16:30'), ('34', '17:00'),
		 ('35', '17:30'), ('36', '18:00'), ('37', '18:30'), ('38', '19:00'), ('39', '19:30'),
		 ('40', '20:00'), ('41', '20:30'), ('42', '21:00'), ('43', '21:30'), ('44', '22:00'),
		 ('45', '22:30'), ('46', '23:00'), ('47', '23:30')], string='From', default='0')

	time_to = fields.Selection(
		[('0', '00:00'), ('1', '00:30'), ('2', '01:00'), ('3', '01:30'), ('4', '02:00'),
		 ('5', '02:30'), ('6', '03:00'), ('7', '03:30'), ('8', '04:00'), ('9', '04:30'),
		 ('10', '05:00'), ('11', '05:30'), ('12', '06:00'), ('13', '06:30'), ('14', '07:00'),
		 ('15', '07:30'), ('16', '08:00'), ('17', '08:30'), ('18', '09:00'), ('19', '09:30'),
		 ('20', '10:00'), ('21', '10:30'), ('22', '11:00'), ('23', '11:30'), ('24', '12:00'),
		 ('25', '12:30'), ('26', '13:00'), ('27', '13:30'), ('28', '14:00'), ('29', '14:30'),
		 ('30', '15:00'), ('31', '15:30'), ('32', '16:00'), ('33', '16:30'), ('34', '17:00'),
		 ('35', '17:30'), ('36', '18:00'), ('37', '18:30'), ('38', '19:00'), ('39', '19:30'),
		 ('40', '20:00'), ('41', '20:30'), ('42', '21:00'), ('43', '21:30'), ('44', '22:00'),
		 ('45', '22:30'), ('46', '23:00'), ('47', '23:30')], string='To', default='1')


class BookingInfo(models.Model):
	_name = 'booking.info'

	name = fields.Char(string='Sale Order',)
	customer_name = fields.Char(string='Customer')
	date = fields.Date(string='Date')
	time_from = fields.Char(string='From')
	time_to = fields.Char(string='To')
	room_code = fields.Char(string='Room Code')
	sales_person = fields.Char(string='Sales Person')
	status = fields.Char(string='Status')
	total_appointment_time = fields.Char(string='Total Appointment Time')


class ProductTemplateInherited(models.Model):
	_inherit = 'product.template'

	appointment_time = fields.Integer(string="Appointment Time")

	@api.onchange('type')
	def hide_appointment_time(self):
		if self.type != 'service':
			self.appointment_time = 0


class SaleInherited(models.Model):
	_inherit = "sale.order"

	@api.multi
	def unlink(self):
		for order in self:
			booking_object = self.env['booking.info'].search([('name', '=', order.name)])
			if booking_object:
				booking_object.unlink()
		unlink_object = super(SaleInherited, self).unlink()
		return unlink_object

	@api.multi
	def action_cancel(self):
		action_object = super(SaleInherited, self).action_cancel()
		self.update_booking()
		return action_object

	@api.multi
	def action_draft(self):
		draft_object = super(SaleInherited, self).action_draft()
		self.update_booking()
		return draft_object

	@api.multi
	def _write(self, values):
		write_object = super(SaleInherited, self)._write(values)
		for rec in self:
			rec.update_booking()
		return write_object

	@api.multi
	def print_quotation(self):
		draft_object = super(SaleInherited, self).print_quotation()
		self.update_booking()
		return draft_object

	def check_appointment_time_conflict(self, total_appointment_time, room, date, time_from, time_to):
		if total_appointment_time == 0:
			if room:
				raise ValidationError("You can't select room for non appointment product")
			elif date:
				raise ValidationError("You can't select date for non appointment product")
			elif time_from or time_to:
				raise ValidationError("You can't select time slot for non appointment product")
			else:
				return True
		if not room:
			raise ValidationError("You didn't select any room for appointment")
		if not date:
			raise ValidationError("You didn't select any date for appointment")
		if not time_from or not time_to:
			raise ValidationError("You didn't select any time slot for appointment")

		year, month, day = (int(x) for x in date.split('-'))
		days = ['0', '1', '2', '3', '4', '5', '6']
		day = days[calendar.weekday(year, month, day)]
		room_time_from = 0
		room_time_to = 0
		for d in room.room_time_slot:
			if d.name == day:
				room_time_from = int(d.time_from)
				room_time_to = int(d.time_to)
		time_from = int(time_from)
		time_to = int(time_to)
		time_diff = (time_to - time_from)
		if time_diff == 0:
			raise ValidationError("Selected Appointment Time Can't be Zero(0)")

		if total_appointment_time == time_diff:
			if self.check_room_time_conflict(room, time_from, time_to, date):
				return True
			else:
				raise ValidationError("Selected Room time appointment is not available ")
		elif total_appointment_time > (room_time_to - room_time_from):
			raise ValidationError("appointment time can't be greater then total room appointment time limit")
		elif time_diff < total_appointment_time:
			raise ValidationError("Selected Room Appointment time is less then appoinment time requested \nPlease select a room appointment time which is equal to the total appointment time")
		elif time_diff > total_appointment_time:
			raise ValidationError("Room Appointment Time selected is greater the appointment time \nPlease select a room appointment time which is equal to the total appointment time")

	def check_room_time_conflict(self, room, time_from, time_to, date):
		year, month, day = (int(x) for x in date.split('-'))
		days = ['0', '1', '2', '3', '4', '5', '6']
		day = days[calendar.weekday(year, month, day)]
		room_time_from = 0
		room_time_to = 0
		for d in room.room_time_slot:
			if d.name == day:
				room_time_from = int(d.time_from)
				room_time_to = int(d.time_to)
		time_from = int(time_from)
		time_to = int(time_to)

		available_time = [i for i in range(int(room_time_from), int(room_time_to) + 1)]
		selected_set = [i for i in range(int(time_from), int(time_to) + 1)]
		selected_set = set(selected_set)

		booking_info = self.env['booking.info'].search(
			[('room_code', '=', room.code), ('date', '=', date), ('name', '!=', self.name), '|', ('status', '=', 'sale'), ('status', '=', 'draft')])
		booking_slots = []
		if booking_info:
			if not set(selected_set).issubset(set(available_time)):
				return False

			for booked_room in booking_info:
				if booked_room.date.strftime("%Y-%m-%d") == date:
					booking_slots.append([int(booked_room.time_from), int(booked_room.time_to)])

			booked_set = []

			for slot in booking_slots:
				temp = [i for i in range(int(slot[0]), int(slot[1]) + 1)]
				booked_set += temp
				if selected_set.issubset(set(temp)):
					return False

			booked_set = set(booked_set)

			remaining_time = set(available_time) - booked_set
			remaining_time.add(time_from)
			remaining_time.add(time_to)

			if set(selected_set).issubset(remaining_time):
				return True
		else:
			if set(selected_set).issubset(set(available_time)):
				return True
		return False

	@api.one
	@api.constrains('order_line', 'room_allotted', 'date', 'time', 'user_id')
	def check_lines(self):
		if len(self.time) > 1:
			raise ValidationError("You can't add more then one time slot")

		if self.state == 'sale':
			if self.check_appointment_time_conflict(self.total_appointment_time, self.room_allotted, self.date.strftime("%Y-%m-%d"), self.time.time_from, self.time.time_to):
				self.update_booking()
				return True
		else:
			if (len(self.room_allotted) > 0) and (self.total_appointment_time > 0) and (len(self.time) > 0) and self.date:
				if not self.check_appointment_time_conflict(self.total_appointment_time, self.room_allotted, self.date.strftime("%Y-%m-%d"), self.time.time_from, self.time.time_to):
					raise ValidationError("Selected Room time appointment is not valid or not available ")
		self.update_booking()
		return True

	@api.multi
	def action_confirm(self):
		if len(self.time) > 1:
			raise ValidationError("You can't add more then one time slot")
		if self.check_appointment_time_conflict(self.total_appointment_time, self.room_allotted, self.date.strftime("%Y-%m-%d"), self.time.time_from, self.time.time_to):
			returned_value = super(SaleInherited, self).action_confirm()
			self.update_booking()
			return returned_value

	@api.model
	def create(self, vals):
		sale_object = super(SaleInherited, self).create(vals)
		booking_dist = {
			'name': str(sale_object.name),
			'total_appointment_time': str(sale_object.total_appointment_time),
			'customer_name': str(sale_object.partner_id.name),
			'date': sale_object.date,
			'room_code': str(sale_object.room_allotted.code),
			'sales_person': str(sale_object.user_id.name),
			'status': str(sale_object.state),
			'time_from': sale_object.time.time_from,
			'time_to': sale_object.time.time_to,
		}

		self.env['booking.info'].create(booking_dist)
		return sale_object

	room_allotted = fields.Many2one('room.booking', string='Room Allotted')
	date = fields.Date('Date')
	time = fields.One2many(comodel_name='room.time.slot', inverse_name='sale_order_time_slot_ids', string='Time Slot Booked', ondelete='cascade')
	total_appointment_time = fields.Integer(string='Total Booking Time', compute="calculate_appointment_time", store=True)

	@api.one
	@api.depends('order_line', 'order_line.product_id', 'order_line.product_uom_qty')
	def calculate_appointment_time(self):
		time = 0
		for line in self.order_line:
			val = line.product_id.appointment_time
			qty = line.product_uom_qty
			time += int(val) * int(qty) if val else 0
		self.total_appointment_time = time
		return time

	def update_booking(self):

		booking_data = {
			'total_appointment_time': str(self.total_appointment_time),
			'customer_name': str(self.partner_id.name),
			'date': self.date,
			'room_code': str(self.room_allotted.code),
			'sales_person': str(self.user_id.name),
			'status': str(self.state),
			'time_from': self.time.time_from,
			'time_to': self.time.time_to,
		}

		booking_object = self.env['booking.info'].search([('name', '=', self.name)])

		if booking_object:
			booking_object.write(booking_data)
