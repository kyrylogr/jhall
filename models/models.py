# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
import datetime
import dateutil.parser
import pytz

def schedule_time_to_float(t):
    return t.hour + t.minute/60

def convert_naive_datetime_to_utc(vdate, record):
    tz_name = record._context.get('tz') or record.env.user.tz            
    context_tz = pytz.timezone(tz_name)
    return context_tz.localize(vdate, is_dst=False).astimezone(pytz.UTC)

def convert_naive_datetime_to_field(vdate, record):
    return fields.Datetime.to_string(
        convert_naive_datetime_to_utc(vdate,record)
    )

def convert_field_to_datetime(value, record):
    vdate = fields.Datetime.from_string(value)
    tz_name = record._context.get('tz') or record.env.user.tz            
    context_tz = pytz.timezone(tz_name)
    return pytz.UTC.localize(vdate, is_dst=False).astimezone(context_tz)

def float_hours_to_time(vhours):
    return (datetime.datetime.min +
        datetime.timedelta(hours=vhours)).time()

class d_region(models.Model):
    _name = 'jhall.d_region'
    _description = 'Regions'
    name = fields.Char('Name', required = True)
    short_name = fields.Char('Short Name', required = True)
    description = fields.Text('Description', required = False)
    is_used = fields.Boolean('Is Used?', required = True, default = True)

class d_hall(models.Model):
    _name = 'jhall.d_hall'
    _description = 'Hall location'
    name = fields.Char('Name', required = True)
    short_name = fields.Char('Short Name', required = True)
    description = fields.Text('Description', required = False)
    is_used = fields.Boolean('Is Used?', required = True, default = True)
    region_id = fields.Many2one('jhall.d_region', 'Region',
            ondelete='restrict')

class d_spot(models.Model): 
    _name = 'jhall.d_spot'
    _description = 'Space in hall'
    name = fields.Char('Name', required = True)
    short_name = fields.Char('Short Name', required = True)
    description = fields.Text('Description', required = False)
    is_used = fields.Boolean('Is Used?', required = True, default = True)
    hall_id = fields.Many2one('jhall.d_hall', 'Hall',
           ondelete='restrict', required = True)

class p_user_params(models.TransientModel):
    _name = 'jhall.user_params'
    hall_id = fields.Many2one('jhall.d_hall', 'Hall')
    @api.multi
    def set_param_hall_id(self):
        for wizard in self:
#            self.env.context.update('hall_id', wizard.hall_id)
#            self._context.update('hall_id', wizard.hall_id)
            self.with_context( {'hall_id' : wizard.hall_id} )

class d_equipment_type(models.Model):
    _name = 'jhall.d_equipment_type'
    _description = 'Equipment Type'
    name = fields.Char('Name', required = True)
    short_name = fields.Char('Short Name', required = True)
    is_used = fields.Boolean('Is Used?', required = True, default = True)

class d_equipment(models.Model):
    _name = 'jhall.h_equipment'
    _description = 'Equipment'
    type_id = fields.Many2one('jhall.d_equipment_type', 'Type',
           ondelete='restrict', required = True)
    hall_id = fields.Many2one('jhall.d_hall', 'Hall',
           ondelete='restrict', required = True)
    spot_id = fields.Many2one('jhall.d_spot', 'Spot',
           ondelete='restrict')
    name = fields.Char('Name', required = True)
    no = fields.Char('Number', required = False)
    description = fields.Text('Description')
    is_used = fields.Boolean('Is Used?', required = True, default = True)

class d_service_category(models.Model):
    _name = 'jhall.d_service_category'
    _description = 'Service Category'
    name = fields.Char('Name', required = True)
    short_name = fields.Char('Short Name', required = True)
    description = fields.Text('Description', required = False)
    is_used = fields.Boolean('Is Used?', required = True, default = True)

