from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os

gauth = GoogleAuth()
drive = GoogleDrive(gauth)

# Constants
# path = r"C:\Users\10126516\Desktop\Çalışmalar\Selenium_Kodları"   
folder_id = "1-GmnyZG9sFfOJsHETINJRO6INKoWvuuY"

# Query for files in the specified folder with the given MIME types (CSV and TXT)
query = "trashed=false and '{folder_id}' in parents and (mimeType='text/csv' or mimeType='text/plain')"


def upload_to_drive(Dosya):
    upload_file_name = Dosya
    # Drivedan ilgili klasördeki dosyaları alır.
    # Eğer Hisseler.csv dosyası varsa dosya değişkene atanır.
    file_list = drive.ListFile({'q': query.format(folder_id=folder_id)}).GetList()
    uploaded_file = None
    print(file_list)
    for file in file_list:
        print(file["title"])
        if(file["title"] == upload_file_name):
            uploaded_file = file
            
    # Eğer upload edilmiş bir dosya varsa o güncellenir.
    # Yoksa yeni dosya oluşturulup upload edilir.
    if uploaded_file:
        gfile = uploaded_file
    else:
        gfile = drive.CreateFile({'parents': [{'id': folder_id}], 'title': upload_file_name})
    
    # Set file content and upload
    gfile.SetContentFile(os.path.join( upload_file_name))
    gfile.Upload()
