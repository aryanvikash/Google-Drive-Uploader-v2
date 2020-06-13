#!/usr/bin/env python3


import asyncio
import argparse
import json
import os
import os.path as path
import re

from bot.helper.utils import listdir

from bot import Creds_path ,LOGGER
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
IS_TEAM_DRIVE = False
# Creds_path= "/mnt/c/Users/Aryan Vikash/Desktop/Pyrogdrive/creds"
# ID = "920262337"
FOLDER_MIME_TYPE = 'application/vnd.google-apps.folder'
BotCloneFolderName = "GdriveUpmeClone"


drive: GoogleDrive
http = None
initial_folder = None


def gupload(filename: str ,ID = None, parent_folder: str="Gdriveupmebot") -> None:
    drive: GoogleDrive
    http = None
    # initial_folder = None
    gauth: drive.GoogleAuth = GoogleAuth()
    gauth.LoadCredentialsFile(path.join(Creds_path, ID))
    if gauth.credentials is None:
        # AUTHURL = gauth.GetAuthUrl()
        print("not Auth Users")

    elif gauth.access_token_expired:
        # Refresh them if expired
        gauth.Refresh()
        gauth.SaveCredentialsFile(path.join(Creds_path, ID))
        gauth.Authorize()
    else:
        # Initialize the saved creds
        gauth.Authorize()
    drive = GoogleDrive(gauth)
    http = drive.auth.Get_Http_Object()
    if not path.exists(filename):
        print(f"Specified filename {filename} does not exist!")
        return
    # print(filename)

    if parent_folder:

        # Check the files and folers in the root foled
        file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
        for file_folder in file_list:
            if file_folder['title'] == parent_folder:
                # Get the matching folder id
                folderid = file_folder['id']
                print("Folder Already Exist  !!  Trying To Upload")
                # We need to leave this if it's done
                break
        else:
            # Create folder
            folder_metadata = {'title': parent_folder,
                               'mimeType': 'application/vnd.google-apps.folder'}
            folder = drive.CreateFile(folder_metadata)
            folder.Upload()
            folderid = folder['id']
            # Get folder info and print to screen
            foldertitle = folder['title']
            # folderid = folder['id']
            print('title: %s, id: %s' % (foldertitle, folderid))

    file_params = {'title': filename.split('/')[-1]}
    if parent_folder:
        file_params['parents'] = [{"kind": "drive#fileLink", "id": folderid}]
    try:
        file_to_upload = drive.CreateFile(file_params)
        file_to_upload.SetContentFile(filename)
        file_to_upload.Upload(param={"http": http})
        file_to_upload.FetchMetadata()
        file_to_upload.InsertPermission({
            'type': 'anyone',
            'value': 'anyone',
            'role': 'reader',
            'withLink': True
        })
        # SEND msg file_to_upload['webContentLink']
        LOGGER.info(file_to_upload['webContentLink'])
        
        # loop = asyncio.get_event_loop()
        # loop.run_until_complete(sendMsg(event, file_to_upload['webContentLink']))
        # asyncio.run(sendMsg(event, file_to_upload['webContentLink']))

        return file_to_upload['webContentLink']
    except Exception as e:
        LOGGER.error(e)

        return e