class d_service_type(models.Model):
    _name = 'jhall.d_service_type'
    _description = 'Service Type'
    equipment_type_id = fields.Many2one('jhall.d_equipment_type', 'Equipment Type',
           ondelete='restrict', required = False)
    category_id = fields.Many2one('jhall.d_service_category', 'Category',
           ondelete='restrict', required = False)
    name = fields.Char('Name', required = True)
    short_name = fields.Char('Short Name', required = True)
    description = fields.Text('Description', required = False)
    is_used = fields.Boolean('Is Used?', required = True, default = True)
    is_coach_included = fields.Boolean('Is trainer included?', required = True, default = False)
    num_customers = fields.Integer('Maximum number of customers', required = True, default = 1)
    default_unit_time = fields.Integer('Default time (pay unit)', required = True, default = 60)
    min_time = fields.Integer('Minimum duration (minutes)', required = True, default = 60)
    max_time = fields.Integer('Maximum duration (minutes)')
    time_step = fields.Integer('Step duration (minutes)', required = True, default = 30)
    hall_reserve = fields.Boolean('Complete hall reservation', required = True, default = False)
    hall_id = fields.Many2one('jhall.d_hall', 'hall',
           ondelete='restrict', required = False)

class d_service_price(models.Model):
    _name = 'jhall.d_service_price'
    _description = 'Service price'
    type_id = fields.Many2one('jhall.d_service_type', 'Service Type',
            ondelete='restrict', required = True)
    date_begin = fields.Date('Begin Date', required = True, default = fields.Date.today)
    date_end = fields.Date('End Date', required = True)
    price_cash = fields.Float("Price Cash", (10,2),required = True)
    price_units = fields.Float("Price Unit", (5,2))

class d_trainer(models.Model):
    _name = 'jhall.d_trainer'
    _description = 'Trainer'
    _inherits = {'res.partner': "partner_id"}
    partner_id = fields.Many2one('res.partner',ondelete='restrict',required=True)
    skills = fields.Char('Skills')
    experience = fields.Integer('experience (1-10)')
    is_used = fields.Boolean('Is Used?', required = True, default = True)

class d_abonement_type(models.Model):
    _name = 'jhall.d_abonement_type'
    _description = 'Abonement Type'
    name = fields.Char('Name', required = True)
    short_name = fields.Char('Short Name', required = True)
    description = fields.Text('Description', required = False)
    is_used = fields.Boolean('Is Used?', required = True, default = True)
    is_coach_included = fields.Boolean('Is trainer included?', required = True, default = True)
    n_units = fields.Integer('Units', required = True, default = 8)
    days_duration = fields.Integer('Duration in days', required = True, default = 45)

class d_abonement_price(models.Model):
    _name = 'jhall.d_abonement_price'
    _description = 'Abonement price'
    type_id = fields.Many2one('jhall.d_abonement_type', 'Abonement Type',
            ondelete='restrict', required = True)
    date_begin = fields.Date('Begin Date', required = True, default = fields.Date.today)
    date_end = fields.Date('End Date', required = True)
    price = fields.Float("Price", (7,2),required = True)

