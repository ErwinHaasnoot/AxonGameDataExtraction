#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2012 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
"""Simple intro to using the Google Analytics API v3.

This application demonstrates how to use the python client library to access
Google Analytics data. The sample traverses the Management API to obtain the
authorized user's first profile ID. Then the sample uses this ID to
contstruct a Core Reporting API query to return the top 25 organic search
terms.

Before you begin, you must sigup for a new project in the Google APIs console:
https://code.google.com/apis/console

Then register the project to use OAuth2.0 for installed applications.

Finally you will need to add the client id, client secret, and redirect URL
into the client_secrets.json file that is in the same directory as this sample.

Sample Usage:

  $ python hello_analytics_api_v3.py

Also you can also get help on all the command-line flags the program
understands by running:

  $ python hello_analytics_api_v3.py --help
"""

__author__ = 'api.nickm@gmail.com (Nick Mihailovski)'

import argparse
import sys

from apiclient.errors import HttpError
from apiclient import sample_tools
from oauth2client.client import AccessTokenRefreshError


def main(argv):
  # Authenticate and construct service.
  service, flags = sample_tools.init(
      argv, 'analytics', 'v3', __doc__, __file__,
      scope='https://www.googleapis.com/auth/analytics.readonly')

  # Try to make a request to the API. Print the results or handle errors.
  try:
    first_profile_id = get_first_profile_id(service)
    if not first_profile_id:
      print 'Could not find a valid profile for this user.'
    else:
      get_all_data(service, first_profile_id)
      #print_results(results)

  except TypeError, error:
    # Handle errors in constructing a query.
    print ('There was an error in constructing your query : %s' % error)

  except HttpError, error:
    # Handle API errors.
    print ('Arg, there was an API error : %s : %s' %
           (error.resp.status, error._get_reason()))

  except AccessTokenRefreshError:
    # Handle Auth errors.
    print ('The credentials have been revoked or expired, please re-run '
           'the application to re-authorize')


def get_first_profile_id(service):
  """Traverses Management API to return the first profile id.

  This first queries the Accounts collection to get the first account ID.
  This ID is used to query the Webproperties collection to retrieve the first
  webproperty ID. And both account and webproperty IDs are used to query the
  Profile collection to get the first profile id.

  Args:
    service: The service object built by the Google API Python client library.

  Returns:
    A string with the first profile ID. None if a user does not have any
    accounts, webproperties, or profiles.
  """

  accounts = service.management().accounts().list().execute()

  if accounts.get('items'):
    firstAccountId = accounts.get('items')[0].get('id')
    webproperties = service.management().webproperties().list(
        accountId=firstAccountId).execute()

    if webproperties.get('items'):
      firstWebpropertyId = webproperties.get('items')[0].get('id')
      profiles = service.management().profiles().list(
          accountId=firstAccountId,
          webPropertyId=firstWebpropertyId).execute()

      if profiles.get('items'):
        return profiles.get('items')[0].get('id')

  return None


def get_all_data(service, profile_id):
    """Executes and returns data from the Core Reporting API.
    
    Args:
      service: The service object built by the Google API Python client library.
      profile_id: String The profile ID from which to retrieve analytics data.
    
    Returns:
      The response returned from the Core Reporting API.
    """
    
    fname = "game_data_21_06_2014.csv"
    fh = open(fname,'w')
    noheader = False
    datestart = 0    
    dates = ['2012-01-01','2012-02-01',
             '2012-03-01',
             '2012-04-01',
             '2012-05-01',
             '2012-06-01',
             '2012-07-01',
             '2012-08-01',
             '2012-09-01',
             '2012-10-01',
             '2012-11-01',
             '2012-12-01',
             '2013-01-01',
             '2013-02-01',
             '2013-03-01',
             '2013-04-01',
             '2013-05-01',
             '2013-06-01',
             '2013-07-01',
             '2013-08-01',
             '2013-09-01',
             '2013-10-01',
             '2013-11-01',
             '2013-12-01',
             '2014-01-01',
             '2014-02-01',
             '2014-03-01',
             '2014-04-01',
             '2014-05-01',
             '2014-06-01',
             '2014-07-01',
             '2014-08-01'
             '2014-09-01']
    for i in xrange(datestart,len(dates)-1):
        startdate = dates[i]
        enddate = dates[i+1]  
        print 'Retrieving events between {} and {}:'.format(startdate,enddate)
        old_count = -1
        count = 0
        start_index = 1
        max_results = 10000
        while old_count != count:
          
            out = service.data().ga().get(
                ids='ga:' + profile_id,
                start_date=startdate,
                end_date=enddate,
                metrics='ga:eventValue',
                dimensions='ga:eventAction,ga:eventLabel,ga:date,ga:hour',
                #sort='-ga:eventAction',
                #filters='ga:city==Leiden',
                start_index='%i' % start_index,
                max_results='%i' % max_results).execute();
            old_count = count
            fh.flush();
            n = print_results(out,fh,noheader)
            
            noheader = True
            count += n
            start_index += n
            print "written %s lines to file total, starting at index %s next"%(count,start_index)
   


def print_results(results, fh = False, noHeader = False):
  """Prints out the results.

  This prints out the profile name, the column headers, and all the rows of
  data.

  Args:
    results: The response returned from the Core Reporting API.
  """
  n = 0
  #print
  #print 'Profile Name: %s' % results.get('profileInfo').get('profileName')
  #print

  # Print header.
  if(noHeader == False):
      output = ['%s' % header.get('name') for header in results.get('columnHeaders')]
      #print ','.join(output)      
      fh.write(','.join(output))

  # Print data table.
  if results.get('rows', []):
    for row in results.get('rows'):
        
      output = ['%s' % cell for cell in row]
      n += 1
      #print ','.join(output)
      fh.write('\n'+ ','.join(output))

  else:
    print 'No Rows Found'

  return n


if __name__ == '__main__':
  main(sys.argv)
