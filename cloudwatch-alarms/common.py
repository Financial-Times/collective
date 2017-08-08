#!/usr/bin/env python

import requests, sys

ok = '\033[94m'
endc = '\033[0m'
fail = '\033[91m'

def construct_invalid_sns_topic(region):
    arn_prefix = 'arn:aws:sns:'
    return str(arn_prefix + region + ":" + ":collective_environment_variable_topic_unset")

def info(input):
    print '        ' + ok + input + endc

def error(input):
    print '        ' + fail + 'ERROR: ' + input + endc

def get_instanceid():
    return get_metadata("http://169.254.169.254/latest/meta-data/instance-id")

def get_metadata(request):
    try:
        result = requests.get(request, timeout=3)
        if result.status_code is 200:
            return str(result.text)
        else:
            error("Failed to get metadata")
            return False
    except:
        return False

def metadata_get_region(url):
    region = get_metadata(url)
    if region:
        return region[:-1]
    else:
        info("Unable to resolve region from metadata, using default eu-west-1")
        return "eu-west-1"

def process_dimensions(Dimensions):
    darray=[]
    for item in Dimensions:
        #info("Processing Dimensions " + str(item))
        if "()" in item['Value'][-2:]:
            info("Dimensions value is a pointer to function " + item['Value'][:-2])
            try:

                item['Value'] = globals()[item['Value'][:-2]]() # To reference function in this module https://ubuntuforums.org/showthread.php?t=1110989
            except Exception, e:
                error("Unable to load function " + item['Value'][:-2] + " in module common: " + str(e))
        darray.append(item)
    #info("Dimensions list is " + str(darray))
    return darray

def variable_processor(var):
    if "()" in var[-2:]:
        info("Variable value is a pointer to function " + var[:-2])
        try:
            #func = getattr(common, item['Value'][:-2]) # To reference function in module common http://stackoverflow.com/questions/3061/calling-a-function-of-a-module-from-a-string-with-the-functions-name-in-python
            #item['Value'] = func()
            return globals()[var[:-2]]() # To reference function in this module https://ubuntuforums.org/showthread.php?t=1110989
        except Exception, e:
            error("Unable to load function " + var[:-2] + " in module common: " + str(e))
    else:
        return var
