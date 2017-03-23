# Collective Puppet module

Creates CloudWatch alams for metrics.  

## Alarms

### cpu_credit_balance

Creates alarm for CPUCreditBalance metric.

Class parameters
 * $alarmprefix - REQUIRED, defines alarm name prefix, eg. com.ft.membership.ec2
 * $alarm_threshold - Default value 10, defines numeric threshold for alarm
 * $aws_dir - Default value /root/.aws, defines directory for AWS region configuration
 * config_file - Default value false, use default configuration YAML file.
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
