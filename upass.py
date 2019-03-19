#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Web crawler for sfu upass auto-renew."""

__author__ = 'Chong Guo <armourcy@gmail.com>'
__copyright__ = 'Copyright 2018, Chong Guo'
__license__ = 'MIT'

import os
import json
import urllib3
import requests

from lxml import html, etree
from typing import Dict, List

IFTTT_URL = 'https://maker.ifttt.com/trigger/{event}/with/key/{key}'


class UPass():
    def __init__(self):
        self._load_config()
        # Disable SSL Warnings
        urllib3.disable_warnings()

    def _load_config(self):
        with open(os.path.dirname(os.path.realpath(__file__)) + '/config.json') as config:
            config_data: Dict[str, str] = json.load(config)
            self._sfu_usr_pass: Dict[str, str] = {
                'username': config_data['username'],
                'password': config_data['password']
            }
            # IFTTT is optional config
            self._ifttt: Dict[str, str] = {
                'event_name': config_data.get('ifttt_event', ''),
                'key': config_data.get('ifttt_key', '')
            }

    def request(self):
        try:
            self._request_upass()
        except AssertionError as e:
            print("Error encountered. {error}".format(error=e))
            if self._ifttt['event_name'] and self._ifttt['key']:
                self._send_ifttt_message(status=False)

    def _send_ifttt_message(self, status):
        url = IFTTT_URL.format(event=self._ifttt['event_name'], key=self._ifttt['key'])
        url += '?value1={value1}'.format(value1='succeeded' if status else 'failed')
        response = requests.get(url)
        assert (response.status_code == 200)

    def _request_upass(self):
        r = requests.Session()

        # Get upassbc website
        r1 = r.get('https://upassbc.translink.ca/', verify=False)
        assert (r1.status_code == 200)
        assert (r1.url == 'https://upassbc.translink.ca/')

        # Select school, default here sfu
        r2 = r.post('https://upassbc.translink.ca/', data={'PsiId': 'sfu'}, verify=False)
        assert (r2.status_code == 200)
        assert (r2.url.startswith('https://cas.sfu.ca/cas/login'))

        # Parse signin form, get all the hidden fields, combined them with username and password in the config file
        tree = html.fromstring(r2.content)
        form = tree.find('.//form')
        hidden_fields = form.findall('.//input[@type="hidden"]')

        sfu_data: Dict[str, str] = self._sfu_usr_pass
        for hidden_field in hidden_fields:
            sfu_data[hidden_field.name] = hidden_field.value
        # Signin post request
        r3 = r.post('https://cas.sfu.ca/cas/{action}'.format(action=form.action), data=sfu_data)
        assert (r3.status_code == 200)
        assert (r3.url.startswith('https://idp.sfu.ca/idp/profile'))

        # Below request r4 and r5 are due to python requests library doesn't load javascript in the webpage,
        # there are javascript to automatically submit those two forms in the webpage, here we mannally do it
        tree = html.fromstring(r3.content)
        form = tree.find('.//form')
        fields = form.findall('.//input')
        translink_data = {}
        for field in fields:
            translink_data[field.name] = field.value
        r4 = r.post('https://upassadfs.translink.ca/adfs/ls/', data=translink_data, verify=False)
        assert (r4.status_code == 200)
        assert (r4.url == 'https://upassadfs.translink.ca/adfs/ls/')

        tree = html.fromstring(r4.content)
        form = tree.find('.//form')
        fields = form.findall('.//input')
        data = {}
        for field in fields:
            data[field.name] = field.value
        r5 = r.post('https://upassbc.translink.ca/fs/', data=data, verify=False)
        assert (r5.status_code == 200)
        assert (r5.url == 'https://upassbc.translink.ca/fs/')

        # Check if there are new month eligibility need to request
        tree = html.fromstring(r5.content)
        form = tree.find('.//form[@action="/fs/Eligibility/Request"]')
        hidden_fields = form.findall('.//input[@type="hidden"]')
        checkbox_fields = form.findall('.//input[@type="checkbox"]')
        data = {}
        for hidden_field in hidden_fields:
            data[hidden_field.name] = hidden_field.value
        for checkbox_field in checkbox_fields:
            data[checkbox_field.name] = 'true'
        if len(checkbox_fields) == 0:
            print('😅 There is no new request available yet.')
        else:
            # Request eligibility
            print('🧐 Start requesting new month eligibility...')
            r6 = r.post('https://upassbc.translink.ca/fs/Eligibility/Request/', data=data, verify=False)
            assert (r6.status_code == 200)

            # Check if we request successful
            tree = html.fromstring(r6.content)
            form = tree.find('.//form[@action="/fs/Eligibility/Request"]')
            checkbox_fields = form.findall('.//input[@type="checkbox"]')
            if len(checkbox_fields) == 0:
                print('🎉 Request successful!')
            else:
                print('😰 Request failed...')


if __name__ == '__main__':
    upass = UPass()
    upass.request()
