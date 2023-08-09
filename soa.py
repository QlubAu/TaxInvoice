import pandas as pd
import pdfkit
import PyPDF2
import numpy as np
import os


def delete_files(directory):
    for filename in os.listdir(directory):
        # Check if the first 4 letters of the filename are 'temp'
        if filename[:4].lower() == 'temp':
            # Construct the full file path
            file_path = os.path.join(directory, filename)
            # Delete the file
            os.remove(file_path)
            print(f'Deleted: {file_path}')
        else:
            print(f'Skipped: {filename}')

    print("Process completed.")