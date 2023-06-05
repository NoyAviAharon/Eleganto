import requests
from pathlib import Path
import json
import webbrowser
from concurrent.futures import ThreadPoolExecutor
import mysql.connector
import os
from time import sleep
import tkinter as tk
from tkinter import ttk
import time
import threading
from tkinter.messagebox import showinfo



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


def upload_images(headers, photoscene_id, desktop_path):
    completion_label = tk.Label(window, text="", font=("Arial", 12))
    completion_label.pack()
    base_dir = desktop_path
    file_names = list_files_in_folder(base_dir)
    url = "https://developer.api.autodesk.com/photo-to-3d/v1/file"
    data = {
        "photosceneid": photoscene_id,
        "type": "image"

    }
    progress['maximum'] = 100
    completed = 0
    total_files = len(file_names)
    with ThreadPoolExecutor(max_workers=1) as executor:
        for filename in file_names:
            completed = executor.submit(upload_file, base_dir, data, filename, headers, url, completed).result()

            percent_done = int((completed / total_files) * 100)
            progress['value'] = percent_done
            percent_label.config(text=f"{percent_done}%")
            window.update_idletasks()

        if percent_done == 100:
            # Display completion message and continue button
            completion_label = tk.Label(window, text="upload completed!", font=("Arial", 12))
            completion_label.pack(pady=10)

            continue_button = tk.Button(window, text="To continue", command=start_progress)
            continue_button.pack(pady=10)






def upload_file(base_dir, data, filename, headers, url, completed):
    files = [(f"file[0]", (filename, open(Path(base_dir) / Path(filename), "rb"), 'image/jpg'))]

    response = requests.post(url, headers=headers, data=data, files=dict(files))
    if response.status_code == 200:
        json_response = response.json()
        print("=============== upload_images ============")
        print(json.dumps(json_response, indent=4))

        # Increase completed by 1
        completed += 1
    else:
        print("Error:", response.status_code, response.content)

    return completed



def start_create_3d_obj(headers, photoscene_id):
    url = f"https://developer.api.autodesk.com/photo-to-3d/v1/photoscene/{photoscene_id}"
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        json_response = response.json()
        print("=============== start_create_3d_obj ============")
        print(json.dumps(json_response, indent=4))
    else:
        print("Error:", response.status_code, response.content)


def update_progress(progress, percent_label, status):
    percent_done = int(status)
    progress['value'] = percent_done
    percent_label.config(text=f"{percent_done}%")
    window.update_idletasks()

def progress_status(headers, photoscene_id, progress, percent_label):
    status = 0
    url = f'https://developer.api.autodesk.com/photo-to-3d/v1/photoscene/{photoscene_id}/progress'
    progress['maximum'] = 100  # Set the maximum value for the progress bar
    while status != 100:
        # Make API request to get progress
        sleep(2)
        access_token = get_access_token()
        headers = create_auth_header(access_token=access_token)
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            progress_data = response.json()
            json_response = response.json()
            print("=============== progress_status ============")
            print(json.dumps(json_response, indent=4))

            status = int(progress_data.get("Photoscene", {}).get('progress', 0))
            print(f'Status: {status=}%')

            # Update progress in the Tkinter window
            update_progress(progress, percent_label, status)
        else:
            print('Failed to get progress:', response.status_code, response.text)
        if status == 100:
            # Display completion message and continue button
            completion_label = tk.Label(window, text="your model is ready!", font=("Arial", 18))
            completion_label.pack(pady=10)

            continue_button = tk.Button(window, text="To continue", command=create_window)
            continue_button.pack(pady=10)


