import requests
import pandas as pd
import datetime as dt_
from io import StringIO
from datetime import datetime, timedelta
import streamlit as st
import re
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import PyPDF2
import pdfkit
from io import BytesIO
from googleapiclient.http import MediaIoBaseUpload
import os.path
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from tempfile import NamedTemporaryFile
import streamlit_authenticator as stauth

from io import BytesIO
import pdfkit
import PyPDF2




html_template = """ 

<!DOCTYPE html>
<html>
    <head>
        <style>
            .rectangle {
                background-color: #7b08ce;
                height: 50px;
                width: 100%;
            }
            table {
                width: 100%;
                text-align: left;
                border-collapse: collapse;
            }
            th, td {
                border-bottom: 1px solid #ccc;
                padding: 8px;
            }
            .address-block {
                width: 500px; 
                text-align: left;
                margin-bottom: 20px;
            }
            .address-block p {
                margin: 0;
                padding: 0;
            }

        </style>
    </head>
    <body>
        <div class="rectangle"> </div>
        <h1>Tax Invoice</h1>
        <p>Statement Period: 01/06/2023 to 30/06/2023</p>
        <div class="address-block">
            <p><strong>From:</strong> FAST TECHNOLOGY GROUP AUSTRALIA PTY LTD</p>
            <p>320, Pitt St,</p>
            <p>Sydney, NSW 2000</p>
            <p>ABN: 18 655 352 686</p>
        </div>
        <div class="address-block">
            <p><strong>To:</strong> ${restaurant}</p>
            <p>${address_resto}</p>
            <p>ABN: ${abn_no}</p>
        </div>
        <table>
            <tr>
                <th>Item</th>
                <th>Amount</th>
            </tr>
            <tr>
                <td>Total Amount Processed through Qlub</td>
                <td>$${paid_amount}</td>
            </tr>
            <tr>
                <td>Processing Fees (Excludes GST)</td>
                <td>-$${commission_amount_ex_tax}</td>
            </tr>
            <tr>
                <td>GST</td>
                <td>-$${tax}</td>
            </tr>
            <tr>
                <td>Processing Fees (Includes GST)</td>
                <td>$${commission_amount_in_tax}</td>
            </tr>
            <tr>
                <td colspan="3" style="border-bottom: none;"></td>   <!-- Add this line -->
            </tr>
        </table>
        <p>This report is provided to enable you to support a GST credit, if applicable, for the GST incurred on your processing fees. The fee totals are inclusive of all Credit and Debit fees incurred through Visa, MasterCard, American Express, eftpos and JCB transactions. Fee rates may vary from the advertised percentage due to rounding and differences in pricing for transactions that are tapped, inserted, swiped or manually entered. The effective fee rates are calculated by dividing the Processing Fees Amount (including or excluding GST) by the Total Collected Amount. </p>
        <p> These fees have already been deducted from your settlements and are not outstanding. </p>
        <p>&copy; FAST TECHNOLOGY GROUP AUSTRALIA PTY LTD</p>
    </body>
</html>




    """
restaurant_ids = [3834, 3810, 3773, 3770, 3769, 3725, 3724, 3723, 3722, 3719, 3713, 3701, 3700, 3689, 3679, 3665, 3622, 3504, 3502, 3501, 3500, 3499, 3452, 3404, 3403, 3348, 3347, 3336, 3298, 3264, 3256, 3237, 3236, 3235, 3234, 3233, 3232, 3187, 3186, 3175, 3174, 3173, 3168, 3167, 3120, 3118, 3030, 3029, 3027, 2958, 2939, 2882, 2850, 2846, 2845, 2827, 2826, 2825, 2799, 2772, 2762, 2761, 2752, 2657, 2630, 2518, 2517, 2505, 2504, 2453, 2361, 2316, 2211, 2081, 1934, 1905, 1869, 1852, 1851, 1850, 1840, 1828, 1810, 1809, 1807, 1795, 1777, 1762, 1727, 1690, 1688, 1663, 1653, 1605, 1604, 1531, 1509, 1508, 1413, 1347, 1341, 1334, 1318, 1300, 1299, 1294, 1291, 1257, 1228, 1221, 1207, 1192, 1184, 1064, 1062, 1023, 971, 944, 934, 918, 913, 909, 893, 881, 876, 859, 826, 808, 790, 617, 601, 587, 586, 492, 437, 387, 273, 272, 271, 103]

