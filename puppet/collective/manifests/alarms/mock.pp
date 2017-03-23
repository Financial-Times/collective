class collective::alarms::mock (
  $config_file = false
) {

  notify { "class-name-notify":
    message => "Class name ${name}" #name variable references the class name, eg. collective::alarms::mock
  }

  if $config_file {
    $config_file_path = $config_file
  }
  else {
    $subclass_list = split($name, '::')
    $subclass_name = $subclass_list[-1]
    $config_file_path = "config/${subclass_name}.yml"
  }

  notify { "config_file-notify":
    message => "Using config file ${config_file_path}" #references the subclass name, eg. mock
  }


}