def start_progress():
    photoscene_id = get_photoscene_id()
    print(photoscene_id)
    clear_window(window)
    progress_label = tk.Label(window, text="Progress:", font=("Arial", 14))
    progress_label.pack(pady=10)

    # Instruction Label
    instruction_label = tk.Label(window, text="We create your 3D model\n This may take time, please be patient",
                                 font=("Arial", 10))
    instruction_label.pack(pady=10)

    # Progress Bar
    progress = ttk.Progressbar(window, orient=tk.HORIZONTAL, length=200, mode='determinate')
    progress.pack(pady=12)

    # Percentage Label
    percent_label = tk.Label(window, text="0%", font=("Arial", 12))
    percent_label.pack()

    access_token = get_access_token()
    headers = create_auth_header(access_token=access_token)

    start_create_3d_obj(headers=headers, photoscene_id=photoscene_id)

    progress_status(headers, photoscene_id, progress, percent_label)



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
    print(model_name)

    url = "https://api.echo3D.com/upload"

    payload = {
        'key': 'orange-hall-7575',
        'email': 'noyki@ac.il',
        'target_type': 2,
        'hologram_type': 2,
        'secKey': 'BfSdNm5nqQDDMuXO7t8AFznG',
        'type': 'upload'
    }

    response = None
    try:
        with open(path, 'rb') as file:
            file_size = os.path.getsize(path)
            uploaded_size = 0

            files = [('file_model', (f"{model_name}.zip", file))]
            response = requests.post(url, data=payload, files=files, stream=True)

            if response.status_code == 200:
                response_json = response.json()
                echo3d_link = response_json["additionalData"]["shortURL"]
                print(response.text)
                print(response.content)
                print(response.status_code)
                print(response_json)
                return echo3d_link

    except Exception as e:
        if response:
            print(response.text)
        print("Upload failed:", str(e))

    return None



def change_color():
    import requests

    # Set the necessary variables
    api_key = 'orange-hall-7575'
    model_id = "eb7b9a73-190f-4523-a16c-2f42c3f0c6ba"
    new_color = '#FF0000'  # Specify the new color in hexadecimal format

    # Set the API endpoint URL
    url = f'https://api.echo3d.co/v1/models/{model_id}'

    # Set the headers with the API key
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }

    # Construct the payload with the new color
    payload = {
        'color': new_color
    }

    # Send the PUT request to update the model color
    response = requests.put(url, json=payload, headers=headers)

    # Check the response status
    if response.status_code == 200:
        print('Model color updated successfully.')
    else:
        print('Failed to update the model color.')
        print(response.text)
        print(response.content)
        print('Response:', response.json())


def insert_to_db(model_name, link):
    myconn = mysql.connector.connect(host="mtapanel.mtacloud.co.il", user="korenta_Elega1", passwd="123456",
                                     db="korenta_DB1")
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

def get_photoscene_id():
    file_path = 'photoscene_id.txt'
    with open(file_path, 'r') as file:
        photoscene_id = file.read()
        return photoscene_id

def get_text():
    value = entry.get()
    print("the 3D model was uploaded with the name: ", value)







# def simulate_loading(file_names):
#     progress['maximum'] = 100
#     i=0
#     for filename in file_names:
#         time.sleep(0.05)  # Simulate some processing time
#         progress['value'] = filename
#         percent_label.config(text=f"{i}%")
#         window.update_idletasks()
#         i+=1

# def create_loading_profile():


def close_window():
    window.destroy()


def clear_window(window):
    # Destroy all widgets in the window
    for widget in window.winfo_children():
        widget.destroy()

    # Update the window to reflect the changes
    window.update()

def save_model_name():
    global model_name
    model_name = model_name_entry.get()
    print(model_name)



def upload_model_and_insert_to_db():
    print(model_name)
    echo3d_link = upload_model(zip_path, model_name=model_name)
    insert_to_db(model_name, echo3d_link)




def create_window():
    photoscene_id = get_photoscene_id()
    obj_link = get_obj_link(headers=headers, photoscene_id=photoscene_id)
    global zip_path
    zip_path = download_file(obj_link)
    global model_name_entry, window
    window = tk.Tk()
    window.title("Model Name Input")
    window.geometry("400x200")
    window.resizable(False, False)

    model_name_label = tk.Label(window, text="Model Name:", font=("Arial", 15))
    model_name_label.pack(pady=10)
    instruction_label = tk.Label(
        window,
        text="Please provide a name without any special characters and spaces",
        font=("Arial", 12)
    )
    instruction_label.pack(pady=10)
    model_name_entry = tk.Entry(window, font=("Arial", 12))
    model_name_entry.pack(pady=5)

    upload_button = tk.Button(window, text="Upload", command=upload)
    upload_button.pack(pady=10)

    window.mainloop()





