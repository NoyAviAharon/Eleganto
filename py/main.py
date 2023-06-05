import requests
from pathlib import Path
import json
import webbrowser
from concurrent.futures import ThreadPoolExecutor
import mysql.connector


def get_access_token():
    url = "https://developer.api.autodesk.com/authentication/v1/authenticate"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "grant_type": "client_credentials",
        "scope": "data:read data:write",
        "redirect_uri": "http://localhost:8080/api/auth/callback",
        "client_id": "8ccmbBbmbmj4TiTJGIgyGwi9XpCerjYW",
        "client_secret": "OcK8NvW7a0D39WcU",
        "grant_type": "client_credentials"
    }

    response = requests.post(url, headers=headers, data=data)

    if response.status_code == 200:
        json_response = response.json()
        print("=============== get_access_token ============")
        print(json.dumps(json_response, indent=4))
    else:
        print("Error:", response.status_code, response.content)

    res_json = response.json()
    return res_json["access_token"]


def create_auth_header(access_token):
    return {'Authorization': f'Bearer {access_token}'}


def create_photoscene(headers, scenename='res'):
    url = 'https://developer.api.autodesk.com/photo-to-3d/v1/photoscene'
    data = {
        'scenename': scenename,
        'format': 'obj'
    }
    response = requests.post(url, headers=headers, data=data)
    json_response = response.json()
    print("=============== create_photoscene ============")
    print(json.dumps(json_response, indent=4))
    photoscene_id = json_response["Photoscene"]["photosceneid"]
    return photoscene_id


import os


def list_files_in_folder(folder_path):
    """
    Lists all files in a given folder.

    Args:
        folder_path (str): The path of the folder to list files from.

    Returns:
        List[str]: A list of file names in the folder.
    """
    files = []
    try:
        # Iterate through all items in the folder
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            # Check if the item is a file
            if os.path.isfile(item_path) and item_path.lower().endswith(".jpg"):
                files.append(item)
    except Exception as e:
        print(f"Error listing files in folder: {e}")
    return files


def upload_images(headers, photoscene_id):
    base_dir = "/Users/noy/Documents/sadna_api/"
    base_dir = os.path.join(base_dir, "noy")
    file_names = list_files_in_folder(base_dir)
    url = "https://developer.api.autodesk.com/photo-to-3d/v1/file"
    data = {
        "photosceneid": photoscene_id,
        "type": "image"
    }
    with ThreadPoolExecutor(max_workers=1) as executor:
        for filename in file_names:
            executor.submit(upload_file, base_dir, data, filename, headers, url)


def upload_file(base_dir, data, filename, headers, url):
    files = [(f"file[0]", (filename, open(Path(base_dir) / Path(filename), "rb"), 'image/jpg'))]
    # print(files)
    response = requests.post(url, headers=headers, data=data, files=dict(files))
    if response.status_code == 200:
        json_response = response.json()
        print("=============== upload_images ============")
        print(json.dumps(json_response, indent=4))
    else:
        print("Error:", response.status_code, response.content)


def start_create_3d_obj(headers, photoscene_id):
    url = f"https://developer.api.autodesk.com/photo-to-3d/v1/photoscene/{photoscene_id}"
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        json_response = response.json()
        print("=============== start_create_3d_obj ============")
        print(json.dumps(json_response, indent=4))
    else:
        print("Error:", response.status_code, response.content)


def progress_status(headers, photoscene_id):
    status = 0
    url = f'https://developer.api.autodesk.com/photo-to-3d/v1/photoscene/{photoscene_id}/progress'
    while status != 100:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            progress_data = response.json()
            json_response = response.json()
            print("=============== progress_status ============")
            print(json.dumps(json_response, indent=4))

            status = int(progress_data.get("Photoscene", {}).get('progress', 0))
            print(f'Status: {status=}%')
        else:
            print('Failed to get progress:', response.status_code, response.text)


def get_obj_link(headers, photoscene_id):
    url = f'https://developer.api.autodesk.com/photo-to-3d/v1/photoscene/{photoscene_id}?format=obj'
    data = dict(format="obj")
    response = requests.get(url, headers=headers, params=data)
    json_response = response.json()

    print("=============== upload_images ============")
    print(json.dumps(json_response, indent=4))

    scenelink = json_response["Photoscene"]["scenelink"]
    return scenelink



def download_file(url):
    import os
    import requests
    import zipfile

    dest_folder = 'models/'
    os.makedirs(dest_folder, exist_ok=True)
    zip_filename = url.split('/')[-1].replace(" ", "_")
    zip_filename = zip_filename.split("?")[0]
    print(zip_filename.split("?")[0])
    zip_path = os.path.join(dest_folder, zip_filename)
    print(zip_path)
    r = requests.get(url, stream=True)
    open(zip_path, "wb").write(r.content)

    return zip_path



def upload_model(path, model_name):
    print("=============== upload_model ============")
    import requests

    url = "https://api.echo3D.com/upload"

    payload = {'key': 'orange-hall-7575',
               'email': 'noyki@ac.il',
               'target_type': 2,
               'hologram_type': 2,
               'secKey': 'BfSdNm5nqQDDMuXO7t8AFznG',
               'type': 'upload'
               }
    files = [
        ('file_model', (f"{model_name}.zip", open(path, 'rb'))),
    ]

    response = requests.post(url, data=payload, files=files)
    response_json = response.json()
    return response_json["additionalData"]["shortURL"]


def insert_to_db(model_name, link):
    myconn = mysql.connector.connect(host="mtapanel.mtacloud.co.il", user="korenta_Elega1", passwd="123456", db="korenta_DB1")
    cur = myconn.cursor()
    sql = "insert into Model_link(model_name, model_link) values (%s, %s)"
    val = (model_name, link)
    try:
        cur.execute(sql, val)
        myconn.commit()
    except:
        myconn.rollback()
    print(cur.rowcount, "record inserted!")
    # print(cur.)
    myconn.close()


if __name__ == "__main__":
    if False:
        access_token = get_access_token()

        headers = create_auth_header(access_token=access_token)
    # photoscene_id = create_photoscene(headers=headers)
    # upload_images(headers=headers, photoscene_id=photoscene_id)
    # from time import sleep
    # sleep(60)

        photoscene_id = "1NZa2jParwHR3xdryfBhYmXGhOCZGdevzdh4Y9E8U8E"
        start_create_3d_obj(headers=headers, photoscene_id=photoscene_id)
        progress_status(headers=headers, photoscene_id=photoscene_id)
        obj_link = get_obj_link(headers=headers, photoscene_id=photoscene_id)
        zip_path = download_file(obj_link)
        model_name = str(input("please provide model name without any special characters and spaces"))
        echo3d_link = upload_model(zip_path, model_name=model_name)

    insert_to_db("Sal_Noy", "https://go.echo3d.co/Vjuf")
