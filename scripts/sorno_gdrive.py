#!/usr/bin/python
"""A command line client for Google Drive.

The API doc used to implement this is in
https://developers.google.com/drive/web/quickstart/quickstart-python

Currently, you can upload files with the script.

In order to use this script, please look at the "Using scripts involve Google
App API" section of the sorno-py-scripts README (can be found in
https://github.com/hermantai/sorno-scripts/tree/master/sorno-py-scripts). The
API needed for this script is "Drive API" with the scope
'https://www.googleapis.com/auth/drive.readonly'

Examples:

    You can upload files by running:

        $ sorno_gdrive.py upload <file1> [file2, file3...]


    Copyright 2014 Heung Ming Tai

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""

import argparse
import logging
import os
import pprint
import subprocess
import sys
import tempfile

import apiclient
from apiclient.discovery import build
from apiclient.http import MediaFileUpload

import httplib2

from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage

from sorno import consoleutil
from sorno import loggingutil
from sorno import webutil

_LOG = logging.getLogger(__name__)

# Check https://developers.google.com/drive/scopes for all available scopes
OAUTH_SCOPE = 'https://www.googleapis.com/auth/drive'

# Redirect URI for installed apps
REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'

CREDENTIALS_FILE = os.path.expanduser("~/.sorno_gdrive-google-drive-api.cred")

GDRIVE_MIMETYPE_FOLDER = "application/vnd.google-apps.folder"


class App(object):
    def __init__(self):
        self.drive_service = None

    def auth(self, use_credentials_cache=True):
        # Copy your credentials from the console
        client_id = os.getenv('GOOGLE_APP_PROJECT_CLIENT_ID')
        client_secret = os.getenv('GOOGLE_APP_PROJECT_CLIENT_SECRET')

        if not client_id:
            print(
                "Please set the environment variable"
                " GOOGLE_APP_PROJECT_CLIENT_ID"
            )
            sys.exit(1)

        if not client_secret:
            print(
                "Please set the environment variable"
                " GOOGLE_APP_PROJECT_CLIENT_SECRET"
            )
            sys.exit(1)

        # Run through the OAuth flow and retrieve credentials
        flow = OAuth2WebServerFlow(client_id, client_secret, OAUTH_SCOPE,
                                   redirect_uri=REDIRECT_URI)

        # Indicate we need the user to grant us permissions and give the auth code or
        # not
        need_get_code = True

        if os.path.exists(CREDENTIALS_FILE) and use_credentials_cache:
            storage = Storage(CREDENTIALS_FILE)
            credentials = storage.get()
            print("Use old credentials")
            need_get_code = False

        if need_get_code:
            authorize_url = flow.step1_get_authorize_url()
            print 'Go to the following link in your browser: ' + authorize_url
            code = raw_input('Enter verification code: ').strip()

            credentials = flow.step2_exchange(code)

            storage = Storage(CREDENTIALS_FILE)
            storage.put(credentials)

        # Create an httplib2.Http object and authorize it with our credentials
        http = httplib2.Http()
        http = credentials.authorize(http)

        self.drive_service = build('drive', 'v3', http=http)

    def list_action(self, args):
        self.auth(args.use_credentials_cache)
        for f in self.list_path(args.path):
            print(f['name'])

    def list_path(self, path):
        if not path:
            path = '/'

        if path == '/':
            return self.list_path_by_parent_id('root')

        response = self.drive_service.files().list(
            q="name contains '%s'" % path,
            fields='nextPageToken, files(id, name, mimeType, parents)').execute()

        folders = [
            f for f in response['files']
            if f['mimeType'] == GDRIVE_MIMETYPE_FOLDER
        ]
        if len(folders) == 0:
            raise ResourceNotExists('Path "%s" not found' % path)

        if len(folders) == 1:
            folder = folders[0]
        else:
            c = consoleutil.choose_item(
                "Choose the directory to list: ",
                [f['name'] for f in folders],
            )
            folder = folders[c]

        return self.list_path_by_parent_id(folder['id'])

    def get_file_metadata(self, file_id):
        return self.drive_service.files().get(fileId=file_id).execute()

    def list_path_by_parent_id(self, file_id):
        response = self.drive_service.files().list(
            q="'%s' in parents" % file_id,
            fields='nextPageToken, files(id, name, mimeType, parents)').execute()
        return response['files']


    def upload_action(self, args):
        self.auth(args.use_credentials_cache)
        self.upload_files(args.files)

    def upload_files(self, filepaths):
        _LOG.info("Will upload files: %s" , ", ".join(filepaths))

        for filepath in filepaths:
            if (filepath.startswith("http://") or
                filepath.startswith("https://")):
                _LOG.info("Will upload file %s to Google Drive", filepath)
                basefn = os.path.basename(filepath)
                dest = os.path.join(tempfile.tempdir, basefn)
                _LOG.info("Download %s to %s", filepath, dest)
                webutil.download_file(filepath, dest)
                _LOG.info("Upload %s to Google Drive", dest)
                self.upload_file(dest)
            else:
                _LOG.info("Upload file: %s", filepath)
                self.upload_file(filepath)

    def upload_file(self, filepath):
        self.ensure_mimetype_exists(filepath)
        media = MediaFileUpload(
            filepath,
        )

        file_title = os.path.basename(filepath)
        response = self.drive_service.files().insert(
            media_body=media,
            body={
                'title': file_title,
            },
        ).execute()

        pprint.pprint(response)

    def download_action(self, args):
        _LOG.error("Not implemented, yet")
        sys.exit(1)

    def ensure_mimetype_exists(self, filepath):
        import mimetypes
        if mimetypes.guess_type(filepath)[0]:
            return

        _LOG.warn(
            "Cannot detect mimetype for %s, assume it's text/plain.",
            filepath,
        )

        ext = os.path.splitext(filepath)[1]
        # works most of the time, if not, too bad
        _LOG.info("Add type text/plain for extension %s", ext)
        mimetypes.add_type('text/plain', ext, strict=True)
        assert mimetypes.guess_type(filepath)


class ResourceNotExists(Exception):
    pass


def main():
    app = App()
    args = parse_args(app, sys.argv[1:])

    loggingutil.setup_logger(_LOG, debug=args.debug)
    args.func(args)


def parse_args(app_obj, cmd_args):
    description = __doc__.split("Copyright 2014")[0].strip()
    parser = argparse.ArgumentParser(
        description=description,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--no-credentials-cache",
        dest="use_credentials_cache",
        action="store_false",
        default=True,
        help="If specified, old credentials are not reused and you have to"
            " follow the instruction from this script to get the code every"
            " time you use this script.",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
    )

    subparsers = parser.add_subparsers(title="Subcommands")

    #
    # list
    #

    parser_list = subparsers.add_parser("list")
    parser_list.add_argument(
        "path",
        nargs="?",
    )
    parser_list.set_defaults(func=app_obj.list_action)

    #
    # upload
    #

    parser_upload = subparsers.add_parser("upload")
    parser_upload.add_argument(
        "files",
        nargs="+",
        help="Local filepaths for files to be uploaded",
    )
    parser_upload.set_defaults(func=app_obj.upload_action)

    #
    # downlload
    #

    parser_download = subparsers.add_parser("download")
    parser_download.set_defaults(func=app_obj.download_action)

    args = parser.parse_args(cmd_args)
    return args


if __name__ == '__main__':
    main()