def upload():
    global model_name
    model_name = model_name_entry.get()

    progress_window = tk.Toplevel()
    progress_window.title("Uploading...")
    progress_window.geometry("300x100")

    progress_label = tk.Label(progress_window, text="Uploading...")
    progress_label.pack(pady=10)

    progress_bar = ttk.Progressbar(progress_window, length=200, mode='indeterminate')
    progress_bar.pack(pady=5)

    # Start the upload in a separate thread
    upload_thread = threading.Thread(target=upload_model_and_insert_to_db)
    upload_thread.start()

    def check_upload_status():
        if upload_thread.is_alive():
            progress_window.after(100, check_upload_status)
        else:
            progress_window.destroy()
            showinfo("Upload Complete", "Upload completed successfully!")

    progress_window.after(100, check_upload_status)
    progress_window.mainloop()



if __name__ == "__main__":
    access_token = get_access_token()
    headers = create_auth_header(access_token=access_token)
    photoscene_id = create_photoscene(headers=headers)


    file_path = 'photoscene_id.txt'
    with open(file_path, 'w') as file:
        file.write(photoscene_id)

    print(f"photoscene_id saved to {file_path}")
    folder_name = 'images/'
    desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop', folder_name)
    os.makedirs(desktop_path, exist_ok=True)
    #upload_images(headers=headers, photoscene_id=photoscene_id,desktop_path=desktop_path)

    global window, progress, percent_label
    window = tk.Tk()
    window.title("Loading  images Profile")
    window.geometry("700x400")
    window.resizable(False, False)
    # Instruction Label
    instruction_label = tk.Label(window,
                                 text="A  folder has been created on your desktop,\n please upload the images you want to turn into a 3D model into this folder",
                                 font=("Arial", 18))
    instruction_label.pack(pady=10)

    # Progress Bar
    progress = ttk.Progressbar(window, orient=tk.HORIZONTAL, length=200, mode='determinate')
    progress.pack(pady=12)

    # Percentage Label
    percent_label = tk.Label(window, text="0%", font=("Arial", 12))
    percent_label.pack()

    # Instruction Label
    instruction_label = tk.Label(window, text="Click start after you have uploaded the images to the folder",
                                 font=("Arial", 10))
    instruction_label.pack(pady=10)

    # Start Button
    start_button = tk.Button(window, text="Start", command=lambda: upload_images(headers, photoscene_id, desktop_path))
    start_button.pack(pady=10)

    window.mainloop()

    sleep(60)

    photoscene_id=get_photoscene_id()


    #start_create_3d_obj(headers=headers, photoscene_id=photoscene_id)
    #progress_status(headers=headers, photoscene_id=photoscene_id)


    access_token = get_access_token()
    headers = create_auth_header(access_token=access_token)

    # obj_link = get_obj_link(headers=headers, photoscene_id=photoscene_id)
    # zip_path = download_file(obj_link)

    create_window()

    upload_model_and_insert_to_db()




    global completed_window
    completed_window = tk.Tk()
    completed_window.title("Process finished")
    completed_window.geometry("400x150")
    completed_window.resizable(False, False)

    completed_window_label = tk.Label(completed_window, text="The process was successfully completed!\n Now you can see the model on the website", font=("Arial", 15))
    completed_window_label.pack(pady=10)

    completed_window.mainloop()



    #model_name = str(input("please provide model name without any special characters and spaces"))


    #echo3d_link = upload_model(zip_path, model_name=model_name)
    #insert_to_db(model_name,echo3d_link)


