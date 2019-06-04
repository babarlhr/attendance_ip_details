# -*- coding: utf-8 -*-

from odoo import api, fields, models
import requests
from odoo.http import request
from odoo import http
import uuid 
import os
import platform
import socket


class HrAttendance(models.Model):
    _inherit = 'hr.attendance'

    user_location = fields.Char(
        'Location', 
        readonly=True, 
        copy=False
    )
    user_ip_address = fields.Char(
        string="IP Address", 
        readonly=True, 
        copy=False
    )
    user_last_logged_browser = fields.Char(
        string='Browser', 
        readonly=True, 
        copy=False
    )
    user_last_logged_os = fields.Char(
        string='OS', 
        readonly=True, 
        copy=False
    )
    mac_address = fields.Char(
        string='MAC', 
        readonly=True, 
        copy=False
    )
    user_api = fields.Text(
        string='USER API', 
        readonly=True, 
        copy=False
    )
    custom_device_user_agent = fields.Char(
        String="Device Info"
    )
    user_location_checkout = fields.Char(
        'Location', 
        readonly=True, 
        copy=False
    )
    user_ip_address_checkout = fields.Char(
        string="IP Address", 
        readonly=True, 
        copy=False
    )
    user_last_logged_browser_checkout = fields.Char(
        string='Browser', 
        readonly=True, 
        copy=False
    )
    user_last_logged_os_checkout = fields.Char(
        string='OS', 
        readonly=True, 
        copy=False
    )
    mac_address_checkout = fields.Char(
        string='MAC', 
        readonly=True, 
        copy=False
    )
    user_api_checkout = fields.Text(
        string='USER API', 
        readonly=True, 
        copy=False
    )
    custom_device_user_agent_checkout = fields.Char(
        String="Device Info"
    )

    @api.multi
    def write(self, vals):
        res = super(HrAttendance, self).write(vals)
        if vals.get('check_out', False):
            for result in self:
                try:
                    browser_name = request.httprequest.user_agent.browser
        #             request_ip = http.request.httprequest.remote_addr
                    custom_mac = hex(uuid.getnode())
                    base_url = self.env['ir.config_parameter'].get_param('web.base.url')
                    gw = os.popen("ip -4 route show default").read().split()
                    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    s.connect((gw[2], 0))
                    ipaddr = s.getsockname()[0]
                    
                    wsgienv = request.httprequest.environ
                    env = dict(
                     HTTP_HOST=wsgienv['HTTP_HOST'],
                     REMOTE_ADDR=wsgienv['REMOTE_ADDR'],
                     )
                    ipaddress = env['REMOTE_ADDR']
                    
                    
                    url = 'http://ip-api.com/json/'
                    r = requests.get(url)
                    js = r.json()
                    city = js['city']
                    zip = js['zip']
                    regionname = js['regionName']
                    country = js['country']
                    address = city + ', ' + regionname +', ' + zip + ', ' + country
                    
                    result.user_location_checkout = address
                    result.user_ip_address_checkout = ipaddress
                    result.user_last_logged_browser_checkout = browser_name
                    result.mac_address_checkout = custom_mac
                    result.user_last_logged_os_checkout = platform.system()
                    result.user_api_checkout = js
                    result.custom_device_user_agent_checkout = http.request.httprequest.user_agent or ''
                except:
                    pass
        return res

    @api.model
    def create(self, vals):
        result = super(HrAttendance, self).create(vals)
        try:
            browser_name = request.httprequest.user_agent.browser
#             request_ip = http.request.httprequest.remote_addr
            custom_mac = hex(uuid.getnode())
            base_url = self.env['ir.config_parameter'].get_param('web.base.url')
            gw = os.popen("ip -4 route show default").read().split()
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect((gw[2], 0))
            ipaddr = s.getsockname()[0]
            
            wsgienv = request.httprequest.environ
            env = dict(
             HTTP_HOST=wsgienv['HTTP_HOST'],
             REMOTE_ADDR=wsgienv['REMOTE_ADDR'],
             )
            ipaddress = env['REMOTE_ADDR']
            
            
            url = 'http://ip-api.com/json/'
            r = requests.get(url)
            js = r.json()
            city = js['city']
            zip = js['zip']
            regionname = js['regionName']
            country = js['country']
            address = city + ', ' + regionname +', ' + zip + ', ' + country
            
            result.user_location = address
            result.user_id = self.env.user.id
            result.user_ip_address = ipaddress
            result.user_last_logged_browser = browser_name
            result.mac_address = custom_mac
            result.user_last_logged_os = platform.system()
            result.user_api = js
            result.custom_device_user_agent = http.request.httprequest.user_agent or ''
        except:
            pass
        return result
