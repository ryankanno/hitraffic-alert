# -*- coding: utf-8 -*-

import os
import requests
from eve import Eve
from flask import render_template
from flask import request
from geopy import geocoders
import googlemaps
from polyline import decode_line
import json
from wtforms import Form
from wtforms import TextField
from wtforms import validators
from settings import GOOGLE_API_KEY

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')

if 'PORT' in os.environ:
    port = int(os.environ.get('PORT'))
    host = '0.0.0.0'
else:
    port = 5000
    host = '127.0.0.1'

app = Eve(template_folder=tmpl_dir, static_folder=static_dir)

@app.route('/s', methods=['GET', 'POST'])
def slash():
    if request.method == 'GET':
        form = NumberAddressForm()
        return render_template('slash.html', form=form)
    elif request.method == 'POST':
        form = NumberAddressForm(request.form)
        if form.validate():
            phone = ''.join(e for e in form.phone.data if e.isalnum())
            headers = {'Content-Type': 'application/json'}
            phone_endpoint = 'http://%s:%s/%s/' % (host, port, "phones")
            response = requests.get(phone_endpoint + phone, headers=headers)

            if response.status_code != 200:
                gmaps = googlemaps.Client(key=GOOGLE_API_KEY)
                directions = gmaps.directions(form.home_address.data, form.work_address.data, mode="driving")
                g = geocoders.GoogleV3(GOOGLE_API_KEY)
                home_location_geo = g.geocode(form.home_address.data)
                work_location_geo = g.geocode(form.work_address.data)
                data = form.data
                data["work_address_geo"] = {'type': 'Point', 'coordinates': [work_location_geo.longitude, work_location_geo.latitude]}
                data["home_address_geo"] = {'type': 'Point', 'coordinates': [home_location_geo.longitude, home_location_geo.latitude]}
                response = requests.post(phone_endpoint, json.dumps(data), headers=headers)
                decoded = decode_line(directions[0]["overview_polyline"]["points"])
                stuffs = []
                for decode in decoded:
                    stuffs.append({'phone': phone, 'location': {'type': 'Point', 'coordinates': [decode[1], decode[0]]}})

                route_endpoint = 'http://%s:%s/%s/' % (host, port, "routes")
                response = requests.post(route_endpoint, json.dumps(stuffs), headers=headers)
                return render_template('success.html')
            else:
                return render_template('already_registered.html')
        return render_template('slash.html', form=form)


class NumberAddressForm(Form):
    phone = TextField(u'Phone Number', [validators.required(), validators.length(max=11)])
    home_address = TextField(u'Home Address', [validators.required()])
    work_address = TextField(u'Work Address', [validators.required()])


if __name__ == '__main__':
    app.run(host=host, port=port, threaded=True)
