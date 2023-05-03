import os
import qrcode
import requests

api_key = "floral-sound-8712"
sec_key = "mhU3RT4l521SlAHq4XkGTvni"
model_id = "595dd625-64e1-4b87-9847-dadd1a1f18bf"

url = f"https://api.echo3d.com/query?key={api_key}&secKey={sec_key}"

response = requests.get(url)
data = response.json()

short_url = data["db"][model_id]["additionalData"]["shortURL"]

filename = f"qrcode_{model_id}.png"
folder = os.path.abspath("img-QRcode")

if not os.path.exists(folder):
    os.makedirs(folder)

filepath = os.path.join(folder, filename)

qr = qrcode.QRCode(version=1, box_size=10, border=5)
qr.add_data(short_url)
qr.make(fit=True)
img = qr.make_image(fill_color="black", back_color="white")
img.save(filepath)

print(f"QR code saved as {filepath}")
