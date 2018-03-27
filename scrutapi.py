import urllib
import urllib2
import json
from datetime import datetime
import ssl
import findtime

url = 'https://10.30.70.70/fcgi/scrut_fcgi.fcgi'
context = ssl._create_unverified_context()


def build_request(report_type, start, end, exporter):  #function to build out API request to Scrutinizer
     #whatever you pass in as a variable will be used as a report type (i.e 'applications')
    report_details = {
       'reportTypeLang' : report_type, #this is where elements from the panel list is used. 
       'reportDirections' : {
               'selected' : 'inbound'
       },
       'times' : {
        "dateRange": "Custom",
        "start": start, #start time is passed in here
        "end": end, #end time is passed in here
        "clientTimezone": "America/New_York"
       },
       'filters' : {
               'sdfDips_0' : exporter, #uses all devices. 

       },
       'dataGranularity' : {
               'selected' : '1m'
       },

               'rateTotal': {
            'selected': 'rate'
        },
        'bbp': {
            'selected': 'bits'
        },

}
    data_i_need = {
       'inbound' : {
              'graph' : 'timeseries',
              'table' : {
                       'query_limit' : {
                               'offset' : 0,
                               'max_num_rows' : 10
                       }
               }
       },
 }
    data = {
       'rm' : 'report_api',
       'action' : 'get',
       'rpt_json' : json.dumps( report_details ),
       'data_requested' : json.dumps( data_i_need )
}
    data = urllib.urlencode( data )
    req = urllib2.Request( url, data )
    response = urllib2.urlopen( req, context=context)
    report = response.read()
    report_obj = json.loads( report )
    # print(json.dumps(report_obj, indent=4, sort_keys=True)) uncomment for troublsehooting. 
    return report_obj #JSON object is returned from the function




def graphing_data(app, exporter): #parses JSON against what is requested from grafana, only returns what is requested as JSON
    final_list = []

    if exporter == 'all':
      interval = findtime.find_interval_all_device(app)
    else:
      interval = findtime.find_interval_single_device(app)    
    

    for k, v in app.iteritems():
        items = v['graph']['pie']['inbound']
        data_points = v['graph']['timeseries']['inbound']
        for x,y in zip(items,data_points):
            update = [[((t[1] * 8)/interval['time']), (t[0] * 1000)] for t in y] #Scrutinizer sends back TOTAL BYTES. We multiply by 8 for bits
                                                                                #then devide by the interval for Bits / Second. 

            formatted_results = { 'target':x['label'],
                   'datapoints':update}
            final_list.append(formatted_results)


    return final_list

def hyphen_split(a):  #this converts the date / time into epoch for Scrutinizer's API. 
    p = '%Y-%m-%dT%H:%M'
    epoch = datetime(1970, 1, 1)
    if a.count(":") == 1:
        return a.split(":")[0]
    else:
        a = ":".join(a.split(":", 2)[:2])
        return int(((datetime.strptime(a, p) - epoch).total_seconds()))