# {
#   "id": "87f1f429-2706-4f20-9ab3-f966e04a8b81",
#   "target": {
#     "id": "bfc786a6-e21f-4a83-90dd-aca9aed80c6c",
#     "type": "BRICK_TARGET",
#     "holograms": [
#       "eb7b9a73-190f-4523-a16c-2f42c3f0c6ba"
#     ]
#   },
#   "hologram": {
#     "filename": "simona.obj",
#     "storageID": "fab9c11f-afbc-449d-b432-03418614382b",
#     "id": "eb7b9a73-190f-4523-a16c-2f42c3f0c6ba",
#     "type": "MODEL_HOLOGRAM",
#     "targetID": "bfc786a6-e21f-4a83-90dd-aca9aed80c6c"
#   },
#   "sdks": [
#     false,
#     false,
#     false,
#     false,
#     false,
#     false,
#     false,
#     false,
#     false
#   ],
#   "additionalData": {
#     "createdAt": "1684174761490",
#     "fileSize": "590922",
#     "glbHologramStorageFilename": "simona.glb",
#     "glbHologramStorageID": "57f727e3-8e70-4c6a-99f4-6166b67972bc.glb",
#     "lastAccessed": "1684174761490",
#     "qrARjsMarkerStorageFilename": "marker_qr_arjs_orange-hall-7575.png",
#     "qrARjsMarkerStorageID": "c1f0311e-8998-4e25-bd9e-73239a76abbc.png",
#     "qrARjsStorageFilename": "qr_arjs_orange-hall-7575.png",
#     "qrARjsStorageID": "dc2bb1cf-25a5-467d-ad81-9c396fcfaf54.png",
#     "qrARjsTargetStorageFilename": "qr_arjs_orange-hall-7575.patt",
#     "qrARjsTargetStorageID": "0c71e96a-3da2-47f7-8c71-566eff40b81e",
#     "qrFaceARStorageFilename": "qr_facear_orange-hall-7575.png",
#     "qrFaceARStorageID": "b1e2e76a-be46-4009-a656-2b1b3a364a67.png",
#     "qrWebARStorageFilename": "qr_webar_orange-hall-7575.png",
#     "qrWebARStorageID": "d7ff49ea-1f5f-46c8-8a3e-1319544a6ec3.png",
#     "qrWebXRStorageFilename": "qr_webxr_orange-hall-7575.png",
#     "qrWebXRStorageID": "3d3735a4-a998-4ce4-b303-2b226d670599.png",
#     "shortURL": "https://go.echo3d.co/73rv",
#     "usdzHologramStorageFilename": "simona.usdz",
#     "usdzHologramStorageID": "8d12d25b-ef43-4da8-8563-009503e8b586.usdz",
#     "vuforiaHologramStorageFilename": "simona.h",
#     "vuforiaHologramStorageID": "a19a5dea-378d-44c6-873a-745c3d4fc872"
#   }

# parser = argparse.ArgumentParser(description='Run our photo to 3D model program')
# parser.add_argument('-f', '--force-train-model', action="store_true", help='Force the model train')
# parser.add_argument('-c', '--use-word-correction', action="store_true",
#                     help='Use word correction for input using word2vec algorithm')
# parser.add_argument('-m', '--mode', choices=['online', 'offline'], dest='mode',
#                     help='The mode the chatbot run [online/offline]', required=True)
#
# parser.add_argument('--offline_input_file', '-i', dest='input_file', type=str,
#                     default="bot_offline_input_example.csv")
# parser.add_argument('--offline_output_file', '-o', dest='output_file', type=str,
#                     default="bot_offline_output_example.csv")
#
# args = parser.parse_args()
# print('Script configuration:')
# print('\n'.join(f'{k}={v}' for k, v in vars(args).items()))
#
# if args.force_train_model:
#     create_model_and_data()
#
# try:
#     WORDS, CLASSES, INTENTS, MODELS = load_saved_data_and_model()
# except Exception:
#     create_model_and_data()
#     WORDS, CLASSES, INTENTS, MODELS = load_saved_data_and_model()
#
# if args.use_word_correction:
#     use_correction()
# if args.mode == "online":
#     online_mode()
# else:
#     if exists(args.input_file):
#         run_offline_chatbot(args.input_file, args.output_file)
#     else:
#         print(f"input file {args.input_file} doesn't exist please use flag --offline_input_file properly")
