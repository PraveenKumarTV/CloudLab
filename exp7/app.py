import tkinter as tk
from tkinter import filedialog, messagebox
import dropbox
from dropbox.exceptions import ApiError

# Function to authenticate with Dropbox using an access token
def authenticate_dropbox():
    # Replace this with your access token
    ACCESS_TOKEN = 'sl.u.AF-2YcfB0dpDi43-TFO5bPRua62UgO4Zoy_AEH1ayBJw5UctsI1-xqBYhgdefpPVmkJ4bsD153q95EmxTFF5b7B2Mq6f8VG3X2Al1eycr5PdNiEmb4yUAF1W-ixZ37hMj6dF_SESRrq61dkJ2Pk-LhYqU6QogHGGwQrWCskG9T11-HDPvXpT3aBGajebNq1l1RbtvF09xHjKkJfbYJ8Do24y20_VViyxQCsiwUpPv8RF5Fdhgm8LwjuOZemTaaG0rHH0Ve220SO5UWR0Ak6zMHURRw1xjMy_Sr_APo-2IBUIoufmds0M-B6bdjsCPjBf03gqdywpZSCbM3A-Li63ENzAeF7L2ee8DXcZKg01eic6qxZgXdHFNCSWa6ecH2_FWC0bZ7KFkJC5e8_zpWQQf9JKgVhMe9WyYr0x9RbP3txrywoyXVlyJv336nMCguZVPf1WGO9kSybjTFKB9HQ3bswif0lJrJM-FZ1W2V5nOTzKLXRL6KBC53PgDEGoMU0Jplw48g1q0tqbgeG8omQMwAN3L8fgHVupYAr0xmSJOVskJpVPnNVCEvXm39xP4zltPez_kL_YBPeEHAPzJFF-xrhvmds8vSw-G6_4erLf15LV1_EGdtNdxlEhRSpMKMkN8TUhVwPpWVDf_1R_Iil-FYlzE533J6MriFUQZtq9vCYP4wK9M40AgsvM20uBmcZqIBE3SqCjrgBCwZJPS673VqiPErpErHgS60Ufp3XkEg5OacDhI5N0Wp5AuU5-Dgw6fWjzDmAX_q2-Hq77Cq0g4rMSPgkK4Tz9AlS94IpiDfM8uXO7wCdGn18B6SlI-Ph0lgdFURuzEGKVcx68mIeCs0aV3UK1CLjoEfvD4aYL-2yG40BHHTSj7Zt9ndq_HCHbySeIauvtT0-Q1KwE_YJZzpSqvK3W_gOxR0yMUZcmzzIJ8tnaRl1n1qb_1UpdDQKjgA1_KxOkqaO4aE5tRFMf3kjA-_3IlWmoQdn6VE9jfgUjxBqAxcOw7ZGm-2wSNXsy3mv0PaHRsCw3V--Vo_IBICxOIzK0zvn7C_RdXiKs_B9cgc4tNcbK7J2HMs60RhOcMGC5FwNgbcf2In6ulc1exjcwO5b5w5ouuXFolEsH0vV8aZZFeLdADET1Lq7kMYbCuHUozHrslAo_13Qwop9aeoSL-e09wvgXoop8sMc5N9emQxx-bTOdq1JeK0TbO4DEJjIojx-JZCMQRg299_uvD9P0w0Tdj-n0qVs_WzXpyNDT2-0Nxt7wMY_WyYf_v0zGiJNH7pYqEskiTzjZ5d1iqQ08Q8nfiHm_1k-MQiZx7Z2FfeN5g4-u4KXaJL3QfaOmFiDbpCZbDBpJp9Gsok0w1y5KBVsnydy72AsfqpamV3LLr0u1UK8ovfitZ823pYhNAXChmKvN-QW4FSgo6D_iyiYpGGIdWpkaSckeCOkYCn_TL_JfhizCBIMRUfWYRtzI1Tc'
    try:
        dbx = dropbox.Dropbox(ACCESS_TOKEN)
        return dbx
    except Exception as e:
        print(f"Authentication Failed: {e}")
        messagebox.showerror("Authentication Failed", f"Failed to authenticate with Dropbox: {e}")
        return None

# Function to upload a file to Dropbox
def upload_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        try:
            dbx = authenticate_dropbox()
            if dbx:
                with open(file_path, "rb") as f:
                    file_name = file_path.split("/")[-1]
                    dbx.files_upload(f.read(), f"/{file_name}", mode=dropbox.files.WriteMode.overwrite)
                    messagebox.showinfo("Success", f"File '{file_name}' uploaded successfully!")
        except Exception as e:
            print(f"Upload Failed: {e}")
            messagebox.showerror("Upload Failed", f"Failed to upload the file: {e}")

# Function to list all files in Dropbox
def list_files():
    try:
        dbx = authenticate_dropbox()
        if dbx:
            files = dbx.files_list_folder('').entries
            file_names = [f.name for f in files]
            file_list_box.delete(0, tk.END)
            for file_name in file_names:
                file_list_box.insert(tk.END, file_name)
    except Exception as e:
        print(f"List Files Failed: {e}")
        messagebox.showerror("List Files Failed", f"Failed to list files: {e}")

# Function to download a file from Dropbox
def download_file():
    selected_file = file_list_box.curselection()
    if selected_file:
        file_name = file_list_box.get(selected_file)
        try:
            dbx = authenticate_dropbox()
            if dbx:
                metadata, res = dbx.files_download(path=f'/{file_name}')
                with open(file_name, 'wb') as f:
                    f.write(res.content)
                messagebox.showinfo("Success", f"File '{file_name}' downloaded successfully!")
        except Exception as e:
            print(f"Download Failed: {e}")
            messagebox.showerror("Download Failed", f"Failed to download the file: {e}")

# GUI setup
def create_gui():
    root = tk.Tk()
    root.title("Dropbox File Manager")

    # Buttons
    upload_button = tk.Button(root, text="Upload File", command=upload_file)
    upload_button.pack(pady=10)

    list_button = tk.Button(root, text="List Files", command=list_files)
    list_button.pack(pady=10)

    download_button = tk.Button(root, text="Download File", command=download_file)
    download_button.pack(pady=10)

    # Listbox for displaying files in Dropbox
    global file_list_box
    file_list_box = tk.Listbox(root, width=50, height=10)
    file_list_box.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
