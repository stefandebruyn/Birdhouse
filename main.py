from flask import Flask, request, render_template, send_from_directory, url_for, jsonify, redirect, send_file
import os
from rev_ai.speechrec import RevSpeechAPI
import random
import string
from interpreter.parsing import parse
import requests
from xml_parser import xml_parse
from urllib.request import urlopen, quote
from flask_googlemaps import GoogleMaps, Map

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "temporary_uploads"
app.config['GOOGLEMAPS_KEY'] = "AIzaSyB9QanEBVf2jJZH1-0uTvHXf39Su026rEY"

# Initialize the extension
GoogleMaps(app)


us_state_abbrev = {
    'alabama': 'AL',
    'alaska': 'AK',
    'arizona': 'AZ',
    'arkansas': 'AR',
    'california': 'CA',
    'colorado': 'CO',
    'connecticut': 'CT',
    'delaware': 'DE',
    'florida': 'FL',
    'georgia': 'GA',
    'hawaii': 'HI',
    'idaho': 'ID',
    'illinois': 'IL',
    'indiana': 'IN',
    'iowa': 'IA',
    'kansas': 'KS',
    'kentucky': 'KY',
    'louisiana': 'LA',
    'maine': 'ME',
    'maryland': 'MD',
    'massachusetts': 'MA',
    'michigan': 'MI',
    'minnesota': 'MN',
    'mississippi': 'MS',
    'missouri': 'MO',
    'montana': 'MT',
    'mebraska': 'NE',
    'nevada': 'NV',
    'new hampshire': 'NH',
    'new jersey': 'NJ',
    'new mexico': 'NM',
    'new york': 'NY',
    'north carolina': 'NC',
    'north dakota': 'ND',
    'ohio': 'OH',
    'oklahoma': 'OK',
    'oregon': 'OR',
    'pennsylvania': 'PA',
    'rhode island': 'RI',
    'south carolina': 'SC',
    'south dakota': 'SD',
    'tennessee': 'TN',
    'texas': 'TX',
    'utah': 'UT',
    'vermont': 'VT',
    'virginia': 'VA',
    'washington': 'WA',
    'west virginia': 'WV',
    'wisconsin': 'WI',
    'wyoming': 'WY',
}


# Send main page
@app.route('/')
def hello_world():
    return app.send_static_file("homepage.html")