# class Based file Clone
class mydrive:

    def __init__(self,ID):
        self.FOLDER_MIME_TYPE = "application/vnd.google-apps.folder"
        self.BotCloneFolderName = "GdriveUpmeClone"
        self.drive: GoogleDrive
        self.http = None
        self.gauth: drive.GoogleAuth = GoogleAuth()
        print(ID)
        self.gauth.LoadCredentialsFile(path.join(Creds_path, ID))
        print(ID)
        if self.gauth.credentials is None:
            # AUTHURL = gauth.GetAuthUrl()
            print("Not Auth Users")

        # if not os.path.isfile(os.path.join(Creds_path,ID) ):
        #     print("path : ", Creds_path)
        #     print("Creds: ", os.path.join(Creds_path,ID))
        #     print("not auth")


        elif self.gauth.access_token_expired:
            # Refresh them if expired
            self.gauth.Refresh()
            self.gauth.SaveCredentialsFile(path.join(Creds_path, ID))
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
        # if not path.exists(filename):
        #     print(f"Specified filename {filename} does not exist!")
        #     return

    def __set_permission(self, drive_id):
        permissions = {
            'role': 'reader',
            'type': 'anyone',
            'value': None,
            'withLink': True
        }
        return self.service.permissions().create(supportsTeamDrives=True, fileId=drive_id, body=permissions).execute()
        
    def uploadfile(self , filename: str , parent_folder :str = None) :

            if not path.exists(filename):
                print(f"Specified filename {filename} does not exist!")
                return
            # print(filename)


            file_params = {'title': filename.split('/')[-1]}

            if parent_folder:
                folderid = self.createfolder_with_name("megadownload")
                file_params['parents'] = [{"kind": "drive#fileLink", "id": folderid}]
            try:
                LOGGER.info(f"Uploading Satarted : {filename}")
                file_to_upload = self.drive.CreateFile(file_params)
                file_to_upload.SetContentFile(filename)
                file_to_upload.Upload(param={"http": self.http})
                file_to_upload.FetchMetadata()
                file_to_upload.InsertPermission({
                    'type': 'anyone',
                    'value': 'anyone',
                    'role': 'reader',
                    'withLink': True
                })
            
                LOGGER.info(f"Uploading Complete : {filename}")
                return file_to_upload['webContentLink']
            except Exception as e:
                # LOGGER.error(e)
                print(e)

                # return e



    def getId(self,link):
            # link = link.rstrip('export=download').rstrip('&')
            link = link.translate({ord('&'): None}).replace("export=download"," ").strip()

            if link.find("view") != -1:
                file_id = link.split('/')[-2]
            elif link.find("open?id=") != -1:
                file_id = link.split("open?id=")[1].strip()
            elif link.find("uc?id=") != -1:
                file_id = link.split("uc?id=")[1].strip()
            elif link.find("file/d/") != -1:
                file_id = link.split("/")[-1].strip()
            elif link.find("id=") != -1:
                file_id = link.split("=")[-1].strip()
            elif link.find("/folders/") != -1:
                file_id = link.split("folders/")[-1].strip()
            else:
                file_id = 'not found'

            return file_id

    
    def copy_file(self,file_id,my_file_title ,dest_folder_id):
        copied_file = {'title': my_file_title,"parents":[{"id":dest_folder_id}]}
        f = self.service.files().copy(supportsAllDrives=True,fileId=file_id, body=copied_file).execute()
        try:
            return  f['title'],f['fileSize'], f['webContentLink']
        except Exception as e:
            print(e)
            return  


    #TODO Fix folder upload
    # def copyFolder(self,name,local_path,folder_id,parent_id):
    #     page_token = None
    #     q =f"'{folder_id}' in parents"
    #     files = []
    #     LOGGER.info(f"Syncing: {local_path}")
    #     new_id = None
    #     while True:
    #         response = self.service.files().list(q=q,
    #                                               spaces='drive',
    #                                               fields='nextPageToken, files(id, name, mimeType,size)',
    #                                               pageToken=page_token).execute()
    #         for file in response.get('files', []):
    #             files.append(file)
    #         page_token = response.get('nextPageToken', None)
    #         if page_token is None:
    #             break  
    #     if len(files) == 0:
    #         return parent_id
    #     for file in files:
    #         if file.get('mimeType') == selff.__G_DRIVE_DIR_MIME_TYPE:
    #             file_path = os.path.join(local_path,file.get('name'))
    #             current_dir_id = self.create_directory(file.get('name'),parent_id)
    #             new_id = self.cloneFolder(file.get('name'),file_path,file.get('id'),current_dir_id) 
    #         else:
    #             self.transferred_size += int(file.get('size'))
    #             try:
    #                 self.copyFile(file.get('id'),parent_id)
    #                 new_id = parent_id
    #             except Exception as e:
    #                 if isinstance(e,RetryError):
    #                     LOGGER.info(f"Total Attempts: {e.last_attempt.attempt_number}")
    #                     err = e.last_attempt.exception()
    #                 else:
    #                     err = e
    #                 LOGGER.error(err)
    #     return new_id


    def getInfo(self,source_id : str):
        info = self.service.files().get(supportsAllDrives=True,fileId=source_id,fields="title,id,mimeType,fileSize").execute()
        return info

    def getFolderitem(self ,folder_id ,parent_id = None):
        # List Everything In that {folder_id}
        q =f"'{folder_id}' in parents"
        page_token = None
        rawitems=[]
        files = []
        folders = []
        while True:
            response = self.service.files().list(q=q,supportsAllDrives=True,
                                                includeItemsFromAllDrives=True,
                                                  spaces='drive',
                                                  fields='nextPageToken, items(id, title, mimeType)',
                                                  pageToken=page_token).execute()
            
            for item in response.get('items', []):
                rawitems.append(item)

            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break 

        
        if len(rawitems) == 0:
            return parent_id
        else:
            for item in rawitems :
                
                if item.get("mimeType") == FOLDER_MIME_TYPE:
                    folders.append(item)
                    
                else:
                    files.append(item)

            
            return files ,folders
    


