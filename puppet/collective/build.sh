#!/usr/bin/env bash
#
# Build puppet module
#
# USAGE: ./build --version=1.2.3

declare -A ARGS

errorAndExit() {
  echo -e "\e[31m$(date '+%x %X') ERROR: $1\e[0m"
  usage
  exit $2
}

info() {
  echo -e "\e[34m$(date '+%x %X') INFO: ${1}\e[0m"
}

processCliArgs() {
  #Reads arguments into associative array ARGS[]
  #Key-Value argument such as --myarg="argvalue" adds an element ARGS[--myarg]="argvalue"
  #
  # USAGE: processCliArgs $*
  for each in $*; do
    if [[ "$(echo ${each} | grep '=' >/dev/null ; echo $?)" == "0" ]]; then
      key=$(echo ${each} | cut -d '=' -f 1)
      value=$(echo ${each} | cut -d '=' -f 2)
      ARGS[${key}]="${value}"
    else
      errorAndExit "Argument must contain = character as in --key=value"
    fi
  done
}

updateMetadataVersion() {
  sed -i "s/\"version\":.*,/\"version\": \"${1}\",/g" metadata.json
}

usage() {
  info "USAGE: $0 --version=1.2.3"
}

validateManifest() {
  find . -name '*.pp' -exec puppet parser validate {} \; &>> validate.log
  if [[ "$(cat validate.log | wc -l)" -gt "0" ]]; then
    cat validate.log
    rm -f validate.log
    errorAndExit "Manifest validation failed" 1
  else
    info "Manifest validation successful"
    rm -f validate.log
  fi
}

if [[ ! -f metadata.json ]]; then
  errorAndExit "Failed to find metadata.json. Exit 1." 1
fi

processCliArgs $*

if [[ -z ${ARGS[--version]} ]]; then # Prompt user for version numner unless provided by --version CLI flag
  read -p "Please enter module version number, eg. 1.2.3: " ARGS[--version]
fi

if [[ ${ARGS[--version]} =~ ^[0-9]+\.[0-9]+\.[0-9]+ ]]; then # Validate format of the version
  info "Building module version ${ARGS[--version]}"
else
  errorAndExit "Version number must be in format of x.y.z" 1
fi

if [[ -d pkg/ ]]; then # Remove previous buils if pkg/ directory exists
  rm -rf pkg/
fi

info "Updating version in metadata.json"
updateMetadataVersion ${ARGS[--version]}

info "Validating manifests"
validateManifest

info "Building puppet module version ${ARGS[--version]}"
puppet module build .
