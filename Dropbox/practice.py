import tkinter as tk
from tkinter import messagebox, filedialog
import dropbox
from dropbox.exceptions import ApiError
def Auth_dropBox():
    access_tk="sl.u.AGD5WbNombuiaxj3Z8XJz7F_VGPpKi2d6myS_UNCEJmuJrSoxotOAW1NYBpsWMdbrOl6anvcd48lkIapDLNnI65oD4ZOy1oFiM0yxkWNaePe_I3xocVANk7ZP3flurS3gF2dtolnVIODR1k5lzA4my9hPOmNNx75MsePyiG2XA4ud_YGfW4LwlbwVyjcrHr5kK6WilvQNKroJAFksy-9R39LvyYC5K24aaBlievWY2-ecoxzMq06rWohLZ0mjaXJ1elSeL-NgAlKtiWCSxt3W_6pmeGCvBHZIEA7O6QIr782IUEW0x-bk4Lh71bjngDvdVyfzUq7I-4ih1TLA0gY2XXQryXBwn2UkTZCOqrwOzZzHGSTR3bXKuPv3DRiMuz0QE-TUVyef-ZC6v9_OyqLL8T5I6KkYZTyS86SWWNbHwfPXhmN2h-iU6tjU95izgdlka4mINjp2pW9YzhMyKsjuceWlZJCWDol0_0JuiNwodskb9jdPfrNFtJ-t-PH0stXFdc25DT0bCJiyq1UJe_z5uMz0FA-I8PzReL_pp0MtatA503eiA3xsZjSrbZH-_gTiBFMifWxKUbeMTCLPXGoatpjnTNn-HhBl0-Ix60FdKH36RiopAOCWGpfFm73_zoczER48cN3HRxxlhLThGDcAdN0Zkqg78F2uFSv-8rgawqmaqKNAiadrYWTK8H34cZhD-5r93Dcv7Fz6pitiRT-6fetRwDmQnjjW8VJdARqsV27OP_yzUxk9ABVbniV_lkW6G6XoJwPaVyiVBMlQCSTqSgcaKnohjVcK-4-Gw7PA6axp6kWXcdk-c0RoNBGivaDaBzrKEeLpM1LePCwuUmz5sODw8gLqV49A_i7z_3BrUvKxG15hN93ZpvFkEOjj7dk5QJcDzXSsV4ZfIZqgr6D9H65O853sDI9Witz9NEHS0Uh7YuElgZoi6XNTvwj8ZHWt-t7GmPio-u7CV-Sk_OAbwBEJLeLQ_cCeqDRkLRz5Xw8UYVvjnakDook1hzuzbCSD2MYEV_AvHbmx5LzFAbttE5NXKtnTLhKGUCDrY9f_1wLaAcBj9uLsjug0dvbUBjBDdbOTV1_JRXcqYBsEq8EWVJxeL8eGBt8VN0fgioBrFrlKf2UQu4qz15INocHwPKwKqzHp984q4sD_RQM7MGocBSYNV6jgxWm2qe6c4LI0LdjY8SI8CPu05ciRRVv3-7l8vGd7TFmGA8uEnoP24Cfq97y4vkNdbp_cgrVdLW1Kgftp5s_G000umP8A3rUtKgtbEKSCE5Sevr01mXGYQtxoiThvlAH6S9MbbdicHXRN-oGRWcAF4MAFM7J3__MiFabTYLrCmkY-qe9eoLVyp70gOFdWg9_KqNcqJ4dsYXrFLhHrpCwSQeV5QMZ8xBNDmQDk-lkTdg8mkz2iiS9gVFPgA052bh3ASuDVoWf0ilAOt2HL2L8MLYHTKkNT1dNCKPnGkk"
    try:
        dbx=dropbox.Dropbox(access_tk)    
        if dbx:
            return dbx
    except Exception as e:
        print("Auth failed")
        messagebox.showerror("Auth failed",f"Auth failed {e}")
        return None
def upload_file():
    filePath=filedialog.askopenfilename()
    if filePath:
        try:
            dbx=Auth_dropBox()
            if dbx:
                filename=filePath.split("/")[-1]
                with open(filePath,"rb") as f:
                    dbx.files_upload(f.read(),f"/{filename}",mode=dropbox.files.WriteMode.overwrite)
                    messagebox.showinfo("File uploaded successfully","File uploaded successfully")
        except Exception as e:
            print("Error: ",e)
            messagebox.showerror("Error!",e)
def list_files():
    try:
        dbx=Auth_dropBox();
        if dbx:
            files=dbx.files_list_folder("").entries
            filenames=[f.name for f in files]
            file_list_box.delete(0,tk.END)
            for i in filenames:
                file_list_box.insert(tk.END,i)
            print("Files fetched successfully")
            messagebox.showinfo("Files fetched successfully")
    except Exception as e:
        print("Error",e)
        messagebox.showinfo(e)
def create_gui():
    root=tk.Tk()
    root.title("DropBox demo")
    upload=tk.Button(root,text="Upload file",command=upload_file)
    upload.pack(pady=10)
    listBtn=tk.Button(root,text="List files",command=list_files)
    listBtn.pack(pady=10)
    global file_list_box
    file_list_box=tk.Listbox(root,width=50,height=10)
    file_list_box.pack(pady=10)
    root.mainloop()
if __name__=="__main__":
    create_gui()
            
        
    
