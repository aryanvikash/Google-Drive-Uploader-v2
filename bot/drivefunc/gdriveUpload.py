import logging as LOGGER
import logging as LOGGER
import os
from os import path

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from pydrive.files import ApiRequestError, FileNotDownloadableError, FileNotUploadedError

from config import Creds_path


class mydrive:
    def __init__(self, user_id):
        self.FOLDER_MIME_TYPE = "application/vnd.google-apps.folder"
        self.user_id = user_id
        self.drive = None
        self.http = None
        self.botfolder = "gdriveupmebot"
        self.gauth = GoogleAuth()
        self._parent_id = None
        self.is_teamdrive = False
        self._refresh_Token()
        self._set_botfolder()

    def _refresh_Token(self):
        self.gauth.LoadCredentialsFile(path.join(Creds_path, self.user_id))
        if self.gauth.credentials is None:
            # AUTHURL = gauth.GetAuthUrl()
            LOGGER.warning("User is not logged in")

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

    def _set_botfolder(self):

        # Check the files and folers in the root foled
        _file_list = self.drive.ListFile(
            {'q': "'root' in parents and trashed=false"}).GetList()
        for file_folder in _file_list:
            if file_folder['title'] == self.botfolder:
                # Get the matching folder id
                self._parent_id = file_folder['id']
                break
        else:
            # Create folder
            folder_metadata = {'title': self.botfolder,
                               'mimeType': 'application/vnd.google-apps.folder'}
            folder = self.drive.CreateFile(folder_metadata)
            folder.Upload()
            self._parent_id = folder['id']

    def __set_permission(self, drive_id):
        permissions = {
            'role': 'reader',
            'type': 'anyone',
            'value': None,
            'withLink': True
        }
        return self.service.permissions().create(supportsTeamDrives=True, fileId=drive_id, body=permissions).execute()

    def upload(self, file_path: str, parent_id: str = None):
        file_params = {'title': os.path.basename(file_path)}

        if parent_id:
            file_params['parents'] = [
                {"kind": "drive#fileLink", "id": parent_id}]
        else:
            file_params['parents'] = [
                {"kind": "drive#fileLink", "id": self._parent_id}]

        file_to_upload = self.drive.CreateFile(file_params)
        LOGGER.info("Uploading Starts :", file_path)
        file_to_upload.SetContentFile(file_path)
        file_to_upload.Upload(param={"http": self.http})
        file_to_upload.FetchMetadata()
        file_to_upload.InsertPermission({
            'type': 'anyone',
            'value': 'anyone',
            'role': 'reader',
            'withLink': True
        })

        LOGGER.info("Uploading Complete : ", file_path)
        return self._getInfo(file_to_upload['id'])

    def _getInfo(self, source_id: str):
        return self.service.files().get(supportsAllDrives=True, fileId=source_id,
                                        fields="title,id,mimeType,fileSize").execute()

    def _create_dir(self, dir_name: str = None, parent_id=None) -> str:
        # Create folder
        LOGGER.info("Folder Not Found !! Creating Folder")
        folder_metadata = {'title': dir_name,
                           'mimeType': 'application/vnd.google-apps.folder'}
        if parent_id:
            folder_metadata["parents"] = [{"id": parent_id}]
        folder = self.drive.CreateFile(folder_metadata)
        folder.Upload()
        folderid = folder['id']

        print('title: %s, id: %s' % (folder['title'], folderid))
        return folderid

    def deleteFile(self,id,permanent=False):
        try:
            deleteFileRef = self.drive.CreateFile({'id': id})
            if permanent:
               return deleteFileRef.Delete()
            else:
               return deleteFileRef.Trash()
            LOGGER.info(f"{id} Item Deleted permanently")
        except Exception as e:
            LOGGER.error(e)
            raise e


    def restore(self,id):
        try:
            restoreFileRef = self.drive.CreateFile({'id': id})
            restoreFileRef.UnTrash()
        except Exception as e:
            raise e



if __name__ == "__main__":
    try:
        d = mydrive("985378987")
        print(d.upload("/home/aryanvikash/test.txt"))
    except ApiRequestError as e:
        print("api req", e)
    except FileNotUploadedError as e:
        print("not upload", e)
    except FileNotDownloadableError as e:
        print("not uploadable", e)
    except Exception as e:
        print("exception", e)
