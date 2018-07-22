# -*- coding: utf-8 -*-

from odoo import models, fields, api

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
     hall_reserve = fields.Boolean('Complete hall reservation', required = True, default = False)     
     num_customers = fields.Integer('Maximum number of customers', required = True, default = 1)               
     default_unit_time = fields.Integer('Default time (pay unit)', required = True, default = 60)     
     min_time = fields.Integer('Minimum duration (minutes)', required = True, default = 60)          
     max_time = fields.Integer('Maximum duration (minutes)')                         
     time_step = fields.Integer('Step duration (minutes)', required = True, default = 30)          

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
    partner_id = fields.Many2one('res.partner',ondelete='restrict',required=True)
    date_birth = fields.Date('Date of birth', required = False)    
    prefered_communication = fields.Selection([
        ('phone', 'Phone'),
        ('sms', 'sms'),
        ('viber', 'Viber'),
        ('telegram', 'Telegram')], string = "Preferred communication")

class h_abonement(models.Model):    
    _name = 'jhall.o_abonement'
    _description = 'Abonement' 
    name = fields.Char('Number', required = True)    
    customer_id = fields.Many2one('jhall.o_customer', 'Client',
            ondelete='restrict', required = True)    
    type_id = fields.Many2one('jhall.d_abonement_type', 'Abonement Type',
            ondelete='restrict', required = True)    
    price = fields.Float("Price", (7,2),required = True, 
            default = 0)
    paid = fields.Float("Amount Paid", (7,2), default = 0)
    left_to_pay = fields.Float("Amount Left", (7,2), default = 0, 
            compute="_compute_left_to_pay", store=True)    
    date_issue = fields.Date('Issue Date', required = False, default = fields.Date.today)
    date_payment = fields.Date('Pay Date', required = False)    
    date_activate = fields.Date('Activate Date')
    date_expire = fields.Date('Expire Date')    
    units = fields.Integer("Units", required = True)
    units_left = fields.Integer("Units left", default = 0, required = True, 
            compute="_compute_units_left", store=True)    
    units_total_used = fields.Integer("Used units",  
            compute="_compute_units_total_used", store=True)
    units_used = fields.Integer("Units used normally", default = 0, required = True, readonly = True)
    units_used_fine = fields.Integer("Units fined", default = 0, required = True, readonly = True)

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

    @api.onchange('type_id')
    def _compute_units(self):
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



