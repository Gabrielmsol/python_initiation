# %% [markdown]
# # Init File
# Aqui voce monta a o seu app, 
# isso mantem o processo mais organizado 
# %%
from app.utils.email_utils import process_email # -> list[dict]
from app.utils.openai_utils import analyze_with_ai # -> dict
from app.utils.sharepoint_utils import upload_file, download_file
from app.utils.excel_util import upload_to_excel
from time import sleep

delay = 10 # Em segundos
file_name = "some_file.xlsx" # Arquivo do excel que vai analizar
def init_app():
    while True:
        sleep(delay)
        download_file(file_path=file_name) # Poe qual arquivo vai dar upload depois
        emails = process_email()
        data = {}
        if emails:
            for email_id, email in emails:
                analysis = analyze_with_ai(email)
                data[email_id] = analysis
                # TODO: Faz uma função para organizar esses arquivos
                
            upload_to_excel(file_name=file_name, data=data)
            upload_file(file_name=file_name)
                
        
     