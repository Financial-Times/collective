#!/usr/bin/env python
import sys, boto3, pprint
from json import loads
import common

def describe_alarms(alarm_prefix):
    client = boto3.client('cloudwatch')
    response = client.describe_alarms(
        AlarmNamePrefix=alarm_prefix
        )

    for item in response['MetricAlarms']:
        instance_id = item['Dimensions'][0]['Value']
        common.info("Instanceid: " + instance_id)
        common.info("AlarmName: " + item['AlarmName'])
        common.info("AlarmDescription: " + item['AlarmDescription'])
        common.info("ComparisonOperator: " + item['ComparisonOperator'])
        common.info("Threshold: " + str(item['Threshold']))

        pprint.pprint(item)
        #sys.exit(0)



def usage():
    common.info("USAGE: " + sys.argv[0] + " namespace")
    sys.exit(0)
if len(sys.argv) < 2:

    usage()
else:
    describe_alarms(sys.argv[1])
