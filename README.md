# chromium-updater-mac

## Usage

ensure python3 installed in /usr/local/bin/python3

```bash
git clone https://github.com/wangxufire/chromium-updater-mac.git ~/.chromium-updater-mac

cp ~/.chromium-updater-mac/com.wangxufire.chromium.updater.plist ~/Library/LaunchAgents/

# Chromium will be automatically updated at 12:00 am every day
launchctl load ~/Library/LaunchAgents/com.wangxufire.chromium.updater.plist

# Execute this command, chromium will be updated immediately
launchctl start com.wangxufire.chromium.updater
```
