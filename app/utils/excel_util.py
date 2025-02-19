# %% [markdown]
# # Excel Helper
# Aqui nem vou me esforçar,
# pq não sei a extrutura do seu arquivo, sabe ?
#
# %%
import pandas as pd
import os


def upload_to_excel(file_name: str, data: dict, sheet_name: str = "Sheet1"):
    file_name = f"static/excel_files/{file_name}"
    
    os.makedirs("static/excel_files", exist_ok=True)
    
    with pd.ExcelFile(file_name) as xls:
        existing_df = pd.read_excel(xls, sheet_name=sheet_name)
            
    new_data_df = pd.DataFrame(data)

    updated_df = pd.concat([existing_df, new_data_df], ignore_index=True)

    with pd.ExcelWriter(file_name, engine="openpyxl", mode="w") as writer:
        updated_df.to_excel(writer, sheet_name=sheet_name, index=False)


def read_from_excel(file_path):
    """Caso precise seila..."""
    file_path = f"static/excel_files/{file_path}"

    excel_data = pd.read_excel(file_path, sheet_name=None)

    data = {sheet: df.to_dict(orient="list") for sheet, df in excel_data.items()}

    return data
