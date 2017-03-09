#!/usr/bin/env python


'''
Script to create or modify existing CloudWatch alarms

usage: put_metric_alarm.py --help

Author: Jussi Heinonen
Date: 9.3.2017
URL: https://github.com/Financial-Times/collective
'''

import sys, boto3, pprint, yaml, argparse, re, os, requests
from json import loads
import common
alarms_file = 'alarms.yml'
config_is_file = True

def put_metric_alarm(namepace, instance_id, description, actions, metric_name, threshold, statistic, operator, plugin_instance):
    client = boto3.client('cloudwatch')
    response = client.put_metric_alarm(
        AlarmName=namepace + "." + instance_id + "." + metric_name + "." + plugin_instance,
        AlarmDescription=description + " Instance-id " + instance_id + ".",
        OKActions=actions,
        AlarmActions=actions,
        ActionsEnabled=True,
        MetricName=metric_name,
        Namespace=namespace,
        Dimensions=[
            {
                'Name': 'Host',
                'Value': instance_id
            },
            {
                'Name': 'PluginInstance',
                'Value': plugin_instance
            },
        ],
        Period=300,
        EvaluationPeriods=1,
        Threshold=threshold,
        Statistic=statistic,
        ComparisonOperator=operator
    )
    for each in response.itervalues():
        if each['HTTPStatusCode'] == 200:
            common.info("Alarm " + namepace + "." + instance_id + "." + metric_name + " created")
            return True
        else:
            common.error("Failed to create alarm " + namepace + "." + instance_id + "." + metric_name)
            return False
    pprint.pprint(response)

parser = argparse.ArgumentParser(description='Create CloudWatch alarms with given name prefix')
parser.add_argument('--namespace', help='Alarm namespace, eg. com.ft.up.semantic-data.neo4j', required=True)
parser.add_argument('--instanceid', help='InstanceID, eg. i-0fc52a4ca4d81b5b4', required=True)
parser.add_argument('--topic', help='[Optional] ARN of SNS Topic to send alerts to, eg. arn:aws:sns:eu-west-1:027104099916:SemanticMetadata', required=False)
parser.add_argument('--config', help='[Optional] File path (./config/alarms.yml) or URL (https://raw.githubusercontent.com/Financial-Times/collective/master/alarms.yml) to alarm configuration YAML file', required=False)
args = parser.parse_args()
namespace = args.namespace
instance_id = args.instanceid
try:
    if args.config: # Check whether --config value is URL or a file
        if re.search("http",args.config):
            common.info("Getting config file from HTTP endpoint " + args.config)
            try:
                r = requests.get(args.config)
                if r.status_code == requests.codes.ok:
                    cfg = yaml.load(r.text)
                    config_is_file = False
                else:
                    common.error("Failed to load document " + args.config)
                    sys.exit(1)
            except Exception, e:
                common.error("Failed to retrieve yaml document from " + args.config + ". Reason: " + str(e) )
                sys.exit(1)
        else:
            if os.path.isfile(args.config):
                common.info("Using config file " + args.config)
                alarms_file = args.config
            else:
                common.error("File " + args.config + " not found!")
                sys.exit(1)
    else:
        common.info("Using default config file " + alarms_file)
    if config_is_file: # If config provided is a file. This is default behaviour, is False only if config is provided as a URL
        with open(alarms_file, 'r') as ymlfile:
            cfg = yaml.load(ymlfile)
        common.info("File " + alarms_file + " loaded")
    for each in cfg.itervalues():
        if args.topic: #Override AlarmActions if --topic is passed in as a parameter
            common.info("Using override topic " + args.topic)
            each['AlarmActions'] = [ args.topic ]        
        put_metric_alarm(namespace, instance_id, each['AlarmDescription'], each['AlarmActions'], each['MetricName'], each['Threshold'],  each['Statistic'], each['ComparisonOperator'], each['PluginInstance'])
except Exception, e:
    common.error("Error while creating alarms: " + str(e))
    sys.exit(1)
