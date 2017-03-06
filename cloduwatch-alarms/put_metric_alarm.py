#!/usr/bin/env python
import sys, boto3, pprint, yaml
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

def usage():
    common.info("USAGE: " + sys.argv[0] + " namespace instance-id")
    sys.exit(0)
if len(sys.argv) < 3:
    usage()
else:
    namespace = sys.argv[1]
    instance_id = sys.argv[2]
    try:
        with open(alarms_file, 'r') as ymlfile:
            cfg = yaml.load(ymlfile)
        common.info("File " + alarms_file + " loaded")
        for each in cfg.itervalues():
            put_metric_alarm(namespace, instance_id, each['AlarmDescription'], each['AlarmActions'], each['MetricName'], each['Threshold'],  each['Statistic'], each['ComparisonOperator'], each['PluginInstance'])
    except Exception, e:
        common.error("Error while creating alarms: " + str(e))
        sys.exit(1)
    #put_metric_alarm(sys.argv[1])
