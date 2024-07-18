import os
import shutil
from config import SCRIPT_ROOT

mermaid_directory = os.path.join(SCRIPT_ROOT, 'Mermaid_Files')


def create_mermaid_folder(mermaid_unique_id):
    mermaid_folder_path = os.path.join(mermaid_directory, mermaid_unique_id)

    os.makedirs(mermaid_folder_path)

    with open(os.path.join(mermaid_folder_path, 'codefile.txt'), 'w') as _: pass
    with open(os.path.join(mermaid_folder_path, 'mermaid_code.txt'), 'w') as _: pass
    
    return mermaid_folder_path

def delete_mermaid_folder(mermaid_unique_id):
    mermaid_folder_path = os.path.join(mermaid_directory, mermaid_unique_id)

    if os.path.exists(mermaid_folder_path):
        shutil.rmtree(mermaid_folder_path)

def save_mermaid_code(mermaid_unique_id, text_contents):
    mermaid_folder_path = os.path.join(mermaid_directory, mermaid_unique_id)
    mermaid_codefile_path = os.path.join(mermaid_folder_path, 'mermaid_code.txt')

    with open(mermaid_codefile_path, 'w') as file_handle:
        file_handle.writelines(text_contents)


