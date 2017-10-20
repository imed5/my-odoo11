# -*- coding: utf-8 -*-

from odoo import api, models,fields
from odoo.exceptions import UserError  
from odoo.tools import float_is_zero, float_compare, pycompat
from odoo import exceptions
import logging
_logger = logging.getLogger(__name__)

class MyInvoice(models.Model):
	_inherit = "account.invoice"
	pay_stamp_duty=fields.Boolean(string='Pay Stamp Duty',default=True, required=True)
	stamp_fee=fields.Monetary(string='Stamp Fee', default=0, required=True)



	@api.one
	@api.depends(
		'state', 'currency_id', 'invoice_line_ids.price_subtotal',
		'move_id.line_ids.amount_residual',
		'move_id.line_ids.currency_id')

	def _compute_residual(self):
		super(MyInvoice, self)._compute_residual()
		fee=float(self.env['ir.config_parameter'].get_param('default.stamp.duty.fee'))
		stamp_type=self.env['ir.config_parameter'].get_param('stamp.duty.stamp.fee.fixed.or.perc')			
		self.stamp_fee=fee
		if self.residual>0 and self.pay_stamp_duty:
			_logger.debug('\n\n\nCOmputing the Stamp Duty\n\n\n')
			_logger.debug(stamp_type)
			if stamp_type=='Percent':
				_logger.debug('\n\n\n\n PERCENT RESI : '+str(self.residual)+'\t\t Def Fee '+str(fee))
				fee=fee*self.residual/100
				_logger.debug(fee)
			self.stamp_fee=fee
			self.residual=self.residual+fee
			_logger.debug('\n\n\n\n FIXED : '+str(self.residual)+'\t\t Def Fee '+str(fee))
			sign = self.type in ['in_refund', 'out_refund'] and -1 or 1
			self.residual_signed = abs(self.residual) * sign
			digits_rounding_precision = self.currency_id.rounding
			recon=False
			if float_is_zero(self.residual, precision_rounding=digits_rounding_precision):
				recon = True

			self.write({
				'stamp_fee': fee,
			})	
			
			#self.write({
			#	'reconciled':recon,
			#	'stamp_fee': fee,
			#	'residual': self.residual,
			#	'residual_signed': abs(self.residual) * sign,
			#})	

	@api.one
	def stamp_duty_remove_fee(self):
		super(MyInvoice, self)._compute_residual()
		self.write({
			'residual': self.residual,
			'pay_stamp_duty':False,
		})		

	@api.one
	def stamp_duty_add_fee(self):
		_logger.debug('\n\n\nCALL B : COmputing the Stamp Duty\n\n\n')
		self.pay_stamp_duty=True
		super(MyInvoice, self)._compute_residual()
		if self.residual>0:
			sign = self.type in ['in_refund', 'out_refund'] and -1 or 1
			fee=float(self.env['ir.config_parameter'].get_param('default.stamp.duty.fee'))
			stamp_type=self.env['ir.config_parameter'].get_param('stamp.duty.stamp.fee.fixed.or.perc')
			_logger.debug(stamp_type)
			if stamp_type=='Percent':
				_logger.debug('\n\n\n\n HERE Hee')
				fee=fee*self.residual/100
				_logger.debug(fee)

			digits_rounding_precision = self.currency_id.rounding
			self.residual=self.residual+fee
			recon=False
			if float_is_zero(self.residual, precision_rounding=digits_rounding_precision):
				recon = True

			self.write({
				'reconciled':recon,
				'stamp_fee': fee,
				'residual': self.residual,
				'residual_signed': abs(self.residual) * sign,
				'pay_stamp_duty':True,
			})	
