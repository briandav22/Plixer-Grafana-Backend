from flask import Flask
import scrutapi
import dataconnector
from flask import jsonify, request
import json



app = Flask(__name__)

panels = ['srcHosts', 'applications', 'srcCountries',  
            'dstHosts', 'topMacsSrc', 'newSrcAs', 'dstdomains',
            'srcdomains', 'newDstAs'] #sample list, add or remove whatever you like. 

exporter = dataconnector.get_exporters() #finds all exporters scrutinizer has available. 

exporter.append('all')

@app.route('/') #used for testing

def homepage():
    return 'congrats, your data source is working!'

@app.route('/search', methods=['POST']) 

def search():
    return jsonify(panels) #whatever is in the panels list will be available as a report type in grafana. 

@app.route('/exporters', methods=['POST']) 

def exporters():
    return jsonify(exporter) #send back a list of exporters 


@app.route('/query', methods=['POST']) # returns timeseries and object names (only what is in request data)

def query():
    data_to_graph = [] # items to graph get stored here. 
    grafana_post_request = request.get_json() #turns the grafana request into a JSON object
    start_time = scrutapi.hyphen_split(grafana_post_request['range']['from']) #grabs start time from grafana, converts to epoch for scrutinizer
    end_time = scrutapi.hyphen_split(grafana_post_request['range']['to']) #grabs end time from grafana, converts to epoch for scrutinizer
    
    for items in grafana_post_request['targets']: #loops through all off your rpt_langs and builds a list to pass to grafana
        report_lang = items['target']
        if items['exporter'] == 'all': # time works different for all devices, so we take a different track. 
            json_from_scrut = scrutapi.build_request(report_lang, start_time, end_time, 'in_GROUP_ALL')
            if 'error' in json_from_scrut['report']:
                print(json_from_scrut['report']['error'])
            else:
                data_for_grafana = scrutapi.graphing_data(json_from_scrut, 'all')
                data_to_graph.append(data_for_grafana)            
        elif items['exporter'] != 'select exporter': #
            exporter = dataconnector.convert_exporter(items['exporter'])
            json_from_scrut = scrutapi.build_request(report_lang, start_time, end_time, exporter)
            if 'error' in json_from_scrut['report']:
                print(json_from_scrut['report']['error'])
            else:
                data_for_grafana = scrutapi.graphing_data(json_from_scrut, exporter)
                data_to_graph.append(data_for_grafana)
        else:
            print('select and exporter!')
    
    data_to_graph = [item for items in data_to_graph for item in items]
    return jsonify(data_to_graph)

    
        
        
        


     #flattens out the list 

     #sends JSON back to graphana to be graphed

app.run(host="0.0.0.0") #fires up the server.
