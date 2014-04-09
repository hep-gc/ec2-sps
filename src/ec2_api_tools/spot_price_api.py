'''
Created on Mar 27, 2014

@author: rd
'''
from pprint import pprint

import boto.ec2,logging

def get_current_spot_price(json_req):
    req_args_array = json_req['request_args']
    regions=[]
    inst_types=[]
    image_types=[]
    zones = []
    
    json_response_data = []
    
    for obj in req_args_array:
        for obj_key in obj.keys():
            if obj_key == 'Regions':
                regions = obj[obj_key];
            if obj_key == 'ZONES':
                zones = obj[obj_key];
            if obj_key == 'InstanceTypes':
                inst_types = obj[obj_key];
            if obj_key == 'ImageTypes':
                image_types = obj[obj_key];
    
    for region in regions:
        #check zones 
        conn = boto.ec2.connect_to_region(region)
        if len(zones) > 0:
            #for each zone do calls for each image and eash instance type   
            for zone in zones:
                for inst in inst_types:
                    for img in image_types:
                        #pprint("get sel zone price for %s %s %s "%(zone,inst,img))
                        
                        start_time = json_req['start_time']
                        end_time = json_req['end_time']
                        #start_time = dt.datetime.now().isoformat()
                        #end_time = dt.datetime.now().isoformat()
                        instance_type=inst
                        product_description = img
                        availability_zone = zone
                        dry_run = False
                        max_results = 100
                        next_token = None
                        filters = None
                        price = conn.get_spot_price_history(start_time, end_time, instance_type, product_description, availability_zone, dry_run, max_results, next_token, filters)
                        #price_obj = price.pop()
                        for price_obj in price:
                            #pprint("%s : %s "%(price_obj,price_obj.price))
                            json_data = {}
                            json_data['region']=region
                            json_data['instance_type']=inst
                            json_data['image_type']=img
                            json_data['zone']=zone
                            json_data['price']=price_obj.price
                            json_data['timestamp']=price_obj.timestamp
                            json_response_data.append(json_data)
                            #price_obj = price.pop()
                        
        else:
            #for each region get their zones and do calles for each instance type and image type
            #conn = boto.ec2.connect_to_region(region)
            reg_zones = conn.get_all_zones()
            for zone in reg_zones:
                for inst in inst_types:
                    for img in image_types:
                        #pprint("OK:get all zones price for %s %s %s "%(zone,inst,img))
                        start_time = json_req['start_time']
                        end_time = json_req['end_time']
                        instance_type=inst
                        product_description = img
                        availability_zone = zone.name
                        dry_run = False
                        max_results = 100
                        next_token = None
                        filters = None
                        price = conn.get_spot_price_history(start_time, end_time, instance_type, product_description, availability_zone, dry_run, max_results, next_token, filters)
                        
                        for price_obj in price:
                            #pprint("%s : %s "%(price_obj,price_obj.price))
                            json_data = {}
                            json_data['region']=region
                            json_data['instance_type']=inst
                            json_data['image_type']=img
                            json_data['zone']=zone.name
                            json_data['price']=price_obj.price
                            json_data['timestamp']=price_obj.timestamp
                            json_response_data.append(json_data)
    logging.debug(json_response_data)
    return json_response_data
                            
                