#TODO temp  workaround to clone folder
    def cloneFolder(self,folder_id):
        folder = ""
        files =""
        files , folders = self.getFolderitem(folder_id)

        #Get Folder Name Of recived id
        folderinfo = self.getInfo(folder_id)
        cloneParentFolderId = folderinfo.get("id")
        
        folder_title = folderinfo.get("title")

        #Create Bot Default Folder
        botcloneFolderId = self.createfolder_with_name(BotCloneFolderName)
        
        # Create Parentfoldr Inside Bot default Folder
        cloneParentFolderId  = self.create_dir(folder_title,botcloneFolderId)
        folder_url = f"https://drive.google.com/drive/u/0/folders/{cloneParentFolderId}"

        #copy file in parent id
        print("length of file : ",len(files)) 
        # if len(files) > 0:
        #     for file in files:
        #         file_id = file.get("id")
        #         file_title = file.get("title")
        #         self.copy_file(file_id,file_title,cloneParentFolderId)
        #         print("copy File",file_title)
                
             #clone Folder Inside Folder
        self.ResCopyFile(files,cloneParentFolderId)
        print("foldeer length ",len(folders))
        
        if len(folders) > 0:
            for folder  in folders :
                # self.ResCopyFolder(folder)
                cloneParentFolderId =  self.create_dir(folder.get("title") , cloneParentFolderId)
                files , folders = self.getFolderitem(folder.get("id"))
                for file in files:
                    file_id = file.get("id")
                    file_title = file.get("title")
                    self.copy_file(file_id,file_title,cloneParentFolderId)
                    print(" Folder Cloned :",file_title , "\n\n\n")

                # if len(folders) > 0:
                #     for folder  in folders :
                #         # self.ResCopyFolder(folder)
                #         cloneParentFolderId =  self.create_dir(folder.get("title") , cloneParentFolderId)
                #         files , folders = self.getFolderitem(folder.get("id"))
                #         for file in files:
                #             file_id = file.get("id")
                #             file_title = file.get("title")
                #             self.copy_file(file_id,file_title,cloneParentFolderId)
                #             print(" Folder Cloned :",file_title , "\n\n\n")

        print("clone Complete")
        return folder_title ,folder_url

        
        

    def ResCopyFolder(self,folder):
        
                userParentFolderId =  folder.get("id")
                cloneParentFolderId =  self.create_dir(folder.get("title") , userParentFolderId)
                files , folders = self.getFolderitem(folder.get("id"))
                self.ResCopyFile(files,cloneParentFolderId)
                if len(folders) > 0:
                    for f in folders:
                        self.ResCopyFile(files,f.get("id"))
                # for file in files:
                #     file_id = file.get("id")
                #     file_title = file.get("title")
                #     self.copy_file(file_id,file_title,cloneParentFolderId)
                #     print(" Folder Cloned :",file_title , "\n\n\n")


    def ResCopyFile(self,files,ParentFolderId):
        if len(files) > 0:
            for file in files:
                print("coping file...",file.get("title"))
                file_id = file.get("id")
                file_title = file.get("title")
                self.copy_file(file_id,file_title,ParentFolderId)
                print("copy File",file_title)


    # def getitemids(self,items):

    #TODO fix it 
    # def create_directory(self, directory_name, parent_id):
    #     file_metadata = {
    #         "name": directory_name,
    #         "mimeType": self.FOLDER_MIME_TYPE
    #     }
    #     if parent_id is not None:
    #         file_metadata["parents"] = [parent_id]
    #     file = self.service.files().create(supportsTeamDrives=True, body=file_metadata).execute()
    #     file_id = file.get("id")
    #     if not IS_TEAM_DRIVE:
    #         self.__set_permission(file_id)
    #     LOGGER.info("Created Google-Drive Folder:\nName: {}\nID: {} ".format(file.get("name"), file_id))
    #     return file_id




    def createfolder_with_name(self,parent_folder_name: str =None ,dest_id = None):
        """
        (search by title)
        This function for searching Folder Name and creating new folder if it don't exist

        """
        if parent_folder_name:
            # Check the files and folder in the root 
            file_list = self.drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
            for file_folder in file_list:
                if file_folder['title'] == parent_folder_name:
                    # Get the matching folder id
                    folderid = file_folder['id']
                    LOGGER.info(f"We Found Your Folder :{parent_folder_name}")
                    # We need to leave this if it's done
                    return folderid


                else:
                    # Create folder
                    LOGGER.info("Folder Not Found !! Creating Folder")
                    folder_metadata = {'title': parent_folder_name,
                                    'mimeType': 'application/vnd.google-apps.folder'}

                    # file = self.service.files().create(supportsTeamDrives=True, body=file_metadata).execute()
                    #     file_id = file.get("id")
                    
                    if dest_id is not None:
                        folder_metadata["parents"] = [{"id":dest_id}]
                    folder = self.drive.CreateFile(folder_metadata)
                    folder.Upload()
                    folderid = folder['id']
                    # Get folder info and print to screen
                    foldertitle = folder['title']
                    # folderid = folder['id']
                    print('title: %s, id: %s' % (foldertitle, folderid))
                    return folderid

    def create_dir(self,parent_folder_name: str =None ,dest_id = None):
            folder_metadata = {'title': parent_folder_name,
                            'mimeType': 'application/vnd.google-apps.folder'}

            # file = self.service.files().create(supportsTeamDrives=True, body=file_metadata).execute()
            #     file_id = file.get("id")
            
            if dest_id is not None:
                folder_metadata["parents"] = [{"id":dest_id}]
            folder = self.drive.CreateFile(folder_metadata)
            folder.Upload()
            folderid = folder['id']
            # Get folder info and print to screen
            foldertitle = folder['title']
            # folderid = folder['id']
            print('title: %s, id: %s' % (foldertitle, folderid))
            return folderid

    # def FolderUpload(self,dir) :
    #     if os.path.isdir(dir):
    #         foldername = os.path.basename(dir)
    #         folderId = self.createfolder_with_name(foldername)
    #         files,folders = listdir(dir)
    #         if len(files)>0:
    #             for file in files :
    #                 uplod()

        
    #  def upload_dir(self, input_directory, parent_id):
    #     list_dirs = os.listdir(input_directory)
    #     folderId = self.createfolder_with_name(foldername)
    #     if len(list_dirs) == 0:
    #         return parent_id
    #     new_id = None
    #     for item in list_dirs:
    #         current_file_name = os.path.join(input_directory, item)
    #         if os.path.isdir(current_file_name):
    #             current_dir_id = self.create_directory(item, parent_id)
    #             new_id = self.upload_dir(current_file_name, current_dir_id)
    #         else:
    #             self.uploadfile(filename,)
    #             new_id = parent_id
    #     return new_id
    
    def clone(self,url):
        try:
            public_id =self.getId(url)
            LOGGER.info(f"Drive Clone Item ID  : {public_id}")
            if self.getInfo(public_id).get("mimeType") == FOLDER_MIME_TYPE:
                LOGGER.info("Folder Cloning started")
                title,link = self.cloneFolder(public_id)
                return title,None,link,None
            else:
                LOGGER.info("File Cloning started")
                public_file_title = self.getInfo(public_id).get("title")
                destId = self.createfolder_with_name("gdriveupmebotclone")
                title ,size ,link =  self.copy_file(public_id,public_file_title,destId)
                return title,size,link,None
        except Exception as e:
            LOGGER.error(f"Clone  error : {e}")
            raise e
            return None,None,None,e

        

# if __name__ == "__main__":
    # url = "https://drive.google.com/open?id=1zB2mhW0qnnuIH2jmWdo3YZHOx4o2z6e9"
    # d = mydrive()

    # public_id =d.getId(url)
    # public_file_title = d.getInfo(public_id).get("title")
    # print(public_file_title)
    # idINfo = d.getInfo(d.getId(url)) 
    # print(idINfo)
    # print(d.copy_file("1zB2mhW0qnnuIH2jmWdo3YZHOx4o2z6e9"))
    # print(meta)


