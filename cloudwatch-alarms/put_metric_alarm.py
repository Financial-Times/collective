#!/usr/bin/env python
import sys, boto3, pprint, yaml, argparse
from json import loads
import common
alarms_file = 'alarms.yml'

def put_metric_alarm(namepace, instance_id, description, actions, metric_name, threshold, statistic, operator, plugin_instance):
    client = boto3.client('cloudwatch')
    response = client.put_metric_alarm(
        AlarmName=namepace + "." + instance_id + "." + metric_name + "." + plugin_instance,
        AlarmDescription=description + ". Instance-id " + instance_id + ".",
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
parser.add_argument('--topic', help='ARN of SNS Topic to send alerts to, eg. arn:aws:sns:eu-west-1:027104099916:SemanticMetadata', required=False)

args = parser.parse_args()

namespace = args.namespace
instance_id = args.instanceid
try:
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
