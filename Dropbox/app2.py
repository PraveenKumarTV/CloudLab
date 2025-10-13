import dropbox
import streamlit as st
from dropbox.exceptions import ApiError
def auth():
    try:
        tok="sl.u.AGCesHBD369PWyZlj3Kr4MC2hHKhYfB3MdTdWR6gKixRhscGoVlsEvQj9bbMajQWnIBdIDJdtLEnmni_J-zLyt4VazexZIbZC99FpQ1Ea3Lq6nnjogTQ2G6yzc5qewsoP0tW6HH8aKT0KzNbe3vCOOfCxBR4eZemY5_hHTV5UU8-RHmUVb5M0QbHcLKA3Qja5wv4G0C1DZLlfLSwR9U9A_Ztq12bN9hIBAkiVV1x_FlEWFTAGnefseoI2j81-Fygr3vLdvJgZOkvPyXH4C64IMW3CMTN3gvsWFvrgBb-_kp-_vruURVaqLkZI_mzX908_tunJcmwrfe2EAryW482dZS8DYKn7q56OMn5byLaOCWroXeU-GM7kinIXJNvq7wNvd3pPX0nSzUby7fqH7KZdSkvigXppKXz3T7qGyqIWdjX1uYpNwELMnuIl9vEAp3vlMYWEpcTrfj3rA9ONReICAPUk0tF6OJpuGs4YvubH5bcD8Y8w-a97T-uT375VlYGpnWW_hxns2Lb8pJVXehsmis9C9i4Cf43knLzqYYsLnu4y0fm5EiCAUAMRi63XoVEv3Pw9GCrRnv3EbHoufHM9i-xHN1v84IBjj6LyoB2qin18M0zkwizi-EXx2Rn77FVbAZ3YNLkM99EH02MLeeqIyzFNouHViZDaas3yTj6Hj5Yz2-MT01iycd1zSmH6FO57E4BL24596sv4IT3DgPQVO2K1ZNrHLNBcTomF_9aMAEy1xNF_MOP1j8fujP_IaVJwe7ww7EpOCn-ySYv8oNkmrVAEUK5epzEbPGBbwaj1e1qXIcw_8xH_vnvBLoQDOkIbug3_vbvsTCF6c89n7F2e_qMabYbFJtP-LBBii5rfwCVSwTWlSRJ0YkP69X0nGmyyvu4MTsfMiQFLQTClibwIcKJS-i7_EUkzvhj8zksgG8q_b3eQJgjkm5SaRgRNQYgNwX-4D5rsDOgQtE5R466bQ2nXCfcufKtPlcw6iesZwZMTIQc8VYqgM04Zue33yfD3Tn74Ai7bFqLiQH5wP8jVC260xlAgANzUpc9H2DH3cxDaBa5nnUuOQ1f6d8KEVWU-ceruudeeJtkYLj23--uNrc0cncCk5uOJaEN3zqMADlGf7V60FeL3ymRuSl6zi0roGQMKRC9-aU8kpV7F39dBDgUKXEJkEXqvEGoUHLIkOf010AcCWZ8f9p3dFZdBXEicLrDyb5_LuwOyZtmixrz5easf0BkmTp17KlO75kSaLHSvo45JmCM5n-DxlGTiNahyiRAgaVqAvDP_5K4V2-pyJgpR7xDkuL89CGpRlavNg6jF_jTk_xvVM1P0O0eIhZnlVYIMi7SiymVXQSvER9CdpAyxcS4g1c2W19G0T-ojKdNZvqaT7emeMoAoTfTNtBTBhXtrPS4T34__9IoXAkXOJnGjiaZvbvLeiOJfb9Qz1Pr59YMPLeWO1ZzFx_eSouS2LQ"
        dbx=dropbox.Dropbox(tok)
        return dbx
    except Exception as e:
        st.error("Auth failed")
        return None
def upload(file):
    try:
        dbx=auth()
        if dbx:
            dbx.files_upload(file.read(),f"/{file.name}",mode=dropbox.files.WriteMode.overwrite)
            st.success("file uploaded successfully")
    except ApiError as e:
        st.error("Error in uploading")
def list():
    try:
        dbx=auth()
        if(dbx):
            files=dbx.files_list_folder("")
            fileData=[f.name for f in files.entries]
            return fileData
    except Exception as e:
        st.error("Error in listing")
        return []
def download(filename):
    dbx=auth()
    if(dbx):
        try:
            metadata,res=dbx.files_download(f"/{filename}")
            st.download_button(
                label=f"download {filename}",
                data=res.content,
                file_name=filename
            )
        except Exception as e:
            st.error("Download failed")
st.title("Dropbox file manager")
st.header("File uploader")
uploaded_file=st.file_uploader("Choose a file to upload")
if uploaded_file is not None:
    if st.button('upload'):
        upload(uploaded_file)
st.header("List files")
if(st.button("Referesh files")):
    st.session_state.file_list=list()
fileList=st.session_state.get("file_list",[])
if fileList:
    selectedFile=st.selectbox("Select files to download",fileList)
    if st.button("Download"):
        download(selectedFile)
else:
    st.write("No files found")


