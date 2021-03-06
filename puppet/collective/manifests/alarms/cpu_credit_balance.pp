class collective::alarms::cpu_credit_balance (
$alarmprefix,
$alarm_threshold  = 10,
$aws_dir          = '/root/.aws',
$config_file      = false
) {

  Exec { path => $::path }

  $git_endpoint = 'https://raw.githubusercontent.com/Financial-Times/collective/master/cloudwatch-alarms/'
  $workdir = '/opt/collective'
  $pip_packages = [ 'awscli', 'boto3',  'requests', 'pyyaml' ]

  package { $pip_packages:
    ensure    => present,
    provider  => 'pip'
  }

  file { $workdir: ensure => directory }
  ->
  exec { 'download_put_metric_alarm_py':
    command => "curl -s --connect-timeout 3 ${git_endpoint}/put_metric_alarm.py > ${workdir}/put_metric_alarm.py",
    unless  => "test -f ${workdir}/put_metric_alarm.py"
  }
  ->
  exec { 'download_common_py':
    command => "curl -s --connect-timeout 3 ${git_endpoint}/common.py > ${workdir}/common.py",
    unless  => "test -f ${workdir}/common.py"
  }

  if $config_file {
    $config_file_path = $config_file
  }
  else {
    $subclass_list = split($name, '::')
    $subclass_name = $subclass_list[-1]
    $config_file_path = "${workdir}/${subclass_name}.yml"
    file { "${config_file_path}":
      content => "CPU_CREDIT_BALANCE:
        Namespace: AWS/EC2
        Instanceid: get_instanceid()
        AlarmDescription: CPU Credit Balance is low
        MetricName: CPUCreditBalance
        Threshold: 10
        Statistic: Average
        ComparisonOperator: LessThanOrEqualToThreshold
        Dimensions:
          - Name: InstanceId
            Value:  get_instanceid()
        ",
      notify => Exec['create-alarm']
    }
  }

  file { "$aws_dir": ensure => directory }
  ->
  exec { 'set-aws-region':
    command => "echo \"region = $(curl -s --connect-timeout 3 http://169.254.169.254/latest/dynamic/instance-identity/document | grep region | cut -d '\"' -f 4)\" > $aws_dir/config",
    unless  => "test -f ${aws_dir}/config"
  }
  ->
  exec { 'create-alarm':
    command => "python ${workdir}/put_metric_alarm.py --alarmprefix ${alarmprefix} --config ${config_file_path}",
  }

}