class o_customer(models.Model):
    _name = 'jhall.o_customer'
    _description = 'Client'
    _inherits = {'res.partner': "partner_id"}
    partner_id = fields.Many2one('res.partner',ondelete='restrict',required=True, 
        auto_join=True)
    mobile = fields.Char('mobile phone', related = 'partner_id.mobile')
    date_birth= fields.Date('Date of birth', required = False)
    date_register = fields.Date('Date register', required = False)
    prefered_communication = fields.Selection([
        ('phone', 'Phone'),
        ('sms', 'sms'),
        ('viber', 'Viber'),
        ('telegram', 'Telegram')], string = "Preferred communication")
    notes = fields.Text('Notes')
    last_visit = fields.Many2one('jhall.h_customer_visit', "Last Visit", 
       ondelete='set null', auto_join=True)
    last_visit_date = fields.Date('Last Visit Date',
       related='last_visit.date_visit')
    last_visit_hall = fields.Many2one('jhall.d_hall','Last Visit Location',
       related='last_visit.hall_id')
    next_visit = fields.Many2one('jhall.h_customer_visit', "Next Visit", 
       ondelete='set null', auto_join=True)
    next_visit_date = fields.Date('Next Visit Date',
       related='next_visit.date_visit')
    next_visit_hall = fields.Many2one('jhall.d_hall' ,'Next Visit Location',
       related='next_visit.hall_id')
    count_visits = fields.Integer('Number of visits')
    count_cancels = fields.Integer('Number of cancels')
    date_last_cancel = fields.Date('Date of last cancel')
    count_fines = fields.Integer('Count fines')
    date_last_fine = fields.Date('Date last fine')
    date_last_contact = fields.Date('Date last contact')
    date_next_contact = fields.Date('Date next scheduled contact')
    abonements = fields.One2many('jhall.o_abonement',
        'customer_id', string="Abonements", limit = 20)
    visits = fields.One2many('jhall.h_customer_visit',
        'customer_id', string="Visits", limit = 20)
    contacts = fields.One2many('jhall.o_customer_interraction',
        'customer_id', string="Interractions", limit = 20)

class h_abonement(models.Model):
    _name = 'jhall.o_abonement'
    _description = 'Abonement' 
    name = fields.Char('Number', required = True, index = True)
    state = fields.Selection([
        (1, 'New'),
        (2, 'Active'),
        (3, 'Expired'),
        (4, 'Closed')], string = "State", default = 1, required = True)
    customer_id = fields.Many2one('jhall.o_customer', 'Client',
            ondelete='restrict', required = True)
    type_id = fields.Many2one('jhall.d_abonement_type', 'Abonement Type',
            ondelete='restrict', required = True)
    price = fields.Float("Price", (12,2),required = True, 
            default = 0)
    paid = fields.Float("Amount Paid", (12,2), default = 0)
    left_to_pay = fields.Float("Amount Left", (12,2), default = 0, 
            compute="_compute_left_to_pay", store=True)
    date_issue = fields.Date('Issue Date', required = False, 
            default = fields.Date.today)
    date_payment = fields.Date('Pay Date', required = False)
    date_activate = fields.Date('Activate Date')
    date_expire = fields.Date('Expire Date')
    date_close = fields.Date('Close Date')
    units = fields.Integer("Units", required = True)
    units_left = fields.Integer("Units left", default = 0, 
            required = True, 
            compute="_compute_units_left", store=True)
    units_total_used = fields.Integer("Used units",
            compute="_compute_units_total_used", store=True)
    units_used = fields.Integer("Units used normally", default = 0, 
            required = True, readonly = True)
    units_used_fine = fields.Integer("Units fined", default = 0, 
            required = True, readonly = True)
    notes = fields.Text('Notes')
    payments = fields.One2many('jhall.h_visit_payment', 'abonement', 
            string = 'Payments')
    closed_by_user_id = fields.Many2one('res.users', 'Closed by user',
            ondelete='restrict')

    @api.depends('paid', 'price')
    def _compute_left_to_pay(self):
        for record in self:
            record.left_to_pay = record.price - record.paid

    @api.depends('units_used','units_used_fine')
    def _compute_units_total_used(self):
        for record in self:
            record.units_total_used = record.units_used + record.units_used_fine

    @api.depends('units','units_used','units_used_fine')
    def _compute_units_left(self):
        for record in self:
            record.units_left = (
                record.units - record.units_used 
                - record.units_used_fine)

    @api.onchange('state')
    def _state_change(self):
        if (self.state==4):
            self.closed_by_user_id = self.env.uid
            self.date_close = fields.Date.today()
        else:
            self.closed_by_user_id = None
            if (self.date_close!=0):
                self.date_close = None
            if (self.state==2):
                self.date_activate = fields.Date.today()

    @api.onchange('date_activate')
    def _date_activate_change(self):
        if (self.date_activate!=0):
            if (self.type_id is None):
                raise ValidationError("Type must be filled before activation")
            self.date_expire = ( dateutil.parser.parse(self.date_activate).date() + 
                datetime.timedelta(days=self.type_id.days_duration))

    @api.onchange('type_id')
    def _type_id_change_compute_units(self):
        if (self.state>=2):
            raise ValidationError("Can not change type of active abonement")
        self.units = self.type_id.n_units