def initialize_streamlit():
    """Initialize Streamlit interface by setting the title and instructions."""
    st.title("Revenue Report")
    st.write("Select a date to see the revenue generated")
def get_start_date():
    """Prompt user to select a date using Streamlit and return selected date with specific time combined."""
    # Select a date range
    start_date = st.date_input("Select a start date", dt_.date(2023, 6, 10))
    selected_time = datetime.strptime("03:00:00", "%H:%M:%S").time()

    return datetime.combine(start_date, selected_time)


def get_end_date():
    """Get end date which is one day ahead of the start date."""
    date_end = st.date_input("Select a end date",dt_.date(2023, 7, 10))
    selected_time = datetime.strptime("03:00:00", "%H:%M:%S").time()
    return datetime.combine(date_end, selected_time)

def convert_date_format(date_time, flag):
    """Convert date_time object to a specific string format."""
    return (
        date_time.strftime("%Y-%m-%dT%H:%M:%S.000Z")
        if flag == "start"
        else date_time.strftime("%Y-%m-%dT%H:%M:%S" ".999Z")
    )

@st.cache_data(ttl=12 * 3600)
def get_token() -> str:
    """Get token from vendor panel login"""

    token_url = "https://api-vendor.qlub.cloud/v1/auth/login"
    header = {"Accept": "application/json"}
    data = {
        "email": "Irfan.Karukappadath@qlub.io",
        "password": "Qlub123!!!",
        "type": "admin",
    }

    response = requests.post(token_url, headers=header, json=data)

    # Check status code
    if response.status_code != 201:
        print(f"Unexpected status code {response.status_code}: {response.text}")
        raise Exception(f"Failed to authenticate with status code {response.status_code}")

    # Print entire response
    #print("Response JSON:", response.json())
    #print(json.dumps(response.json(), indent=4))

    try:
        return f'Bearer {response.json()["data"]["cognitoUser"]["signInUserSession"]["idToken"]["jwtToken"]}'
    except KeyError as e:
        raise Exception(f"KeyError: {e}. Full response: {response.json()}") from e


def get_csv_from_api(start_date_time,end_date_time,resto_id):
    api_endpoint = f"https://api-vendor.qlub.cloud/v1/vendor/order/download/{resto_id}?fileFormat=csv&startDate={start_date_time}&endDate={end_date_time}"
    header = {
        "Accept": "application/json, text/plain, */*",
        "Authorization": get_token(),
    }
    response = requests.get(api_endpoint, headers=header)
    data = StringIO(response.text)
    return pd.read_csv(data, sep=",") if response.status_code == 200 else None

import pandas as pd
from googleapiclient.discovery import build
from google.oauth2 import service_account

def get_restaurant_details_l(restaurant_name, sheet_id):

  # Authenticate with service account credentials
  creds = service_account.Credentials.from_service_account_file(
      'client_secret_811309362652-buvv861nns47b9dsr0en9i2g5bjlhpsg.apps.googleusercontent.com.json',
      scopes=['https://www.googleapis.com/auth/spreadsheets.readonly'])

  service = build('sheets', 'v4', credentials=creds)

  # Call the Sheets API to get sheet data
  sheet = service.spreadsheets()
  result = sheet.values().get(spreadsheetId=sheet_id, range='Sheet2!A:Z').execute()
  values = result.get('values', [])

  # Convert to DataFrame
  df = pd.DataFrame(values[1:], columns=values[0])

  # Find restaurant row
  restaurant_row = df.loc[df['restaurant_unique'] == restaurant_name]

  # Get address and ABN
  address_resto = restaurant_row['address1'].values[0] if not restaurant_row.empty else ''
  abn_no = restaurant_row['config.abn'].values[0] if not restaurant_row.empty else ''

  return address_resto, abn_no
def get_restaurant_details(restaurant_name, sheet_id):
    # Define the scope
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

    # Load the credentials from the downloaded JSON file
    credentials = ServiceAccountCredentials.from_json_keyfile_name("soa-qlub-au-76bbf3db96b6.json", scope)

    # Authorize the client
    client = gspread.authorize(credentials)

    # Open the Google Sheet using its ID
    spreadsheet = client.open_by_key(sheet_id)


    worksheet = spreadsheet.get_worksheet(1)

    # Get all values in the form of a DataFrame
    data = worksheet.get_all_records()
    df = pd.DataFrame(data)

    # Find the row that matches the restaurant name
    restaurant_row = df.loc[df['restaurant_unique'] == restaurant_name]

    # Retrieve the address and ABN number, if the row is found
    address_resto = restaurant_row['address1'].values[0] if not restaurant_row.empty else ''
    abn_no = restaurant_row['config.abn'].values[0] if not restaurant_row.empty else ''

    return address_resto, abn_no


