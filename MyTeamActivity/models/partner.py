# add button to the Partner to show the number of activity of the person
class MainPartner(models.Model):
    _inherit = 'res.partner'

    activity_count = fields.Integer(compute='_compute_activity_count')

    # activity_id=fields.One2many('main','partner_id')

    @api.multi
    def _compute_activity_count(self):
        for partner in self:
            operator = 'child_of'
            partner.activity_count = self.env['reminder'].search_count([('customer_name', operator, partner.id)])

# Add Mutiple service in partner form
class AddServices(models.Model):
    _inherit = 'res.partner'

    activity_tags = fields.Many2many('activity.category', 'tag_ids', string="Services")
