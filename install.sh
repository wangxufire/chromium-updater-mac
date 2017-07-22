#!/usr/bin/env bash

# set -e

pip install -U requests

plist_path="$HOME/.chromium-updater-mac/com.wangxufire.chromium.updater.plist"
plist_filename=$(basename "$plist_path")
install_path="$HOME/Library/LaunchAgents/$plist_filename"

sed -i "" "s|~|$HOME|g" "$plist_path"

echo "installing launchctl plist: $plist_path --> $install_path"
cp -f "$plist_path" "$install_path"

launchctl unload "$install_path"
launchctl load -w -F "$install_path"

echo "to check if it's running, run this command: launchctl list | grep chromium.updater"
echo "to uninstall, run this command: launchctl unload $install_path"
