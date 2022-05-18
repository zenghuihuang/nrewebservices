#!/usr/bin/env python3
#
# Get nrewebservices into the python import path. You do not need to do this in your own script.
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/../')

#
# This file contains an example of how to make a very basic use of this library to query all the
# departures at a station using the LDBWS API. For more detailed information on how to use this
# library, and all the web services, API endpoints and objects and properties that you can use
# with this library, please see the API docs at http://nrewebservices.readthedocs.org
#

####################################################################################################
# Load the configuration.

# Set up the address for the LDBWS server.
API_URL = "https://lite.realtime.nationalrail.co.uk/OpenLDBWS/wsdl.aspx?ver=2016-02-16"

# Get the API key from the environment
try:
    API_KEY = os.environ['NRE_LDBWS_API_KEY']
except KeyError:
    print()
    print("To run this example you need to set the environment variable NRE_LDBWS_API_KEY to your")
    print("NRE OpenLDBWS API Key. For example:")
    print()
    print("    export NRE_LDBWS_API_KEY=my-ldbws-api-key")
    print()
    print("To get a key, please see the NREWebServices documentation.")
    print()
    sys.exit(1)

####################################################################################################
# An example of getting a regular departure board.

# Import the ldbws session class.
from nrewebservices.ldbws import Session

# Instantiate the web service session.
session = Session(API_URL, API_KEY)

# Get a departure board containing the next ten departures from Reading.
board = session.get_station_board("ZFD", rows=150, include_departures=True, include_arrivals=False)

print("Trains departing late between 5 - 22 pm from {} to Brighton are:".format(board.location_name))

# Loop over all the train services in that board.
for service in board.train_services:
    
    # Print some basic information about that train service.
    # if str(service.etd) == 'On time':
    scheduledTime = str(service.std)
    if scheduledTime[0:2] == '20' or scheduledTime[0:2] == '22':
        if str(service.destination) == 'Brighton' and str(service.etd) != 'On time':
            print(" Train {} to {}: due {}.".format(
                service.std,
                service.destination,
                service.etd
            ))

print()

####################################################################################################
# An example of getting the Next Departures to various locations board.

# Import the ldbws session class.
from nrewebservices.ldbws import Session

# Instantiate the web service session.
session = Session(API_URL, API_KEY)

# Get a the next departures from Reading to Paddington and Oxford.
board = session.get_next_departures("ZFD", ["BTN"])

print("The next departures from {} to Brighton are as follows:".format(board.location_name))

# Loop over the departures.
for departure in board.next_departures:

    # Build a list of destinations for each train service.
    destinations = [destination.location_name for destination in departure.service.destinations]

    # Print some basic information about that train service.
    print("    {} to {}: due {}.".format(
        departure.service.std,
        ",".join(destinations),
        departure.service.etd
    ))

print()
