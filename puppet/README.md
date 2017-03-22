# Collective Puppet module

Creates CloudWatch alams for metrics.  

## Alarms

### cpu_credit_balance

Creates alarm for CPUCreditBalance metric.

Class parameters
 * $alarmprefix - REQUIRED, defines alarm name prefix, eg. com.ft.membership.ec2
 * $alarm_threshold - Default value 10, defines numeric threshold for alarm
 * $aws_dir - Default value /root/.aws, defines directory where to store AWS region configuration

#### Usage

Including class in Puppet manifest
```
class { 'collective::alarms::cpu_credit_balance':
	alarmprefix => 'com.ft.membership.ec2'
 }
```
Applying class on command line

`puppet apply --modulepath /collective/puppet/ -e "class { 'collective::alarms::cpu_credit_balance': alarmprefix => 'com.ft.membership.ec2' }"`



## Contact info

Maintainer: jussi.heinonen@ft.com
