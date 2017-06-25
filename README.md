# chromium-updater-mac

## Usage

ensure python3 installed in /usr/local/bin/python3

```bash
git clone https://github.com/wangxufire/chromium-updater-mac.git ~/.chromium-updater-mac

# Run this script, then chromium will be automatically updated at 11:30 am every day
~/.chromium-updater-mac/install.sh

# Execute this command, chromium will be updated immediately
launchctl start com.wangxufire.chromium.updater
```
