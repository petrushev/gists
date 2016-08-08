#!/usr/bin/python
from decimal import Decimal
import exifread

import requests


def parse_coordinates(data):
    degrees, minutes, seconds = data[1:-1].replace(" ","").split(',')[:3]
    degrees = Decimal(degrees)
    minutes = Decimal(minutes)
    seconds = seconds.split('/')
    if len(seconds) == 2:
        seconds = Decimal(seconds[0]) / Decimal(seconds[1])
    else:
        seconds = Decimal(seconds[0])
    result = str(degrees + minutes/60 + seconds/3600)
    return result

def get_coordinates(fh):
    tags = exifread.process_file(fh)
    if tags.get('GPS GPSLatitude') is None:
        print "There isn't geo data located in the supplied image"
        return None
    latitude = parse_coordinates(str(tags.get('GPS GPSLatitude')))
    longitude = parse_coordinates(str(tags.get('GPS GPSLongitude')))
    return latitude, longitude

def fetch_from_google(coordinates):
    if coordinates is None:
        print 'Invalid coordinates'
        return

    #Fetch data
    url = 'https://maps.googleapis.com/maps/api/geocode/json?latlng='+','.join(coordinates)
    data = requests.get(url).json()

    if data['results'] == []:
        print 'No results found!'
        return

    return data['results'][0]['formatted_address']

def main():
    import sys

    if len(sys.argv) < 2:
        print 'Usage: python '+sys.argv[0]+' image_name'
        return

    fname = sys.argv[1]
    try:
        f = open(fname, 'rb')
    except IOError:
        print 'Unable to open image file!'
        return None

    coordinates = get_coordinates(f)
    if coordinates is not None:
        result = fetch_from_google(coordinates)
        if result is not None:
            print fname, '\t', result

if __name__ =="__main__":
    main()