def process_csv(start_date_time,end_date_time,csv_df):
    commission_with_tax = 0
    refund_total = 0
    refund_bar = 0
    bill_3 = 0
    tips_total = 0
    bill_5 = 0
    total_bill = 0
    bill_4 = 0
    tax = 0
    commission_without_tax = 0
    resto_name = None

    for index, row in csv_df.iterrows():
        try:
            row_date = datetime.strptime(str(row["DateTime"]), "%m/%d/%Y %H:%M %p")
        except ValueError:
            continue
        start_date = datetime.strptime(start_date_time, "%Y-%m-%dT%H:%M:%S.000Z")
        end_date = datetime.strptime(end_date_time, "%Y-%m-%dT%H:%M:%S.999Z")

        if start_date <= row_date < end_date:
            commission_with_tax += float(row["CommissionIncludingVAT"])
            total_bill += float(row["CustomerPaid"])
            if resto_name is None:
                resto_name = row["RestaurantName"]

    commission_without_tax = commission_with_tax/1.1
    tax = commission_with_tax - commission_without_tax
    commission_without_tax = round(commission_without_tax, 2)
    commission_with_tax = round(commission_with_tax,2)
    tax = round(tax, 2)
    total_bill = round(total_bill, 2)
    total_bill = format(total_bill, ',')
    commission_without_tax = format(commission_without_tax, ',')
    commission_with_tax = format(commission_with_tax, ',')
    tax = format(tax, ',')

    return commission_with_tax, total_bill, tax, commission_without_tax, resto_name,




def generate_and_upload_invoice(html_template, total_amount, commission_amount_ex_tax, tax,commission_amount,restaurant, address_resto, abn_no, google_drive_folder_id,credentials_path):

    # Replace placeholders in HTML template
    html_content = html_template.replace('${paid_amount}', str(total_amount))
    html_content = html_content.replace('${commission_amount_ex_tax}', str(commission_amount_ex_tax))
    html_content = html_content.replace('${tax}', str(tax))
    html_content = html_content.replace('${commission_amount_in_tax}', str(commission_amount))
    html_content = html_content.replace('${restaurant}', str(restaurant))
    html_content = html_content.replace('${address_resto}', str(address_resto))
    html_content = html_content.replace('${abn_no}', str(abn_no))

    # Generate PDF from the HTML content
    pdf_filename_temp = f'temp_{restaurant}.pdf'
    pdfkit.from_string(html_content, pdf_filename_temp)
    pdf_filename = open(pdf_filename_temp, "rb")
    pdf_reader = PyPDF2.PdfReader(pdf_filename)

    temp_pdf_file = open("qlogo.pdf", "rb")
    temp_pdf_reader = PyPDF2.PdfReader(temp_pdf_file)

    # Create a PdfFileWriter object for the output PDF
    pdf_writer = PyPDF2.PdfWriter()
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        if page_num == 0:
            page.merge_page(temp_pdf_reader.pages[0])
        pdf_writer.add_page(page)

    # Save the output PDF
    output_pdf_path = f"{restaurant}_Tax Invoice from Qlub.pdf"
    with open(output_pdf_path, "wb") as out:
        pdf_writer.write(out)

    # Close the PDF files
    pdf_filename.close()
    temp_pdf_file.close()
    SCOPES = ['https://www.googleapis.com/auth/drive']
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path,SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    # Authenticate with Google Drive
    service = build('drive', 'v3', credentials=creds)

    # Upload the output PDF to Google Drive
    file_metadata = {'name': f'{restaurant}_Tax Invoice from Qlub.pdf', 'parents': [google_drive_folder_id]}
    media = MediaFileUpload(output_pdf_path, mimetype='application/pdf')
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print(file.get('id'))
    # Return the file ID


# Usage example:


from io import BytesIO
from googleapiclient.http import MediaIoBaseUpload