@app.route('/pls/')
def pls():

    map_data = [{'id': '343608', 'name': 'Midtown', 'zindex': '1971800', 'url': 'http://www.zillow.com/local-info/CA-Palo-Alto/Midtown/r_343608/', 'latitude': '37.434832', 'longitude': '-122.12517'}, {'id': '343613', 'name': 'Barron Park', 'zindex': '2190900', 'url': 'http://www.zillow.com/local-info/CA-Palo-Alto/Barron-Park/r_343613/', 'latitude': '37.412104', 'longitude': '-122.134747'}, {'id': '343609', 'name': 'Crescent Park', 'zindex': '3510500', 'url': 'http://www.zillow.com/local-info/CA-Palo-Alto/Crescent-Park/r_343609/', 'latitude': '37.452918', 'longitude': '-122.149127'}, {'id': '343621', 'name': 'University South', 'zindex': '1845500', 'url': 'http://www.zillow.com/local-info/CA-Palo-Alto/University-South/r_343621/', 'latitude': '37.444538', 'longitude': '-122.153688'}, {'id': '343620', 'name': 'Duveneck - St. Francis', 'zindex': '2320400', 'url': 'http://www.zillow.com/local-info/CA-Palo-Alto/Duveneck----St.-Francis/r_343620/', 'latitude': '37.448756', 'longitude': '-122.130439'}, {'id': '343611', 'name': 'Old Palo Alto', 'zindex': '3577100', 'url': 'http://www.zillow.com/local-info/CA-Palo-Alto/Old-Palo-Alto/r_343611/', 'latitude': '37.435114', 'longitude': '-122.144543'}, {'id': '343610', 'name': 'Downtown North', 'zindex': '1659000', 'url': 'http://www.zillow.com/local-info/CA-Palo-Alto/Downtown-North/r_343610/', 'latitude': '37.448571', 'longitude': '-122.163578'}, {'id': '343606', 'name': 'Ventura', 'zindex': '1348400', 'url': 'http://www.zillow.com/local-info/CA-Palo-Alto/Ventura/r_343606/', 'latitude': '37.421373', 'longitude': '-122.13267'}, {'id': '343607', 'name': 'Charleston Meadow', 'zindex': '1655100', 'url': 'http://www.zillow.com/local-info/CA-Palo-Alto/Charleston-Meadow/r_343607/', 'latitude': '37.412003', 'longitude': '-122.121766'}, {'id': '416707', 'name': 'South of Midtown', 'zindex': '2001900', 'url': 'http://www.zillow.com/local-info/CA-Palo-Alto/South-of-Midtown/r_416707/', 'latitude': '37.423376', 'longitude': '-122.123063'}, {'id': '416174', 'name': 'The Greenhouse', 'url': 'http://www.zillow.com/local-info/CA-Palo-Alto/The-Greenhouse/r_416174/', 'latitude': '37.419103', 'longitude': '-122.103579', '/region': ''}, {'id': '416399', 'name': 'Palo Verde', 'zindex': '2221400', 'url': 'http://www.zillow.com/local-info/CA-Palo-Alto/Palo-Verde/r_416399/', 'latitude': '37.430558', 'longitude': '-122.113954'}, {'id': '416706', 'name': 'Greenmeadow', 'zindex': '1888100', 'url': 'http://www.zillow.com/local-info/CA-Palo-Alto/Greenmeadow/r_416706/', 'latitude': '37.414018', 'longitude': '-122.10995'}, {'id': '416178', 'name': 'College Terrace', 'zindex': '1790000', 'url': 'http://www.zillow.com/local-info/CA-Palo-Alto/College-Terrace/r_416178/', 'latitude': '37.421832', 'longitude': '-122.151633'}, {'id': '343612', 'name': 'Evergreen Park', 'zindex': '1138400', 'url': 'http://www.zillow.com/local-info/CA-Palo-Alto/Evergreen-Park/r_343612/', 'latitude': '37.428004', 'longitude': '-122.14602'}, {'id': '416175', 'name': 'Adobe Meadow - Meadow Park', 'zindex': '1947700', 'url': 'http://www.zillow.com/local-info/CA-Palo-Alto/Adobe-Meadow----Meadow-Park/r_416175/', 'latitude': '37.425963', 'longitude': '-122.109414'}, {'id': '343617', 'name': 'Fairmeadow', 'url': 'http://www.zillow.com/local-info/CA-Palo-Alto/Fairmeadow/r_343617/', 'latitude': '37.419375', 'longitude': '-122.116706', '/region': ''}, {'id': '343614', 'name': 'Green Acres', 'zindex': '2204300', 'url': 'http://www.zillow.com/local-info/CA-Palo-Alto/Green-Acres/r_343614/', 'latitude': '37.406181', 'longitude': '-122.129827'}, {'id': '343619', 'name': 'Jordan Jr. Hgh School', 'zindex': '2889100', 'url': 'http://www.zillow.com/local-info/CA-Palo-Alto/Jordan-Jr.-Hgh-School/r_343619/', 'latitude': '37.440166', 'longitude': '-122.135682'}, {'id': '416177', 'name': 'Community Center', 'zindex': '2938300', 'url': 'http://www.zillow.com/local-info/CA-Palo-Alto/Community-Center/r_416177/', 'latitude': '37.445459', 'longitude': '-122.145769'}, {'id': '343616', 'name': 'Charleston Gardens', 'url': 'http://www.zillow.com/local-info/CA-Palo-Alto/Charleston-Gardens/r_343616/', 'latitude': '37.418811', 'longitude': '-122.105379', '/region': ''}, {'id': '343623', 'name': 'Professorville', 'url': 'http://www.zillow.com/local-info/CA-Palo-Alto/Professorville/r_343623/', 'latitude': '37.442354', 'longitude': '-122.150949', '/region': ''}, {'id': '416705', 'name': 'Monroe Park', 'url': 'http://www.zillow.com/local-info/CA-Palo-Alto/Monroe-Park/r_416705/', 'latitude': '37.407507', 'longitude': '-122.11634', '/region': ''}, {'id': '416704', 'name': 'Palo Alto Orchards', 'url': 'http://www.zillow.com/local-info/CA-Palo-Alto/Palo-Alto-Orchards/r_416704/', 'latitude': '37.406367', 'longitude': '-122.123785', '/region': ''}, {'id': '343618', 'name': 'Triple El', 'url': 'http://www.zillow.com/local-info/CA-Palo-Alto/Triple-El/r_343618/', 'latitude': '37.443286', 'longitude': '-122.13008', '/region': ''}, {'id': '343622', 'name': 'Southgate', 'url': 'http://www.zillow.com/local-info/CA-Palo-Alto/Southgate/r_343622/', 'latitude': '37.432729', 'longitude': '-122.151194', '/region': ''}, {'id': '416708', 'name': 'St. Claire Gardens', 'url': 'http://www.zillow.com/local-info/CA-Palo-Alto/St.-Claire-Gardens/r_416708/', 'latitude': '37.426399', 'longitude': '-122.121053', '/region': ''}, {'id': '343615', 'name': 'Esther Clark Park', 'url': 'http://www.zillow.com/local-info/CA-Palo-Alto/Esther-Clark-Park/r_343615/', 'latitude': '37.395483', 'longitude': '-122.135007', '/region': ''}, {'id': '416176', 'name': 'Greater Miranda', 'url': 'http://www.zillow.com/local-info/CA-Palo-Alto/Greater-Miranda/r_416176/', 'latitude': '37.394358</latitude><longitude>-122.13056</longitude></region></list></response></RegionChildren:regionchildren>'}]

    coords = []
    for i in range(len(map_data) - 2):
        coords.append((map_data[i]["latitude"], map_data[i]["longitude"]))

    markers = []
    for i in range(len(coords)):
        markers.append({
            'lat': coords[i][0],
            'lng': coords[i][1],
            'infobox': '<a target="_blank" href="' + map_data[i]["url"] + '">' + map_data[i]["name"] + "</p>"
        })

    map = Map(
        identifier="sndmap",
        lat=coords[0][0],
        lng=coords[0][1],
        markers=markers,
        style="height:100vh;width:75vw;margin:0;"
    )

    return render_template('result.html', map=map, data=map_data)