# if these fields are changed, call method
# add constraint that type_id can not be edited
    @api.onchange('type_id')
    def _type_id_change(self):
        modelPrice = self.env['jhall.d_abonement_price']
        res = modelPrice.search( [('type_id','=',self.type_id.id),
            ('date_begin','<=',fields.Date.today()),
            ('date_end','>=',fields.Date.today())] )
        if (res):
            self.price = res.price
            self.left_to_pay = res.price

    @api.onchange('paid')
    def _paid_change(self):
        if (self.paid != 0) and (self.date_payment == 0):
            self.date_payment = fields.Date.today()

class o_trainer_schedule(models.Model):
    _name = 'jhall.o_trainer_schedule'
    _description = 'Abonement'
    trainer_id = fields.Many2one('jhall.d_trainer', 'Trainer',
            ondelete='restrict', required = True)
    hall_id = fields.Many2one('jhall.d_hall', 'Hall',
            ondelete='restrict', required = True)
    date_begin = fields.Date('Date begin', required = True)
    date_end = fields.Date('Date end', required = True)
    day_numbers = fields.Char("Day types (number)")
    time_begin = fields.Float('Time begin', required = True)
    time_end = fields.Float('Time end', required = True)
    break_begin = fields.Float('Break begin', required = False)
    break_end = fields.Float('Break end', required = False)
    service_type = fields.Many2one('jhall.d_service_type', 'Service Type',
            required = False)

class h_customer_visit(models.Model):
    _name = 'jhall.h_customer_visit'
    _description = 'Client visit'
#   date of insert and user who added are in system fields
    date_visit = fields.Date('Date visit', required = True)
    time_begin = fields.Float('Time begin', required = True)
    time_end = fields.Float('Time end', required = True)
    state = fields.Selection([
        ('request', 'Request'),
        ('cancel', 'Cancel'),        
        ('agree',  'Agree'),
        ('reschedule', 'Reschedule'),
        ('confirm', 'Confirm'),
        ('cancel_fine', 'Cancel with fine'),
        ('no_show', 'No show'),
        ('complete', 'Completed')], 
        string = "State", default = 2, required = True)
    hall_id = fields.Many2one('jhall.d_hall', 'Hall',
            ondelete='restrict', required = True)
    customer_id = fields.Many2one('jhall.o_customer', 'Client',
            ondelete='restrict', required = True)
    date_rescheduled_to = fields.Date('Rescheduled to date')
    notes = fields.Text('Notes')
    visit_amount = fields.Float('Amount cash', (12,2))
    visit_amount_units = fields.Float('Amount units', (12,2))
    prepayment = fields.Float('Prepayment', (12,2))
    left_to_pay = fields.Float('Left to pay', (12,2))
    payment_notes = fields.Char('Payment notes')
    client_notes = fields.Text('Client notes')
    date_remind = fields.Date('Date remind')
    user_remind = fields.Many2one('res.users', 'Remind by manager')
    remind_info = fields.Text('Remind Info')
    remind_contact = fields.Many2one('jhall.o_customer_interraction', 'Remind contact',
            ondelete='restrict', required = False)

class h_schedule_book(models.Model):
    _name = 'jhall.h_schedule_booking'
    _description = 'Schedule book'
    _order = 'date_time_book, hall_id, equipment_id'    
