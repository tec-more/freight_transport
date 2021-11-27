from datetime import datetime, timedelta
from odoo import models, fields, api, _
from odoo.tools.float_utils import float_compare
import logging
_logger = logging.getLogger(__name__)

class FreightTransport(models.Model):
    _name = 'freight.transport'
    _description = "销售订单货运信息"

    def _default_validity_date(self):
        if self.env['ir.config_parameter'].sudo().get_param('sale.use_quotation_validity_days'):
            days = self.env.company.quotation_validity_days
            if days > 0:
                return fields.Date.to_string(datetime.now() + timedelta(days))
        return False
    #发货日期
    deliver_date = fields.Date(string='发货日期', store=True,default=_default_validity_date)
    #到达日期
    arrival_date = fields.Date(string='到达日期', store=True,default=_default_validity_date)
    #发货单号
    transport_code = fields.Char(string='发货单号', store=True)
    #发货状态
    send_state = fields.Selection([
        ('not_deliver', '未发货'),
        ('pre_deliver', '准备发货'),
        ('shipped', '已发货'),
        ('on_the_way', '在途中'),
        ('arrived', '已到货'),
        ('in_return', '退货中'),
        ('returned', '已退货'),
        ], string='发货状态', store=True, default='not_deliver')
    #发货备注
    note = fields.Text('备注', default='')
    order_id = fields.Many2one('sale.order', string='货运订单',ondelete='cascade', copy=False,store=True)
    name=fields.Char(string='货运订单号', store=True)
    
    #@api.depends("order_id")
    #def _get_order_name(self):
    #    #orders=self.env["sale.order"].search([()])
    #    saleorders=self.env['sale.order'].search([])
    #    for o in self:
    #        #orders=o.env['sale.order'].search([('id','=',o.order_id)])
    #        for t in saleorders:
    #            if t.id == o.order_id:
    #                o.display_name=t.name

class inheritSalesTrans(models.Model):
    _inherit = "sale.order"
    x_ftids = fields.One2many('freight.transport', 'order_id', string='货运ID',copy=False,store=True)
    x_ft_status = fields.Char(string='货运状态',copy=False,store=True,compute="_compute_ft_state")
    
    #@api.depends("x_ftids")
    #def _compute_ft_status(self):
    #    for record in self:
    #        for xid in x_ft_ids:
    #            record.x_ft_status= xid.send_state
    #@api.depends("send_state")
    #def _compute_ft_state(self):
    #    trans=self.env['freight.transport'].search([()])
    #    for record in self:
    #        for tr in trans:
    #            if tr.order_id == record.id:
    #               record.x_ft_status=tr.send_state
    
    @api.depends("x_ftids.send_state")
    def _compute_ft_state(self):
        self.x_ft_status='未发货'
        trans=self.env['freight.transport'].search([])
        for s in self:
            _logger.info('测试订单:%s '%(s))
            for t in trans:
                _logger.info('货运状态:%s,订单id:%s,源订单:%s'%(t.send_state,s.id,t.order_id.id))
                if t.order_id.id == s.id:
                    _logger.info('货运1:%s'%(self.x_ft_status))
                    _logger.info('货运2:%s'%(s.x_ft_status))
                    sd=dict(t.fields_get(allfields=['send_state'])['send_state']['selection'])[t.send_state]
                    _logger.info('货运3:%s'%(sd))
                    s.x_ft_status=sd