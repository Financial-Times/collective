#!/usr/bin/env python
import sys, boto3, pprint
from json import loads
import common

def describe_alarms(alarm_prefix):
    client = boto3.client('cloudwatch')
    response = client.put_metric_alarm(
        AlarmName='com.ft.up.sematic.neo4j.i-025d2577a31b6f47c.df.loadaverage',
        AlarmDescription='Load Average 4 or above on instance i-025d2577a31b6f47c',
        ActionsEnabled=True,
        MetricName='load.load',
        Namespace='com.ft.up.semantic-data.neo4j',
        Dimensions=[
            {
                'Name': 'Host',
                'Value': 'i-03ddea25106f5f52c'
            },
        ],
        Period=300,
        EvaluationPeriods=1,
        Threshold=4,
        ComparisonOperator='GreaterThanOrEqualToThreshold'
    )
    pprint.pprint(response)

def usage():
    common.info("USAGE: " + sys.argv[0] + " namespace")
    sys.exit(0)
if len(sys.argv) < 2:

    usage()
else:
    describe_alarms(sys.argv[1])
