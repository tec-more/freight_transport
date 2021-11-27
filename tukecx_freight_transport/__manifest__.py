# -*- coding: utf-8 -*-
{
  'name': '货运订单',
  'version': '1.0',
  'summary': 'real freight transport',
  'sequence': 10,
  'description': """
    freight transport
    """,
  'author': 'hepan',
  'website': 'https://www.tukecx.com/',
  'depends' : ['base','sale'],
  'data': [
    'security/ir.model.access.csv',
    'views/freight_transport_views.xml',
  ],
  'application': True,
  "images":["static/description/Banner.png"],
}
