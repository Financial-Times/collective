#!/usr/bin/env python

import requests

ok = '\033[94m'
endc = '\033[0m'
fail = '\033[91m'

def construct_invalid_sns_topic():
    region_url = 'http://169.254.169.254/latest/meta-data/placement/availability-zone/'
    arn_prefix = 'arn:aws:sns:'
    region = metadata_get_region(region_url)
    return str(arn_prefix + region + ":" + ":collective_environment_variable_topic_unset")


def info(input):
    print '        ' + ok + input + endc

def error(input):
    print '        ' + fail + 'ERROR: ' + input + endc

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

def metadata_get_region(url,):
    region = get_metadata(url)
    if region:
        return region[:-1]
    else:
        return "eu-west-1"
