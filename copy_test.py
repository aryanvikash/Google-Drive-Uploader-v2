def copy(origin_file_id, copy_path_id, service="SERVICE INSURANCE", copy_title=None):
    copied_file = {'parents': [{"id": copy_path_id}]}
    if copy_title is not None:
        copied_file['title'] = copy_title
    try:
        file_data = service.files().copy(fileId=origin_file_id, body=copied_file).execute()
        return file_data['id']
    except Exception as e:
        return e


def list_folder(FOLDER_ID, drive="DRIVE INSURANCE"):
    lists = drive.ListFile({"q": "'%s' in parents" % FOLDER_ID}).GetList()
    return lists


def copy_folder(FOLDER_ID, DEST, service="SERVICE of PYDRIVE", drive="DRIVE INSURANCE"):
    list_dir = list_folder(FOLDER_ID=FOLDER_ID)
    for x in list_dir:
        if x["mimeType"] == "application/vnd.google-apps.folder":
            current_dir_id = create_dir_in_folder(
                x["title"], DEST, drive)  # DEST is a folder dir while
            copy_folder(FOLDER_ID=x["id"], DEST=current_dir_id)
        else:
            a = copy(service, x["id"], DEST)
    return a


def create_dir_in_folder(FOLDER, PARANT, drive="DRIVE INSURANCE"):
    folder_metadata = {'title': FOLDER,
                       'mimeType': 'application/vnd.google-apps.folder'}
    if PARANT:
        folder_metadata['parents'] = [{"kind": "drive#fileLink", "id": PARANT}]
    folder = drive.CreateFile(folder_metadata)
    folder.Upload()
    return folder["id"]


# can clone folders of folder
