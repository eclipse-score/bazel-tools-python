#!/bin/bash -e
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
bazel run //third_party/pip:requirements_3_8.test --config=python_3_8 --config=use_workspace_mode
bazel run //third_party/pip:requirements_3_9.test --config=python_3_9 --config=use_workspace_mode
bazel run //third_party/pip:requirements_3_10.test --config=python_3_10 --config=use_workspace_mode
bazel run //third_party/pip:requirements_3_11.test --config=python_3_11 --config=use_workspace_mode
bazel run //third_party/pip:requirements_3_12.test --config=python_3_12 --config=use_workspace_mode
bazel run //third_party/pip:requirements_3_13.test --config=python_3_13 --config=use_workspace_mode
bazel run //third_party/pip:requirements_3_14.test --config=python_3_14 --config=use_workspace_mode
