# Collective Puppet module

Creates CloudWatch alams for metrics.

## Installation

### metadata.json

In Puppet module's metadata add dependency

```
"dependencies": [
        { "name": "ft/collective" }
]
```

### Modulefile

In Puppet module's Modulefile add dependency

`dependency 'ft/collective'`

### Manual installation

`puppet module install ft-collective`

## Alarms

### cpu_credit_balance

Creates alarm for CPUCreditBalance metric.

Class parameters
 * __alarmprefix__ - REQUIRED, defines alarm name prefix, eg. com.ft.membership.ec2
 * __alarm_threshold__ - Default value 10, defines numeric threshold for alarm
 * __aws_dir__ - Default value /root/.aws, defines directory for AWS region configuration
 * __config_file__ - Default value false, use default configuration YAML file.
   * Specify file path to custom configuration file to override default

#### Usage

Including class in Puppet manifest using default configuration file
```
class { 'collective::alarms::cpu_credit_balance':
	alarmprefix => 'com.ft.membership.ec2'
 }
```

Including class in Puppet manifest using custom configuration file
```
class { 'collective::alarms::cpu_credit_balance':
	alarmprefix => 'com.ft.membership.ec2',
  config_file => '/etc/collective/custom_config.yaml'
 }
```

Applying class on command line

`puppet apply --modulepath /collective/puppet/ -e "class { 'collective::alarms::cpu_credit_balance': alarmprefix => 'com.ft.membership.ec2' }"`



## Contact info

Maintainer: jussi.heinonen@ft.com
