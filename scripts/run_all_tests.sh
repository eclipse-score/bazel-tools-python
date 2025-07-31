#!/usr/bin/env bash
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

# Run bazel test with workspace mode and python 3.9.
run_command "bazel --output_base=$HOME/.cache/bazel_tools_python/workspace_output_base test --config=use_workspace_mode --config=python_3_9 //..." "tests (workspace mode and python 3.9)"

# Run bazel test with bzlmod mode and python 3.12.
run_command "bazel --output_base=$HOME/.cache/bazel_tools_python/python_3_12_output_base test --config=python_3_12 //..." "tests (bzlmod mode and python 3.12)"

# Run bazel test with bzlmod mode.
run_command "bazel test //..." "tests (bzlmod mode)"

# Run python quality tools.
run_command "bazel build --config=ruff_check --keep_going //..." "ruff_check"
run_command "bazel build --config=ruff_format --keep_going //..." "ruff_format"
run_command "bazel build --config=pylint --keep_going //..." "pylint"
run_command "bazel build --config=black --keep_going //..." "black"
run_command "bazel build --config=isort --keep_going //..." "isort"
run_command "bazel build --config=mypy --keep_going //..." "mypy"

# Run test workspace tests.
run_command "test/run_all_tests.sh" "tests (in test workspace)"

# Run buildifier.
run_command "bazel run bazel/buildifier:check" "buildifier"

# Run Eclipse-specific checks.
run_command "bazel run //:copyright.check -- --fix" "eclipse copyright check"
run_command "bazel test //:format.check" "eclipse format check"

# Run security vulnerability scan.
run_command "third_party/pip/check_vulnerabilities.sh" "security scan"

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
