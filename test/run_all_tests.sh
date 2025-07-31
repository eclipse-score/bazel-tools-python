#!/usr/bin/env bash
set -u

GREEN='\033[0;32m'
RED='\033[0;31m'
RESET='\033[0m'

BZL_WORSKPACE_OUTPUT_BASE="$HOME/.cache/bazel_tools_python_tests/workspace_output_base"


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

# Run checks with bzlmod mode.
run_command "bazel test //..." "tests (bzlmod mode)"
run_command "bazel build --config=ruff_check --keep_going //..." "ruff_check (bzlmod mode)"
run_command "bazel build --config=ruff_format --keep_going //..." "ruff_format (bzlmod mode)"
run_command "bazel build --config=pylint --keep_going //..." "pylint (bzlmod mode)"
run_command "bazel build --config=black --keep_going //..." "black (bzlmod mode)"
run_command "bazel build --config=isort --keep_going //..." "isort (bzlmod mode)"
run_command "bazel build --config=mypy --keep_going //..." "mypy (bzlmod mode)"

# Run checks in workspace mode
run_command "bazel --output_base=${BZL_WORSKPACE_OUTPUT_BASE} test --config=use_workspace_mode //..." "tests (workspace mode)"
run_command "bazel --output_base=${BZL_WORSKPACE_OUTPUT_BASE} build --config=use_workspace_mode --config=ruff_check --keep_going //..." "ruff_check (workspace mode)"
run_command "bazel --output_base=${BZL_WORSKPACE_OUTPUT_BASE} build --config=use_workspace_mode --config=ruff_format --keep_going //..." "ruff_format (workspace mode)"
run_command "bazel --output_base=${BZL_WORSKPACE_OUTPUT_BASE} build --config=use_workspace_mode --config=pylint --keep_going //..." "pylint (workspace mode)"
run_command "bazel --output_base=${BZL_WORSKPACE_OUTPUT_BASE} build --config=use_workspace_mode --config=black --keep_going //..." "black (workspace mode)"
run_command "bazel --output_base=${BZL_WORSKPACE_OUTPUT_BASE} build --config=use_workspace_mode --config=isort --keep_going //..." "isort (workspace mode)"
run_command "bazel --output_base=${BZL_WORSKPACE_OUTPUT_BASE} build --config=use_workspace_mode --config=mypy --keep_going //..." "mypy (workspace mode)"

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