#   date of insert and user who added are in system fields
    hall_id = fields.Many2one('jhall.d_hall', 'Hall',
            ondelete='restrict', required = True
#            ,  default=lambda self: self.env.context.get('hall_id', False)
            )
    service_type = fields.Many2one('jhall.d_service_type', 'Service Type',
            ondelete='restrict', required = True, auto_join = True)
    equipment_type_id = fields.Many2one('jhall.d_equipment_type', 'Equipment Type',
            related = "service_type.equipment_type_id")
    is_coach_included = fields.Boolean('Need coach', 
            related = "service_type.is_coach_included")
    date_time_book = fields.Datetime('Date Time booking', 
            required = False, index = True)
    date_book = fields.Date('Date schedule', required = True, 
            compute="_compute_date_book", 
            inverse="_inverse_date_book", store = True)
    time_begin = fields.Float('Time begin', required = True,
            compute="_compute_time_begin", 
            inverse="_inverse_time_begin", store = True)
    duration = fields.Float('Duration', default = 1)
    test_field = fields.Float('Test field', default = 1)    
    time_end = fields.Float('Time end', required = True, 
            compute="_compute_time_end", store=True)
    customer_id = fields.Many2one('jhall.o_customer', 'Client',
            ondelete='restrict', required = False)
    customer_mobile = fields.Char('mobile phone', related = 'customer_id.mobile')
    trainer_id = fields.Many2one('jhall.d_trainer', 'Trainer',
            ondelete='restrict', required = False)
    equipment_id = fields.Many2one('jhall.h_equipment', 'Equipment',
            ondelete='restrict', required = False,
            domain="[('type_id', '=', equipment_type_id),('hall_id', '=', hall_id)]" 
            )
    state = fields.Selection([
        ('request', 'Request'),
        ('cancel', 'Cancel'),        
        ('agree',  'Agree'),
        ('confirm', 'Confirm'),
        ('cancel_fine', 'Cancel with fine'),
        ('no_show', 'No client'),
        ('complete', 'Completed')], string = "Book state", default ='agree', required = True)
    visit = fields.Many2one('jhall.h_customer_visit', 'Visit',
            ondelete='restrict', required = False)
    notes = fields.Text('Notes')
#    _defaults = {'hall_id' : context.get('hall_id', False), }        


    @api.constrains('duration')
    def _duration_within_of_service_type(self):
        for record in self:
            if (not (record.service_type) or not (record.duration)):
                continue
            service_type = record.service_type
            duration_minutes = record.duration * 60
            if (service_type.max_time != 0 and duration_minutes > service_type.max_time \
                    or duration_minutes < service_type.min_time):
                raise ValidationError("Booking time out of service time [%d, %d]" % 
                    (service_type.min_time, service_type.max_time))
            if (service_type.time_step>0 and service_type.min_time>0):
                diff_min_time = duration_minutes - service_type.min_time
                diff_units = diff_min_time  / service_type.time_step
                diff_remainder =  diff_min_time - int(diff_units) * service_type.time_step
                if (diff_remainder > 0.01):
                    raise ValidationError("Step time is not respected (%d minutes)" % service_type.time_step)

