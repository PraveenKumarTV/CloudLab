import tkinter as tk
from tkinter import filedialog, messagebox
import dropbox
from dropbox.exceptions import ApiError

# Function to authenticate with Dropbox using an access token
def authenticate_dropbox():
    # Replace this with your access token
    ACCESS_TOKEN = 'sl.u.AGD5WbNombuiaxj3Z8XJz7F_VGPpKi2d6myS_UNCEJmuJrSoxotOAW1NYBpsWMdbrOl6anvcd48lkIapDLNnI65oD4ZOy1oFiM0yxkWNaePe_I3xocVANk7ZP3flurS3gF2dtolnVIODR1k5lzA4my9hPOmNNx75MsePyiG2XA4ud_YGfW4LwlbwVyjcrHr5kK6WilvQNKroJAFksy-9R39LvyYC5K24aaBlievWY2-ecoxzMq06rWohLZ0mjaXJ1elSeL-NgAlKtiWCSxt3W_6pmeGCvBHZIEA7O6QIr782IUEW0x-bk4Lh71bjngDvdVyfzUq7I-4ih1TLA0gY2XXQryXBwn2UkTZCOqrwOzZzHGSTR3bXKuPv3DRiMuz0QE-TUVyef-ZC6v9_OyqLL8T5I6KkYZTyS86SWWNbHwfPXhmN2h-iU6tjU95izgdlka4mINjp2pW9YzhMyKsjuceWlZJCWDol0_0JuiNwodskb9jdPfrNFtJ-t-PH0stXFdc25DT0bCJiyq1UJe_z5uMz0FA-I8PzReL_pp0MtatA503eiA3xsZjSrbZH-_gTiBFMifWxKUbeMTCLPXGoatpjnTNn-HhBl0-Ix60FdKH36RiopAOCWGpfFm73_zoczER48cN3HRxxlhLThGDcAdN0Zkqg78F2uFSv-8rgawqmaqKNAiadrYWTK8H34cZhD-5r93Dcv7Fz6pitiRT-6fetRwDmQnjjW8VJdARqsV27OP_yzUxk9ABVbniV_lkW6G6XoJwPaVyiVBMlQCSTqSgcaKnohjVcK-4-Gw7PA6axp6kWXcdk-c0RoNBGivaDaBzrKEeLpM1LePCwuUmz5sODw8gLqV49A_i7z_3BrUvKxG15hN93ZpvFkEOjj7dk5QJcDzXSsV4ZfIZqgr6D9H65O853sDI9Witz9NEHS0Uh7YuElgZoi6XNTvwj8ZHWt-t7GmPio-u7CV-Sk_OAbwBEJLeLQ_cCeqDRkLRz5Xw8UYVvjnakDook1hzuzbCSD2MYEV_AvHbmx5LzFAbttE5NXKtnTLhKGUCDrY9f_1wLaAcBj9uLsjug0dvbUBjBDdbOTV1_JRXcqYBsEq8EWVJxeL8eGBt8VN0fgioBrFrlKf2UQu4qz15INocHwPKwKqzHp984q4sD_RQM7MGocBSYNV6jgxWm2qe6c4LI0LdjY8SI8CPu05ciRRVv3-7l8vGd7TFmGA8uEnoP24Cfq97y4vkNdbp_cgrVdLW1Kgftp5s_G000umP8A3rUtKgtbEKSCE5Sevr01mXGYQtxoiThvlAH6S9MbbdicHXRN-oGRWcAF4MAFM7J3__MiFabTYLrCmkY-qe9eoLVyp70gOFdWg9_KqNcqJ4dsYXrFLhHrpCwSQeV5QMZ8xBNDmQDk-lkTdg8mkz2iiS9gVFPgA052bh3ASuDVoWf0ilAOt2HL2L8MLYHTKkNT1dNCKPnGkk'
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