# Takes an audio file, returns transcribed text
@app.route('/upload/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        print(request.files)

        try:
            # This should only have one file...
            for file in request.files:
                new_file = request.files[file]


                print("three")

                temp_key = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
                file_type = new_file.filename.rsplit('.', 1)[1].lower()

                new_file.save(os.path.join(app.config['UPLOAD_FOLDER'], temp_key + "." + file_type))

                rev = RevSpeechAPI(
                    "01ISeiBst2n0yC_kC0Xy5L5IhKHAzy4Sc4y2IPGa6qBiUmiLiHIZGTuZupqDJ1z15xPSywWNjblQLtW96HHIYJWuLzQEs"
                )

                # Get ID from rev_ai
                upload_id = rev.submit_job_local_file(os.path.join(
                    app.config['UPLOAD_FOLDER'], temp_key + "." + file_type))["id"]

                # Keep checking if job is finished, break out of loop when true
                complete = False
                while complete is False:
                    if "failure" in rev.view_job(upload_id):
                        return app.send_static_file("homepage.html")
                    if rev.view_job(upload_id)["status"] == 'transcribed':
                        complete = True
                    else:
                        print(rev.view_job(upload_id))

                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], temp_key + "." + file_type))

                rev_string = rev.get_transcript(upload_id, use_json=False)
                parsed_info = parse(rev_string)

                zillow_link = make_zillow_call(construct_house_dict(parsed_info))

                xml_text = requests.get(zillow_link).text

                sexy_fucking_string = add_lines(xml_text)

                file = open('temp_xml/' + temp_key + '.xml', 'w')
                file.write(sexy_fucking_string)
                file.close()

                map_data = xml_parse('temp_xml/' + temp_key + '.xml')

                os.remove('temp_xml/' + temp_key + '.xml')

                print(map_data)

                coords = []

                for i in range(len(map_data) - 2):
                    coords.append((map_data[i]["latitude"], map_data[i]["longitude"]))

                markers = []
                for i in range(len(coords)):
                    markers.append({
                        'lat': coords[i][0],
                        'lng': coords[i][1],
                        'infobox': '<a target="_blank" href="' + map_data[i]["url"] + '">' + map_data[i]["name"] + "</p>"
                    })

                if len(coords) == 0:
                    initial_lat = 0
                    initial_lng = 0
                else:
                    initial_lat = coords[0][0]
                    initial_lng = coords[0][1]

                map = Map(
                    identifier="sndmap",
                    lat=initial_lat,
                    lng=initial_lng,
                    markers=markers,
                    style="height:100vh;width:75vw;margin:0;"
                )

                return render_template('result.html', map=map, data=map_data)
        except Exception:
            return app.send_static_file("homepage.html")

    return "An error occurred"


def construct_house_dict(parsed_info):

    house_dict = {}

    for i in parsed_info:
        house_dict[i[0]] = i[1]

    return house_dict


def make_zillow_call(house_info):

    city = ""
    state = ""

    if "city" in house_info:
        city = "&city=" + house_info["city"]

    if "state" in house_info:
        state = "&state=" + us_state_abbrev[house_info["state"]]
        state = state.replace(" ", "%20")

    url = "http://www.zillow.com/webservice/GetRegionChildren.htm?zws-id=X1-ZWz18axyxyo1sb_3e7gq" + \
        city + state + "&childtype=neighborhood"

    return url


def add_lines(big_fucking_string):

    for i in range(len(big_fucking_string)):
        if big_fucking_string[i] == '>' and big_fucking_string[i + 1] == '<':
            big_fucking_string = big_fucking_string[0:i + 1] + "\n" + big_fucking_string[i+1:]

    return big_fucking_string
