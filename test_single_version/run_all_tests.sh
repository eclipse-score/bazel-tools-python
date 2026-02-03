#!/usr/bin/env bash
# *******************************************************************************
# Copyright (c) 2025 Contributors to the Eclipse Foundation
#
# See the NOTICE file(s) distributed with this work for additional
# information regarding copyright ownership.
#
# This program and the accompanying materials are made available under the
# terms of the Apache License Version 2.0 which is available at
# https://www.apache.org/licenses/LICENSE-2.0
#
# SPDX-License-Identifier: Apache-2.0
# *******************************************************************************

set -u

GREEN='\033[0;32m'
RED='\033[0;31m'
RESET='\033[0m'

declare -A command_status
declare -a command_order
exit_code=0

interrupt_handler(){
	echo -e "${RED}Script interrupted by user.${RESET}"
	exit 130	# Exit code for script interruption by Ctrl+C
}

trap interrupt_handler SIGINT

run_command(){
	local cmd=$1
	local name=$2

	echo -e "Running $name ..."

	if eval "$cmd"; then
		echo -e "${GREEN}$name SUCCEEDED${RESET}"
		command_status["$name"]="SUCCEEDED"
	else
		echo -e "${RED}$name FAILED${RESET}"
		command_status["$name"]="FAILED"
		exit_code=1
	fi

	command_order+=("$name")
}

# Ensure the following commands are run from the test workspace.
cd $(dirname $0)

# Run checks.
run_command "bazel test //..." "tests"
run_command "bazel build --config=ruff_check --keep_going //..." "ruff_check"
run_command "bazel build --config=ruff_format --keep_going //..." "ruff_format"
run_command "bazel build --config=pylint --keep_going //..." "pylint"
run_command "bazel build --config=black --keep_going //..." "black"
run_command "bazel build --config=isort --keep_going //..." "isort"
run_command "bazel build --config=mypy --keep_going //..." "mypy"


# Print execution summary
printf '%-37s | %-10s\n' "Command Name" "Status"
printf '%-37s | %-10s\n' "-------------------------------------" "----------"

for name in "${command_order[@]}"; do
	status="${command_status[$name]}"

	if [[ "$status" == "SUCCEEDED" ]]; then
		printf "%-37s | ${GREEN}%-10s${RESET}\n" "$name" "$status"
	else
		printf "%-37s | ${RED}%-10s${RESET}\n" "$name" "$status"
	fi
done

printf '%-37s | %-10s\n' "-------------------------------------" "----------"

exit $exit_code
