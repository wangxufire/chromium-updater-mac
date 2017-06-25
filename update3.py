#!/usr/bin/env python3
"""
Chromium Updater
Download and install the newest Chromium build
from http://chromium.org on Mac OS X.
"""

import os.path
import sys
import traceback
import urllib.error
import urllib.parse
import urllib.request
from contextlib import closing

import requests

LAST_REVISION_URL = 'https://commondatastorage.googleapis.com/\
chromium-browser-snapshots/Mac/LAST_CHANGE'

DOWNLOAD_URL = 'https://commondatastorage.googleapis.com/\
chromium-browser-snapshots/Mac%2F{}%2Fchrome-mac.zip?alt=media'

DOWNLOAD_PATH = os.path.expanduser('~/.chromium_updater/')


def latest_revision():
    print('Looking for latest revision from %s...' % (LAST_REVISION_URL))
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
    revision = latest_revision()
    print('Latest revision is %s.' % (revision))
    local_download_path = DOWNLOAD_PATH + revision

    if not os.path.exists(DOWNLOAD_PATH):
        os.mkdir(DOWNLOAD_PATH)

    if os.path.exists(local_download_path):
        print('Already have latest version')
        sys.exit()

    os.mkdir(local_download_path)
    os.chdir(local_download_path)
    download_url = DOWNLOAD_URL.format(revision)
    print('Starting download chromium from: %s' % (download_url))

    try:
        with closing(requests.get(download_url, stream=True)) as response:
            chunk_size = 1024
            content_size = int(response.headers['content-length'])
            progress = ProgressBar(
                "progressing",
                total=content_size,
                unit="KB",
                chunk_size=chunk_size,
                run_status="正在下载",
                fin_status="下载完成")
            with open('./chrome-mac.zip', "wb") as file:
                for data in response.iter_content(chunk_size=chunk_size):
                    file.write(data)
                    progress.refresh(count=len(data))
    except:
        traceback.print_exc()
        sys.exit()

    install()
    print('Upgraded to revision %s' % (revision))
    os.system('killall Chromium')
    os.system(
        'open -a /Applications/Chromium.app --args --vmodule=google_api_keys=1'
    )
    sys.exit()


"""
Author：微微寒
Link：http://blog.csdn.net/supercooly/article/details/51046561
"""


class ProgressBar(object):
    def __init__(self,
                 title,
                 count=0.0,
                 run_status=None,
                 fin_status=None,
                 total=100.0,
                 unit='',
                 sep='/',
                 chunk_size=1.0):
        super(ProgressBar, self).__init__()
        self.info = "[%s] %s %.2f %s %s %.2f %s"
        self.title = title
        self.total = total
        self.count = count
        self.chunk_size = chunk_size
        self.status = run_status or ""
        self.fin_status = fin_status or " " * len(self.status)
        self.unit = unit
        self.seq = sep

    def __get_info(self):
        _info = self.info % (self.title, self.status,
                             self.count / self.chunk_size, self.unit, self.seq,
                             self.total / self.chunk_size, self.unit)
        return _info

    def refresh(self, count=1, status=None):
        self.count += count
        self.status = status or self.status
        end_str = "\r"
        if self.count >= self.total:
            end_str = '\n'
            self.status = status or self.fin_status
        print(self.__get_info(), end=end_str)


if __name__ == '__main__':
    update()
