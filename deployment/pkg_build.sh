#!/bin/bash
#
# AutoPkgNotify - Email notifications for AutoPkg
# Copyright 2014 James Barclay
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# This script builds a deployment package for AutoPkgNotify

declare -x awk="/usr/bin/awk"
declare -x chmod="/bin/chmod"
declare -x chown="/usr/sbin/chown"
declare -x cp="/bin/cp"
declare -x find="/usr/bin/find"
declare -x git="/usr/local/bin/git"
declare -x mkdir="/bin/mkdir"
declare -x pkgbuild="/usr/bin/pkgbuild"

declare -x SCRIPT="${0##*/}" ; SCRIPT_NAME="${Script%%\.*}"
declare -x SCRIPT_PATH="$0" RUN_DIRECTORY="${0%/*}"

declare -x PROJECT_DOMAIN="com.github.futureimperfect.autopkg-notify"
declare -x PROJECT_NAME="AutoPkgNotify"
declare -x INSTALL_PATH="/Library/Application Support/autopkg-notify"
declare -x LAUNCH_DAEMON="$(echo "$PROJECT_DOMAIN.plist" | $awk '{ print tolower($0) }')"
declare -x LAUNCH_DAEMON_PATH="/Library/LaunchDaemons"
declare -x COMMIT="$(cd "$RUN_DIRECTORY"; $git log | $awk '/commit/ { print substr($2,1,10);exit }')"
declare -x TMP_PATH="/private/tmp/$PROJECT_NAME-$COMMIT-$$$RANDOM"
declare -x BIN_DIR="$RUN_DIRECTORY/../bin"
declare -x PACKAGE_ID="$PROJECT_DOMAIN.$PROJECT_NAME.$COMMIT"

check_root () {
if [ "$EUID" -ne 0 ]; then
    echo "This script must run as root. Exiting now."
    exit 1
fi
}

check_git () {
if [[ ! -x "$git" ]]; then
    declare -x git="/usr/bin/git"
    if [[ ! -x "$git" ]]; then
        echo "This script requires git. Please install the Xcode command-line tools and try again."
    fi
fi
}

main () {
# Create $BIN_DIR if it doesn't exist
if [[ ! -d "$BIN_DIR" ]]; then
    $mkdir -p "$BIN_DIR"
fi

# Create the tmp directories if needed
if [[ ! -d "$TMP_PATH/$INSTALL_PATH" || ! -d "$TMP_PATH/$LAUNCH_DAEMON_PATH" ]]; then
    $mkdir -p "$TMP_PATH/$INSTALL_PATH"
    $mkdir -p "$TMP_PATH/$LAUNCH_DAEMON_PATH"
fi

# Make sure the recipe_list exists
if [[ -f "$RUN_DIRECTORY/../recipe_list" ]]; then
    $cp -vp "$RUN_DIRECTORY/../recipe_list" "$TMP_PATH/$INSTALL_PATH/"
else
    echo "You must create a file called recipe_list in the project directory with the AutoPkg recipes to run."
    exit 1
fi

# Copy the files to the tmp locations
$cp -Rvp "$RUN_DIRECTORY/../apn" "$TMP_PATH/$INSTALL_PATH/"
$cp -vp "$RUN_DIRECTORY/../README.md" "$TMP_PATH/$INSTALL_PATH/"
$cp -Rvp "$RUN_DIRECTORY/$LAUNCH_DAEMON" "$TMP_PATH/$LAUNCH_DAEMON_PATH/"

# Copy the SMTP password to the tmp location if it exists
if [[ -f "$RUN_DIRECTORY/../p.txt" ]]; then
    $cp -vp "$RUN_DIRECTORY/../p.txt" "$TMP_PATH/$INSTALL_PATH/"
fi

# Change ownership
$chown -Rv 0:0 "$TMP_PATH"

# Make sure $SCRIPT is executable
$chmod a+x "$TMP_PATH/$INSTALL_PATH/apn/autopkg_notify.py"

# Clean up python bytecode files before building
$find "$TMP_PATH/$INSTALL_PATH/" -name "*.pyc" -exec rm {} \;

# Build the pkg
$pkgbuild --identifier "$PACKAGE_ID" \
          --root "$TMP_PATH/" \
          --scripts "$RUN_DIRECTORY/../scripts" \
          "$BIN_DIR/$PROJECT_NAME-$COMMIT.pkg"
}

check_root
check_git
main

exit $?
