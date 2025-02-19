# %% [markdown]
# # SharePoint Utils
# Outra merda que eu não
# tenho então nem sei se vai rodar.
#
# Aqui ele so da upload do arquivo pronto na pasta.
#
# Relaxa que ta cheio de bugs, testei foi é nada.
#
# Boa sorte ai
# %%
from shareplum import Site
from shareplum import Office365
import os

user_name = os.getenv("SHAREPOINT_USER")
password = os.getenv("SHAREPOINT_PASS")
sharepoint_url = os.getenv("SHAREPOINT_URL")
site_url = os.getenv("SITE_URL")
folder_path = "Shared Documents/YourFolder"


def load_client():
    """Como não tenho a API"""
    if user_name and password:
        authcookie = Office365(
            sharepoint_url, username=user_name, password=password
        ).GetCookies()
        site = Site(sharepoint_url + site_url, authcookie=authcookie)
        folder = site.Folder(folder_path)

        return folder


def download_file(file_path: str, download_path: str = None):
    """Estou tentando deixar tudo baixado por baixo de static/excel_files
    file_path é na maquina la do shared point
    download_path é pra sua maquina."""
    if not download_path:
        os.makedirs("static/excel_files", exist_ok=True)
        download_path = os.path.join(os.getcwd(), "static/excel_files", file_path)
    
    os.makedirs(os.path.dirname(download_path), exist_ok=True)

    folder = load_client()
    file_data = folder.get_file(file_path)

    with open(download_path, "wb") as f:
        f.write(file_data)


def upload_file(file_name: str):
    """Aqui file name é o nome do arquivo 
    mesmo que estamos baixando, definimos 
    o folder que vamos dar upload la em cima 
    em folder_path"""
    folder = load_client()

    with open(file_name, "rb") as file:
        file_data = file.read()

    folder.upload_file(file_data, os.path.basename(file_name))
