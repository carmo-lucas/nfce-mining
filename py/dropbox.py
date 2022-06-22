import pathlib
import pandas as pd
import dropbox
from dropbox.exceptions import AuthError


# https://practicaldatascience.co.uk/data-science/how-to-use-the-dropbox-api-with-python

DROPBOX_ACCESS_TOKEN = "sl.BI0GD7r-NuF_fWem-9NuKOgPG6l0xi2hQ-nuvcI5Auz3sgFI8_qKJ1lgB1jt6ruLtMsOKeBdJRUtuy3BnjQYRliFHE2-0UoMgSNLrEK4neq0eRfxg254wEkQPFBuDgrbyA121vMfIgJ5"

def dropbox_connect():
    # Create a connection to Dropbox.

    try:
        dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)
    except AuthError as e:
        print('Error connecting to Dropbox with access token: ' + str(e))
    return dbx


def dropbox_download_file(dropbox_file_path, local_file_path):
    """Download a file from Dropbox to the local machine."""

    try:
        dbx = dropbox_connect()

        with open(local_file_path, 'wb') as f:
            metadata, result = dbx.files_download(path=dropbox_file_path)
            f.write(result.content)
    except Exception as e:
        print('Error downloading file from Dropbox: ' + str(e))


