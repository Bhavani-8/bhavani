import os, zipfile
from datetime import datetime

def zip_folder(folder_path, zip_name):
    """
    Zips the given folder into a zip file.
    :param folder_path: Folder to zip
    :param zip_name: Output zip file name
    """
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                
                # Keep folder structure inside zip
                arcname = os.path.relpath(file_path, folder_path)
                
                zipf.write(file_path, arcname)

    print(f"✅ Zip file created successfully: {zip_name}")


if __name__ == "__main__":
    folder_to_zip = "reports/allure-report"        # Folder name
    today_date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")  # Timestamp for uniqueness
    output_zip = f"allure-report_{today_date}.zip"       # Zip file name

    if os.path.exists(folder_to_zip):
        zip_folder(folder_to_zip, output_zip)
    else:
        print("❌ Folder not found!")