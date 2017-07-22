#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Chromium Updater
Download and install the newest Chromium build
from http://chromium.org on Mac OS X.
"""

from __future__ import absolute_import, division, print_function, \
    with_statement

import logging
import os.path
import requests
import sys
import traceback
from contextlib import closing


LAST_REVISION_URL = 'https://commondatastorage.googleapis.com/\
chromium-browser-snapshots/Mac/LAST_CHANGE'

DOWNLOAD_URL = 'https://commondatastorage.googleapis.com/\
chromium-browser-snapshots/Mac%2F{}%2Fchrome-mac.zip?alt=media'

DOWNLOAD_PATH = os.path.expanduser('~/.chromium_updater/')


def latest_revision():
    logging.info('Looking for latest revision from %s...' %
                 (LAST_REVISION_URL))
    return requests.get(LAST_REVISION_URL).text


def install():
    logging.debug('Extracting files ...')
    if os.system('unzip -q chrome-mac.zip') != 0:
        logging.error(
            'Failed to update maybe the zip file not download success.')
        sys.exit(1)
    logging.debug('Removing old files.')
    os.system('rm -rf /Applications/Chromium.app')
    logging.debug('Installing files.')
    os.system('cp -r chrome-mac/ /Applications/')
    logging.debug('Removing old files ...')
    os.system('rm -rf chrome-mac*')
    logging.info('All done!')


def update():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(levelname)-8s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S')

    revision = latest_revision()
    logging.info('Latest revision is %s.' % (revision))
    local_download_path = DOWNLOAD_PATH + revision

    if not os.path.exists(DOWNLOAD_PATH):
        os.mkdir(DOWNLOAD_PATH)

    if os.path.exists(local_download_path):
        logging.info('Already have latest version')
        sys.exit(0)

    os.mkdir(local_download_path)
    os.chdir(local_download_path)
    download_url = DOWNLOAD_URL.format(revision)
    logging.debug('Starting download chromium from: %s' % (download_url))

    try:
        with closing(requests.get(download_url, stream=True)) as response:
            chunk_size = 1024
            content_size = int(response.headers['content-length'])
            progress = ProgressBar(
                'progressing',
                total=content_size,
                unit='KB',
                chunk_size=chunk_size,
                run_status=to_str('正在下载'),
                fin_status=to_str('下载完成'))
            with open('./chrome-mac.zip', "wb") as file:
                for data in response.iter_content(chunk_size=chunk_size):
                    file.write(data)
                    progress.refresh(count=len(data))
    except:
        traceback.print_exc()
        sys.exit(1)

    install()
    logging.info('Upgraded to revision %s' % (revision))
    os.system('killall Chromium')
    os.system(
        'open -a /Applications/Chromium.app --args --vmodule=google_api_keys=1'
    )
    sys.exit(0)


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
        self.info = '[%s] %s %.2f %s %s %.2f %s'
        self.title = title
        self.total = total
        self.count = count
        self.chunk_size = chunk_size
        self.status = run_status or b''
        self.fin_status = fin_status or b' ' * len(self.status)
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
        end_str = '\r'
        if self.count >= self.total:
            end_str = '\n'
            self.status = status or self.fin_status
        print(self.__get_info(), end=end_str)


def to_str(s):
    if bytes != str:
        if type(s) == bytes:
            return s.decode('utf-8')
    return s


if __name__ == '__main__':
    update()
