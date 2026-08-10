#!/usr/bin/env bash
# Purpose: update review-with-multi-debate to the latest commit on its configured upstream branch.

set -euo pipefail

git submodule update --init review-with-multi-debate
git submodule update --remote --merge review-with-multi-debate
