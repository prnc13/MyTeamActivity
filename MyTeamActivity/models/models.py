# -*- coding: utf-8 -*-


from odoo import models, fields, api,tools
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError



#     its is a activity category Master to add activity(for ex: income tax)
class ActivityCategory(models.Model):
    _name="activity.category"
    _rec_name='activity_category'
    activity_category=fields.Char(string='Activity Category', help="Add Activity Category Here")
    color = fields.Char(string="Color",help="Choose your color",size=7)
    tag_ids=fields.Many2one('res.partner')

#       its is a activity category Master to add activity(for ex: income tax)
class ActivityType(models.Model):
    _name="activity.type"
    _rec_name='activity_type'


    activity_category_id=fields.Many2one('activity.category',string='Activity Category',help="Add Activity Category Here")
    activity_type=fields.Char(string="Activity Type",help="Add Activity Type Here") 


    # hide = fields.Boolean(string='Hide', compute="_compute_hide")
    # @api.onchange('activity_category_id')
    # def _onchange_act(self):
    #     if self.activity_category_id:
    #         return {'domain': {'activity_type_id': [('activity_category_id', '=', self.activity_category_id.id)]}}
    #     else:
    #         return {'domain': {'activity_type_id': []}}


    
        
    # Show Hide State selection based on Country
    # @api.depends('act')
    # def _compute_hide(self):
    #     if self.act:
    #         self.hide = False
    #     else:
    #         self.hide = True        

class SubActivity(models.Model):
    _name='subactivity'
    name=fields.Char('Sub Activity',required=True,help="Add Sub Activity Here")
    activity_category_id=fields.Many2one(related='activity_type_id.activity_category_id',string='Activity Category',help="Add Activity Category Here")
    activity_type_id=fields.Many2one('activity.type',string='Activity Type',help="Add Activity Type Here")
    user_id=fields.Many2one('res.users',string='User')
    date=fields.Date(string="Task Date")
    main_id=fields.Many2one('reminder')

    @api.onchange('activity_category_id')
    def _onchange_act(self):
        if self.activity_category_id:
            return {'domain': {'activity_type_id': [('activity_category_id', '=', self.activity_category_id.id)]}}
        else:
            return {'domain': {'activity_type_id': []}}


class Reminder(models.Model):
    _name='reminder'
    # _inherit = ['mail.thread', 'mail.activity.mixin']
    
    activity_category_id=fields.Many2one(related='activity_type_id.activity_category_id',string='Activity Category',help="Add Activity Category Here")
    activity_type_id=fields.Many2one('activity.type',string='Activity Type',help="Add Activity Type Here")
    user_id=fields.Many2one('res.users',string="User",store=True,default=lambda self: self.env.uid,help="Add User Here")
    customer_name=fields.Many2one('res.partner',help="Add Customer Name Here")
    rem_date= fields.Date(string="Reminder",store=True,required=True,help="Add Reminder Date Here")
    last_date= fields.Date(string='Last Date',store=True,required=True,help="Add Last Date Here")
    actual_date= fields.Date(string='Actual Date',help="Add Actual Date Here")
    target_date= fields.Date(string='Target Date',store=True ,required=True,help="Add Taget Date Here")
    status= fields.Selection([('pending','Pending'),('hold','On Hold'),('done','Done')])
    partner_id=fields.Many2one('res.partner',string='Customer')
    # order_rem_ids=fields.Many2many('final',string="Sub Activity")
    order_rem_ids=fields.One2many('reminder_view','order_ids')
    sub_ids=fields.One2many('subactivity','main_id')
    

    @api.onchange('activity_category_id')
    def _onchange_act(self):
        if self.activity_category_id:
            return {'domain': {'activity_type_id': [('activity_category_id', '=', self.activity_category_id.id)]}}
        else:
            return {'domain': {'activity_type_id': []}}



    @api.multi
    def name_get(self):
        return [(alert.id, '%s %s' % ((""), '%d' % alert.id)) for alert in self]


    # @api.onchange('activity_type_id')
    # def _onchange_state(self):
    #     subactivities = self.env['final'].search([('activity_type_id', '=', self.activity_type_id.id)])
    #     temp = [[4, sub.id] for sub in subactivities]
    #     self.order_rem_ids= temp

    
    @api.onchange('activity_type_id')     
    def _onchange_sub(self):
        activities=[]
        subactivities=self.env['reminder'].search([('activity_type_id', '=', self.activity_type_id.id)])
        
        for activity in subactivities:
            activities.append((0,0,{
                'name':activity.name
                }))
            print(activities)
        self.order_rem_idss=activities
        print(self.order_rem_idss)


     


    # @api.onchange('activity_category_id')
    # def _onchange_act(self):
    #     if self.activity_category_id:
    #         return {'domain': {'activity_type_id': [('activity_category_id', '=', self.activity_category_id.id)]}}
    #     else:
    #         return {'domain': {'activity_type_id': []}}




    @api.multi
    @api.constrains('last_date','rem_date','actual date','target_date')
    def reminder_date(self):
        for this in self:
            end =fields.Date.from_string(this.last_date)
            rem = fields.Date.from_string(this.rem_date)
            target= fields.Date.from_string(this.target_date)
            if end < rem:
                raise ValidationError("Reminder Date is not valid")  
            elif end < target:
                raise ValidationError("Target Date is not valid")
    

class reminderview(models.Model):
    _name='reminder_view'

    name=fields.Char(string='Sub activity',required=True)

    customer_name = fields.Many2one('res.partner', string="Customer Name", related='order_ids.customer_name',readonly=True)

    activity_category_id = fields.Many2one('activity.category', string='Activity Category',
                                  related='order_ids.activity_category_id', readonly=True, store=True)

    activity_type_id = fields.Many2one('activity.type', string='Activity Type',
                                  related='order_ids.activity_type_id', readonly=True, store=True)
    date = fields.Date(string='Sub Activity Target Date', related='product_ids.date', store=True)
    date_1 = fields.Date(string='Sub Activity Actual Date', related='product_ids.date', store=True)
    # supplier = fields.Many2one('res.partner', string='Vendor', related='product_id.supplier',
    order_ids = fields.Many2one('reminder',ondelete='cascade', required=True,string='Reminder ID')
    product_ids=fields.Many2one('subactivity','Sub Activity')
    #                            readonly=True, store=True)
    user_id = fields.Many2one('res.users', string='Sub Activity User',related='product_ids.user_id', store=True)
    status= fields.Selection([('pending','Pending'),('hold','On Hold'),('done','Done')])
   

