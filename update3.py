#!/usr/bin/env python
# Chromium Updater
# Download and install the newest Chromium build from http://chromium.org on Mac OS X.

import urllib.request, urllib.error, urllib.parse, os.path, sys

LAST_REVISION_URL = 'https://commondatastorage.googleapis.com/chromium-browser-snapshots/Mac/LAST_CHANGE'
DOWNLOAD_URL = 'https://commondatastorage.googleapis.com/chromium-browser-snapshots/Mac%2F{}%2Fchrome-mac.zip?alt=media'
DOWNLOAD_PATH = os.path.expanduser('~/.chromium_updater/')

def latest_revision():
	return urllib.request.urlopen(LAST_REVISION_URL).read().decode()

def install():
	print('Extracting files ...')
	os.system('unzip -q chrome-mac.zip')
	print('Removing old files.')
	os.system('rm -rf /Applications/Chromium.app')
	print('Installing files.')
	os.system('cp -r chrome-mac/ /Applications/')
	print('Removing old files ...')
	os.system('rm -rf chrome-mac*')
	print('All done!')

def update():
	print('Looking for latest revision ...')
	revision = latest_revision()
	print('Latest revision is %s.' % (revision))
	local_download_path = DOWNLOAD_PATH + revision

	if not os.path.exists(DOWNLOAD_PATH):
		os.mkdir(DOWNLOAD_PATH)
	
	if os.path.exists(local_download_path) :
		print('Already have latest version')
		sys.exit()
	
	os.mkdir(local_download_path)
	os.chdir(local_download_path)
	download_url = DOWNLOAD_URL.format(revision)
	command = 'curl ' + download_url + ' -o chrome-mac.zip'
	print('Starting download chromium from: %s' % (download_url))
	os.system(command)
	install()
	print('Upgraded to revision %s' % (revision))
	os.system('open -a /Applications/Chromium.app --args --vmodule=google_api_keys=1')
	sys.exit()

if __name__ == '__main__':
	update()