def generate_and_upload_invoice_dl(html_template, total_amount, commission_amount_ex_tax, tax, commission_amount, restaurant, address_resto, abn_no, google_drive_folder_id, credentials_path):
    # Replace placeholders in HTML template
    html_content = html_template.replace('${paid_amount}', str(total_amount))
    html_content = html_content.replace('${commission_amount_ex_tax}', str(commission_amount_ex_tax))
    html_content = html_content.replace('${tax}', str(tax))
    html_content = html_content.replace('${commission_amount_in_tax}', str(commission_amount))
    html_content = html_content.replace('${restaurant}', str(restaurant))
    html_content = html_content.replace('${address_resto}', str(address_resto))
    html_content = html_content.replace('${abn_no}', str(abn_no))

    # Generate PDF from the HTML content
    pdf_bytes_io = BytesIO()
    pdfkit.from_string(html_content, pdf_bytes_io)

    # Create a PdfFileReader object for the PDF content
    pdf_reader = PyPDF2.PdfReader(pdf_bytes_io)
    pdf_bytes_io.seek(0)  # Reset the cursor to the beginning of the file

    temp_pdf_file = open("/Users/irfank/PycharmProjects/invoice_work/qlogo.pdf", "rb")
    temp_pdf_reader = PyPDF2.PdfReader(temp_pdf_file)

    # Create a PdfFileWriter object for the output PDF
    pdf_writer = PyPDF2.PdfWriter()
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        if page_num == 0:
            page.merge_page(temp_pdf_reader.pages[0])
        pdf_writer.add_page(page)

    # Write the PDF to the BytesIO object
    pdf_bytes_io = BytesIO()
    pdf_writer.write(pdf_bytes_io)
    pdf_bytes_io.seek(0)  # Reset the cursor to the beginning of the file

    # Authenticate with Google Drive
    SCOPES = ['https://www.googleapis.com/auth/drive']
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('drive', 'v3', credentials=creds)

    # Upload the output PDF to Google Drive
    file_metadata = {'name': f'{restaurant}_Tax Invoice from Qlub.pdf', 'parents': [google_drive_folder_id]}
    media = MediaIoBaseUpload(pdf_bytes_io, mimetype='application/pdf')
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print(file.get('id'))

    # Close the temporary PDF file
    temp_pdf_file.close()



from tempfile import NamedTemporaryFile
from io import BytesIO
import os
import PyPDF2
import pdfkit
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

def generate_and_upload_invoice_l(html_template, total_amount, commission_amount_ex_tax, tax, commission_amount, restaurant, address_resto, abn_no, google_drive_folder_id, credentials_path,id):
    # Replace placeholders in HTML template
    html_content = html_template.replace('${paid_amount}', str(total_amount))
    html_content = html_content.replace('${commission_amount_ex_tax}', str(commission_amount_ex_tax))
    html_content = html_content.replace('${tax}', str(tax))
    html_content = html_content.replace('${commission_amount_in_tax}', str(commission_amount))
    html_content = html_content.replace('${restaurant}', str(restaurant))
    html_content = html_content.replace('${address_resto}', str(address_resto))
    html_content = html_content.replace('${abn_no}', str(abn_no))

    # Generate PDF from the HTML content
    with NamedTemporaryFile(suffix=".pdf", delete=False) as temp_pdf_file:
        pdfkit.from_string(html_content, temp_pdf_file.name)

        # Create a PdfFileReader object for the PDF content
        pdf_reader = PyPDF2.PdfReader(temp_pdf_file.name)

        temp_logo_pdf_file = open("qlogo.pdf", "rb")
        temp_logo_pdf_reader = PyPDF2.PdfReader(temp_logo_pdf_file)

        # Create a PdfFileWriter object for the output PDF
        pdf_writer = PyPDF2.PdfWriter()
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            if page_num == 0:
                page.merge_page(temp_logo_pdf_reader.pages[0])
            pdf_writer.add_page(page)

        # Write the PDF to the BytesIO object
        """
        pdf_bytes_io = BytesIO()
        pdf_writer.write(pdf_bytes_io)
        pdf_bytes_io.seek(0)  # Reset the cursor to the beginning of the file
        """
        with NamedTemporaryFile(suffix=".pdf", delete=False) as output_pdf_file:
            pdf_writer.write(output_pdf_file)
            output_pdf_path = output_pdf_file.name
        # Authenticate with Google Drive
        # Authenticate with Google Drive
        temp_logo_pdf_file.close()
    SCOPES = ['https://www.googleapis.com/auth/drive']
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('drive', 'v3', credentials=creds)
        # Upload the output PDF to Google Drive
    file_metadata = {'name': f'{id}_{restaurant}_Tax Invoice from Qlub.pdf', 'parents': [google_drive_folder_id]}
    media = MediaFileUpload(output_pdf_path, mimetype='application/pdf')
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()

    # Close the temporary PDF files
    os.unlink(temp_pdf_file.name)
    os.unlink(output_pdf_path)