#           todo: add check for time_step

    @api.onchange('service_type')
    def _change_service_type_calculate_duration(self):
        record = self
        service_type = record.service_type
        if (service_type and service_type.default_unit_time>0):
            target_duration = service_type.default_unit_time / 60
            if (not  record.duration \
                or service_type.min_time > 0 \
                and service_type.min_time> record.duration):
                    record.duration = target_duration
        if (service_type and record.equipment_id \
            and service_type.equipment_type_id != record.equipment_id.type_id):
                record.equipment_id = None


    @api.depends('time_begin', 'duration')
    def _compute_time_end(self):        
        for record in self:
            if not (record.time_begin and record.duration):
                record.time_end = record.time_begin
            record.time_end = record.time_begin + record.duration

    @api.depends('date_time_book')
    def _compute_date_book(self):
        for record in self:
            if not (record.date_time_book):
                continue
            vdate_time = fields.Datetime.from_string(record.date_time_book)
            record.date_book = fields.Date.to_string(vdate_time.date())

    def _inverse_date_book(self):
        for record in self:
            if not (record.date_book):
                continue            
            vdate = fields.Date.from_string(record.date_book)
            if record.date_time_book:
                vtime = fields.Datetime.from_string(record.date_time_book).time()                
            else:
                vtime = float_hours_to_time(record.time_begin)
                
            record.date_time_book = convert_naive_datetime_to_field(
                datetime.datetime.combine(vdate, vtime), record)

    @api.depends('date_time_book')
    def _compute_time_begin(self):
        for record in self:
            if not (record.date_time_book):
                continue
            vdate_time = convert_field_to_datetime(record.date_time_book, record)
            record.time_begin = schedule_time_to_float(
                vdate_time.time())

    def _inverse_time_begin(self):
        for record in self:
            if not (record.time_begin):
                continue
            vtime = float_hours_to_time(record.time_begin)                
            if record.date_book:
                vdate = fields.Date.from_string(record.date_book)                
            else:
                vdate = fields.Datetime.from_string(record.date_time_book).date()
                
            record.date_time_book = convert_naive_datetime_to_field(
                datetime.datetime.combine(vdate, vtime), record)

class h_visit_payment(models.Model):
    _name = 'jhall.h_visit_payment'
    _description = 'Client visit'
    hall_id = fields.Many2one('jhall.o_customer', 'Hall',
        related='visit.customer_id')
    visit = fields.Many2one('jhall.h_customer_visit', 'Visit')        
    customer_id = fields.Many2one('jhall.o_customer', 'Client',
        related='visit.customer_id')
    cash_amount = fields.Float('Cash Amount', (12,2))
    unit_amount = fields.Float('Unit Amount', (12,2))
    abonement = fields.Many2one('jhall.o_abonement', 'Abonement')
    date_visit = fields.Date('Date visit', related='visit.date_visit')
#   add constraint that abonement date_expire 
#   should not be less than date_visit

class o_customer_interraction(models.Model):
    _name = 'jhall.o_customer_interraction'
    _description = 'Customer interraction'
    date_contact = fields.Date('Date contact', required = True)
    initial_mean = fields.Selection([
        ('phone', 'Phone'),
        ('sms', 'sms'),
        ('viber', 'Viber'),
        ('telegram', 'Telegram'),
        ('talk', 'speech'),
        ('other', 'other')], string = "Communication mean", required = True)
    executed_mean  = fields.Selection([
        ('phone', 'Phone'),
        ('sms', 'sms'),
        ('viber', 'Viber'),
        ('telegram', 'Telegram'),
        ('talk', 'speech'),
        ('other', 'other')], string = "Executed mean") 
    hall_id = fields.Many2one('jhall.d_hall', 'Hall',
            ondelete='restrict', required = True)
    customer_id = fields.Many2one('jhall.o_customer', 'Client',
            ondelete='restrict', required = True)
    subject = fields.Char('Subject')
    message = fields.Text('Message')
    state =  fields.Selection([
        ('plan', 'plan'),
        ('attempt', 'attempt'),
        ('sent', 'sent'),
        ('success', 'success'),
        ('giveup', 'giveup')], string = "State")
    num_attempts = fields.Integer('Number of attempts')
    last_attempt = fields.Datetime('Last Attempt')
    notes = fields.Text('Notes')
    customer_responce = fields.Text('Responce')
    customer_confirmed = fields.Boolean('Customer confirmed')
    responce_loyality =  fields.Integer('Responce loyality')
    user_performed = fields.Many2one('res.users', 'Performed by user')
    date_time_contact = fields.Datetime('Date and time of contact')