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


def generate_invoice(data_file, address_file):
    """
    Generate an invoice based on the data in the given Excel file.

    Parameters:
    data_file (str): The path to the Excel file containing the data.

    Returns:
    None
    """
    try:
        # Load data from Excel
        data = pd.read_excel(data_file)
    except Exception as e:
        print(f"Error loading Excel file: {e}")
        return
    try:
        address_data = pd.read_csv(address_file)
    except Exception as e:
        print(f"Error loading Admin panel data dump file: {e}")
        return
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
        <h1>Transaction Report</h1>
        <p>Statement Period: 01/06/2023 to 30/06/2023</p>
        <table>
            <tr>
                <th>A</th>
                <th>Revenue</th>
                <th>$0.00</th>
            </tr>
            <tr>
                <td></td>
                <td>Bill value</td>
                <td>$0.00</td>
            </tr>
            <tr>
                <td></td>
                <td>Tips</td>
                <td>$0.00</td>
            </tr>
            <tr>
                <td></td>
                <td>Surcharge</td>
                <td>$0.00</td>
            </tr>
            <tr>
                <td></td>
                <td>Refunds</td>
                <td>$0.00</td>
            </tr>
            <tr>
                <td></td>
                <td>Total</td>
                <td>$0.00</td>
            </tr>
            <tr>
                <th>B</th>
                <th>Deductibles</th>
                <th>$0.00</th>
            </tr>
            <tr>
                <td></td>
                <td>Total Commission</td>
                <td>$1,767.63</td>
            </tr>
            <tr>
                <th>C</th>
                <th>Net Receivable</th>
                <th>$0.00</th>
            </tr>
            <tr>
                <th>D</th>
                <th>Transferred by Qlub</th>
                <th>$0.00</th>
            </tr>
            <tr>
                <td colspan="3" style="border-bottom: none;"></td>
            </tr>
        </table>
        <p>&copy; FAST TECHNOLOGY GROUP AUSTRALIA PTY LTD</p>
    </body>
</html>















    """

    # HTML template for the invoice
    # HTML template for the invoice with a table

    # Iterate through each row in the Excel data
    for index, row in data.iterrows():
        try:
            restaurant = row.get('restaurant_unique[restaurant]', '')
            total_amount = float(row.get('total_amount', 0))
            payable = float(row.get('Payment(Australia)', 0))
            commission_amount = float(row.get('commission_amount(australia)', 0))
            commission_amount_ex_tax = commission_amount / 1.1
            tax = commission_amount - commission_amount_ex_tax
            commission_amount_ex_tax = round(commission_amount_ex_tax, 2)
            tax = round(tax, 2)
            percent_calc = float(row.get('Paid Amount (excl Qlub Fee)', 1))
            percent = (commission_amount / percent_calc) * 100 if percent_calc else 0
            percent_round = round(percent, 1)
            commission_amount = round(commission_amount, 2)

            total_amount = format(total_amount, ',')
            commission_amount_ex_tax = format(commission_amount_ex_tax, ',')
            commission_amount = format(commission_amount, ',')
            tax = format(tax, ',')

            # searching for restaurant's address and ABN number
            # address_row = address_data.loc[address_data['restaurant_unique']==restaurant]
            # address_resto = address_row['address1'].values[0] if not address_row.empty else ''
            # abn_no = address_row['config.abn'].values[0] if not address_row.empty else ''
            # searching for restaurant's address and ABN number
            address_row = address_data.loc[address_data['restaurant_unique'] == restaurant]
            address_resto = address_row['address1'].values[0] if not address_row.empty else ''
            abn_no = address_row['config.abn'].values[0] if not address_row.empty else ''
            print(abn_no)
            # if np.isnan(abn_no):
            # abn_no = ' '
            # print(abn_no)

            # Fill the template with data
            html_content = html_template.replace('${paid_amount}', str(total_amount))
            html_content = html_content.replace('${commission_amount_ex_tax}', str(commission_amount_ex_tax))
            html_content = html_content.replace('${tax}', str(tax))
            html_content = html_content.replace('${commission_amount_in_tax}', str(commission_amount))
            html_content = html_content.replace('${commission_percent}', str(percent_round))
            html_content = html_content.replace('${pay_able}', str(payable))
            html_content = html_content.replace('${restaurant}', str(restaurant))
            html_content = html_content.replace('${address_resto}', str(address_resto))
            html_content = html_content.replace('${abn_no}', str(abn_no))

            # Generate PDF from the HTML content
            pdf_filename = f'temp_{restaurant}_{index}.pdf'
            pdfkit.from_string(html_content, pdf_filename)

            pdf_filename = open(pdf_filename, "rb")
            pdf_reader = PyPDF2.PdfReader(pdf_filename)

            temp_pdf_file = open("/Users/irfank/Desktop/everything qlub/actuals/qlogo.pdf", "rb")
            temp_pdf_reader = PyPDF2.PdfReader(temp_pdf_file)

            # Create a PdfFileWriter object for the output PDF
            pdf_writer = PyPDF2.PdfWriter()
            # Iterate through all pages in the existing PDF
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                # Merge the temporary PDF with the image onto the current page
                if page_num == 0:  # Only add the image to the first page
                    page.merge_page(temp_pdf_reader.pages[0])
                # Add the page to the PdfFileWriter object
                pdf_writer.add_page(page)

            # Save the output PDF
            with open(
                    "/Users/irfank/Desktop/everything qlub/tax/"f'{index}_adi_Update_{restaurant}_Tax Invoice from Qlub.pdf',
                    "wb") as out:
                pdf_writer.write(out)

            # Close the PDF files
            pdf_filename.close()
            temp_pdf_file.close()

        except Exception as e:
            print(f"Error processing row {index}: {e}")

    print("Invoice generation process completed.")


# Example usage:
print("hello")
generate_invoice("/Users/irfank/Desktop/everything qlub/actuals/f_june.xlsx",
                 "/Users/irfank/Desktop/everything qlub/actuals/latest_restaurants.csv")
delete_files("/Users/irfank/Desktop/everything qlub")
print("zbz")


