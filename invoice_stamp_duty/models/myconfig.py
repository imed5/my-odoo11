from odoo import api, models,fields
from odoo.exceptions import UserError
from odoo import exceptions
import logging 
_logger = logging.getLogger(__name__)


PARAMS = [
    ("stamp_fee_fixed_or_perc", "stamp.duty.stamp.fee.fixed.or.perc"),
]


class StampDutyConfig(models.TransientModel):
	_inherit = 'res.config.settings'
	_name = 'stamp.duty.config'

	default_stamp_duty_fee = fields.Float(string='Stamp Duty value',default=0, required=True)
	stamp_fee_fixed_or_perc    = fields.Selection([('Fixed','Fixed Value'),('Percent','Percentage of the Total')],required=True)




	@api.model
	def get_values(self):
		res = super(StampDutyConfig, self).get_values()
		params = self.env['ir.config_parameter'].sudo()
		res.update(
			stamp_fee_fixed_or_perc=params.get_param('stamp.duty.stamp.fee.fixed.or.perc'),
			default_stamp_duty_fee=float(params.get_param('default.stamp.duty.fee')),
		)
		return res

	@api.multi
	def set_values(self):
		super(StampDutyConfig, self).set_values()
		self.env['ir.config_parameter'].sudo().set_param("stamp.duty.stamp.fee.fixed.or.perc", self.stamp_fee_fixed_or_perc)      
		self.env['ir.config_parameter'].sudo().set_param("default.stamp.duty.fee", self.default_stamp_duty_fee)      

