from django.http import HttpResponse
from django.shortcuts import render

from django.template import RequestContext, loader
from pprint import pprint

from tools import utils

import datetime as dt
import dateutil.parser

import boto.ec2,json

from django.views.decorators.csrf import csrf_exempt

from ec2_spot_price_monitor.models import ImageType,InstanceType

from ec2_api_tools import spot_price_api

@csrf_exempt
def request_spot_price(request):
    #get spot price using ec2 tools
    #conn = boto.connect_ec2()
    jsonMsg = request.POST['jsonMsg']
    #pprint(jsonMsg)
    json_req = json.loads(jsonMsg)
    #boto.conn
    json_response_data = []
    
    if json_req['request'] == 'current_spot_price':
        json_req['start_time'] = dt.datetime.now().isoformat()
        json_req['end_time'] = dt.datetime.now().isoformat()
        json_response_data = spot_price_api.get_current_spot_price(json_req)
        json_response_data = utils.filter_response(json_response_data, json_req['filter_type'])
    elif json_req['request'] == 'list_all_spot_price':  
        json_req['start_time'] = (dt.datetime.now()-dt.timedelta(hours=json_req['other_args']['job_exe_time'])).isoformat()
        json_req['end_time'] = dt.datetime.now().isoformat()
        json_response_data = spot_price_api.get_current_spot_price(json_req) 
        json_response_data = utils.filter_response(json_response_data, json_req['filter_type'])
    elif json_req['request'] == 'periodic_spot_price':  
        pprint("Get Periodic Spot Prices")  
        args = json_req['other_args']
        
        start_date = dateutil.parser.parse(args['job_start_time'])
        stop_date = dateutil.parser.parse(args['job_stop_time'])
        job_exec_time = args['job_exec_time']
        job_period_time = args['job_period_time']
        #pprint("%s %s %s %s"%(start_date,stop_date,job_exec_time,job_period_time))
        
        curr_date = start_date
        while curr_date < stop_date:
            curr_stop_date = curr_date + dt.timedelta(hours=job_exec_time)
            pprint("comparing ::%s:: ::%s:: ::%s::"%(curr_date,curr_stop_date,stop_date))
            #get json spot price for period specified
            json_req['start_time'] = curr_date.isoformat()
            json_req['end_time'] = curr_stop_date.isoformat()
            data = spot_price_api.get_current_spot_price(json_req)
            #for d in data:
            #    json_response_data.append(d)
            data = utils.filter_response(data, json_req['filter_type'])
            for d in data:
                json_response_data.append(d)
            curr_date = curr_date + dt.timedelta(hours=job_period_time)
            
        #json_response_data = utils.filter_response(json_response_data, json_req['filter_type'])    
                    
    #json_req_response = {}
    json_req['response']='spot_price'
    if json_req['response_type'] == 'json':
        json_req['response_data']=json_response_data
    elif json_req['response_type'] == 'html':
        template = loader.get_template('ec2_spot_price_monitor/spot_price_table.html')
        context = RequestContext(request, {'json_response_data':json_response_data})
        json_req['response_data']=template.render(context)
    
    return HttpResponse("%s"%(json.dumps(json_req)))

def index(request):
    regions = boto.ec2.regions()
    zone_info={}
    for region in regions:
        pprint("connect to region %s"%region)
        try:
            conn = boto.ec2.connect_to_region(region.name)
            zones = conn.get_all_zones()
            zone_array = []
            for zone in zones:
                zone_array.append(zone.name)
            zone_info[region.name]=zone_array
        except:
            pprint("Site %s had an issue ignoring"%region.name)
            regions.remove(region)
    pprint(zone_info)   
    #get list of image types and vm instance types
    img_types = ImageType.objects.all()
    inst_types = InstanceType.objects.all()
    pprint(img_types)
    return render(request, 'ec2_spot_price_monitor/SpotPriceService.html',{'regions':regions,'zones':zone_info.items(),'image_types':img_types,'inst_types':inst_types})
    

