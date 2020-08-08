
from bot import LOGGER as _LOG

import math

from os import path
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

from config import Creds_path

OAUTH_SCOPE = ["https://www.googleapis.com/auth/drive",
               "https://www.googleapis.com/auth/drive.file",
               "https://www.googleapis.com/auth/drive.metadata"]

REDIRECT_URI = "urn:ietf:wg:oauth:2.0:oob"
G_DRIVE_DIR_MIME_TYPE = "application/vnd.google-apps.folder"
G_DRIVE_FILE_LINK = "📄 <a href='https://drive.google.com/open?id={}'>{}</a> __({})__"
G_DRIVE_FOLDER_LINK = "📁 <a href='https://drive.google.com/drive/folders/{}'>{}</a> __(folder)__"


class ProcessCanceled(Exception):
    """ raise if thread has terminated """


class Config(object):
    UNFINISHED_PROGRESS_STR = "-"
    FINISHED_PROGRESS_STR = "*"


class GdriveClone:
    def __init__(self, user_id):
        self._bot_clone_folder_name = 'gdriveupmeClone'
        self.user_id = user_id
        self.FOLDER_MIME_TYPE = "application/vnd.google-apps.folder"
        self._parent_id = "1MhqseCGWvNy8Xi0cZFNgW6iCClc18iCS"
        self.drive = None
        self.http = None
        self._is_canceled = False
        self.gauth = GoogleAuth()
        self.gauth.LoadCredentialsFile(path.join(Creds_path, self.user_id))
        self.service = None
        self.current_cloning_file = "N/A"
        self._list = 1
        self._completed = 0

        self._refreshToken()
        self._create_bot_folder()

    def _refreshToken(self):
        """ Refresh Gdrive Token  """
        if self._is_canceled:
            raise ProcessCanceled
        if self.gauth.credentials is None:
            _LOG.warning("user Not Logged in")
            raise Exception("User Not Authorised")
        elif self.gauth.access_token_expired:
            # Refresh them if expired
            self.gauth.Refresh()
            self.gauth.SaveCredentialsFile(path.join(Creds_path, self.user_id))
            self.gauth.Authorize()
            self.drive = GoogleDrive(self.gauth)
            self.http = self.drive.auth.Get_Http_Object()
            self.service = self.drive.auth.service
        else:
            # Initialize the saved creds
            self.gauth.Authorize()
            self.drive = GoogleDrive(self.gauth)
            self.http = self.drive.auth.Get_Http_Object()
            self.service = self.drive.auth.service
        _LOG.info("token Refreshed and authorised")

    def get_id_info(self, file_id):
        """  returns  id info"""
        _file_id = self.service.files().get(supportsAllDrives=True,
                                            fileId=file_id,
                                            fields="title,mimeType,id").execute()

        return _file_id

    def _create_bot_folder(self):
        # Check the files and folers in the root foled
        _file_list = self.drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
        for file_folder in _file_list:
            if file_folder['title'] == self._bot_clone_folder_name:
                # Get the matching folder id
                self._parent_id = file_folder['id']
                break
        else:
            # Create folder
            folder_metadata = {'title': self._bot_clone_folder_name,
                               'mimeType': 'application/vnd.google-apps.folder'}
            folder = self.drive.CreateFile(folder_metadata)
            folder.Upload()
            self._parent_id = folder['id']

    def _list_drive_dir(self, file_id: str) -> list:
        """ List Drive directory Items """
        # query = f"'{file_id}' in parents and (name contains '*')"
        fields = 'nextPageToken, items(id, title, mimeType)'
        query = f"'{file_id}' in parents"
        page_token = None

        files = []

        while True:
            response = self.service.files().list(supportsTeamDrives=True,
                                                 includeTeamDriveItems=True,
                                                 q=query, spaces='drive',
                                                 fields=fields,
                                                 corpora='allDrives',
                                                 pageToken=page_token).execute()

            files.extend(response.get('items', []))
            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break
            if self._is_canceled:
                raise ProcessCanceled

        return files

    def _copy_dir(self, file_id: str, parent_id: str) -> str:
        if self._is_canceled:
            raise ProcessCanceled

        files = self._list_drive_dir(file_id)

        if len(files) == 0:
            return parent_id
        self._list += len(files)
        new_id = None

        for file_ in files:
            if file_['mimeType'] == G_DRIVE_DIR_MIME_TYPE:
                dir_id = self._create_drive_dir(file_['title'], parent_id)
                new_id = self._copy_dir(file_['id'], dir_id)
            else:
                self._copy_file(file_['id'], parent_id)
                new_id = parent_id
        return new_id

    def _copy_file(self, file_id: str, parent_id: str) -> str:
        _File = self.service.files().get(supportsAllDrives=True,
                                         fileId=file_id,
                                         fields="title").execute()
        if self._is_canceled:
            raise ProcessCanceled
        body = {'title': _File['title'], "parents": [{"id": parent_id}]}
        # if parent_id:
        #     body["parents"] = [parent_id]

        drive_file = self.service.files().copy(
            body=body, fileId=file_id, supportsTeamDrives=True).execute()

        percentage = (self._completed / self._list) * 100
        tmp = \
            "__Copying Files In GDrive...__\n" + \
            "```[{}{}]({}%)```\n" + \
            "**Completed** : `{}/{}`"
        self._progress = tmp.format(
            "".join((Config.FINISHED_PROGRESS_STR
                     for _ in range(math.floor(percentage / 5)))),
            "".join((Config.UNFINISHED_PROGRESS_STR
                     for _ in range(20 - math.floor(percentage / 5)))),
            round(percentage, 2),
            self._completed,
            self._list)

        self._completed += 1
        _LOG.info(f"Copied Google-Drive File => Name: {drive_file['title']} ID: {drive_file['id']}")
        return drive_file['id']

    def _create_drive_dir(self, dir_name: str, parent_id: str) -> str:
        """ Create Folder in drive and return id"""
        _LOG.info(dir_name, parent_id)
        body = {"title": dir_name, "mimeType": G_DRIVE_DIR_MIME_TYPE}
        if parent_id:
            body["parents"] = [{"id": parent_id}]
        folder_ = self.drive.CreateFile(metadata=body)
        folder_.Upload()
        _LOG.info("folder created", folder_['title'])
        folder_id = folder_.get("id")
        folder_name = folder_.get("title")

        _LOG.info("Created Google-Drive Folder => Name: %s ID: %s ", folder_name, folder_id)
        return folder_id

    def copyHandler(self, file_id: str):
        """  will handle file Or folder clone """

        drive_file = self.service.files().get(
            supportsAllDrives=True, fileId=file_id, fields="title,id,mimeType").execute()

        if drive_file['mimeType'] == G_DRIVE_DIR_MIME_TYPE:

            dir_id = self._create_drive_dir(drive_file['title'], self._parent_id)
            self._copy_dir(file_id, dir_id)
            ret_id = dir_id
        else:

            ret_id = self._copy_file(file_id, self._parent_id)

        return self.get_id_info(ret_id)


if __name__ == "__main__":

    try:
        gd = GdriveClone("985378987")
        gd.get_id_info('1DkCqtMGjUfxMXxJMOddcDUChX9O5fpa3')
        # print("cloning done:", gd.copyHandler("1r0cx9AOUO2Mflq3mUDqbKlxYqaXqSIZW"))
    except Exception as e:
        print("clone Err lol:", e)