# Usage example:
# generate_and_upload_invoice(html_template, total_amount, commission_amount_ex_tax, tax, commission_amount, restaurant, address_resto, abn_no, google_drive_folder_id, credentials_path)



def generate_and_upload_invoice_to_supabase(html_template, total_amount, commission_amount_ex_tax, tax,
                                            commission_amount, restaurant, address_resto, abn_no, bucket_name,
                                            supabase_url, supabase_api_key, logo_path):
    # Replace placeholders in HTML template
    html_content = html_template.replace('${paid_amount}', str(total_amount))
    html_content = html_content.replace('${commission_amount_ex_tax}', str(commission_amount_ex_tax))
    html_content = html_content.replace('${tax}', str(tax))
    html_content = html_content.replace('${commission_amount_in_tax}', str(commission_amount))
    html_content = html_content.replace('${restaurant}', str(restaurant))
    html_content = html_content.replace('${address_resto}', str(address_resto))
    html_content = html_content.replace('${abn_no}', str(abn_no))

    # Create a BytesIO object to hold the PDF
    pdf_bytes_io = BytesIO()

    # Generate PDF from HTML and write to the BytesIO object
    pdfkit.from_string(html_content, pdf_bytes_io)

    # Create a PdfReader object for the PDF content
    pdf_reader = PyPDF2.PdfReader(pdf_bytes_io)

    # Add logo
    with open(logo_path, "rb") as temp_logo_pdf_file:
        temp_logo_pdf_reader = PyPDF2.PdfReader(temp_logo_pdf_file)
        pdf_writer = PyPDF2.PdfWriter()
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            if page_num == 0:
                page.merge_page(temp_logo_pdf_reader.pages[0])
            pdf_writer.add_page(page)

        # Write the PDF to the BytesIO object
        pdf_bytes_io = BytesIO()
        pdf_writer.write(pdf_bytes_io)
        pdf_bytes_io.seek(0)  # Reset the cursor to the beginning of the file

    # Connect to Supabase
    #supabase: SupabaseClient = create_client(supabase_url, supabase_api_key)
    url: str = os.environ.get(supabase_url)
    key: str = os.environ.get(supabase_api_key)
    supabase: Client = create_client(url, key)

    # Define path in the bucket
    path = f'june/{restaurant}_Tax_Invoice_from_Qlub.pdf'

    # Upload the PDF from the BytesIO object to the specified path in the bucket
    result = supabase.storage.create_signed_url(bucket_name, path, file=pdf_bytes_io)

    # Check for errors
    if result['error']:
        print('Error uploading PDF:', result['error'])
    else:
        print('PDF uploaded successfully:', result['data'])


def main():
    """Main function to run the revenue report generator."""
    initialize_streamlit()
    dt_start = get_start_date()
    dt_end = get_end_date()
    google_drive_folder_id = '1QecPAve2UXzBk5_6zYC3NgFCFXQWxra_'
    credentials_path = 'client_secret_811309362652-buvv861nns47b9dsr0en9i2g5bjlhpsg.apps.googleusercontent.com.json'
    start_date_time = convert_date_format(dt_start, "start")
    end_date_time = convert_date_format(dt_end, "end")
    generate_button = st.button("Generate")
    if generate_button:
        for id in restaurant_ids:
            csv_df = get_csv_from_api(start_date_time, end_date_time, id)
            if csv_df is not None:
                (
                    commission_with_tax,
                    total_bill,
                    tax,
                    commission_without_tax,
                    resto_name,
                ) = process_csv(start_date_time, end_date_time,csv_df)
                sheet_id = "1HiwS7FPYy3Q5tqZ_cG-Dw0Jsqm0f_kjWp2kaEEzdokw"

                address_resto, abn_no = get_restaurant_details_l(resto_name, sheet_id)
                generate_and_upload_invoice(html_template, total_bill, commission_without_tax, tax, commission_with_tax, resto_name, address_resto, abn_no,google_drive_folder_id, credentials_path,id)
                st.write(id)

        st.write("END")
        exit()
if __name__ == "__main__":
    main()