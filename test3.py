import pandas as pd
import pdfkit


def generate_invoice(data_file, address_file, image_path):
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

    # HTML template for the invoice with a table
    html_template = """
    <!DOCTYPE html>
    <html>
        <head>
            <style>
                .header {
                    background-color: purple;
                    height: 50px;
                    width: 100%;
                }
                .company-address, .image-section {
                    display: inline-block;
                    vertical-align: top;
                }
                .image-section {
                    float: right;
                }
            </style>
        </head>
        <body>
            <div class="header"></div>
            <div class="company-address">
                <p>From: Australia Ptd. Ltd.<br>
                PO Box 18238 Collins Street East VIC 8003<br>
                ABN: 14 649 001 383</p>
            </div>
            <div class="image-section">
                <img src="${image_path}" alt="Company Logo" width="100">
            </div>
            <p>To: ${restaurant}<br>
               ${address_resto}<br>
               ABN: ${abn_no}
            </p>
            <table border="1" style="width: 100%; text-align: left;">
                <tr>
                    <th>Item</th>
                    <th>Amount</th>
                </tr>
                <tr>
                    <td>Total Amount</td>
                    <td>${paid_amount}</td>
                </tr>
                <tr>
                    <td>Commission Amount excluding tax</td>
                    <td>${commission_amount_ex_tax}</td>
                </tr>
                <tr>
                    <td>Tax on Commission (10%)</td>
                    <td>${tax}</td>
                </tr>
                <tr>
                    <td>Commission Amount including tax (${commission_percent}%)</td>
                    <td>${commission_amount_in_tax}</td>
                </tr>
            </table>
            <p>This report is provided to enable you to support a GST credit, if applicable, for the GST incurred on your processing fees.</p>
            <p>&copy; 2023 Technologies and Services Pty Ltd</p>
        </body>
    </html>
    """

    # Iterate through each row in the Excel data
    for index, row in data.iterrows():
        try:
            restaurant = row.get('restaurant_unique[restaurant]', '')
            total_amount = float(row.get('total_amount', 0))
            commission_amount = float(row.get('commission_amount(australia)', 0))
            commission_amount_ex_tax = commission_amount / 1.1
            tax = commission_amount - commission_amount_ex_tax
            commission_amount_ex_tax = round(commission_amount_ex_tax, 2)
            tax = round(tax, 2)
            percent_calc = float(row.get('Paid Amount (excl Qlub Fee)', 1))
            percent = (commission_amount / percent_calc) * 100 if percent_calc else 0
            percent_round = round(percent, 1)

            total_amount = format(total_amount, ',')
            commission_amount_ex_tax = format(commission_amount_ex_tax, ',')
            commission_amount = format(commission_amount, ',')
            tax = format(tax, ',')

            # Searching for restaurant's address and ABN number
            address_row = address_data.loc[address_data['restaurant_unique'] == restaurant]
            address_resto = address_row['address1'].values[0] if not address_row.empty else ''
            abn_no = address_row['config.abn'].values[0] if not address_row.empty else ''

            # Fill the template with data
            html_content = html_template.replace('${paid_amount}', str(total_amount))
            html_content = html_content.replace('${commission_amount_ex_tax}', str(commission_amount_ex_tax))
            html_content = html_content.replace('${tax}', str(tax))
            html_content = html_content.replace('${commission_amount_in_tax}', str(commission_amount))
            html_content = html_content.replace('${commission_percent}', str(percent_round))
            html_content = html_content.replace('${restaurant}', str(restaurant))
            html_content = html_content.replace('${address_resto}', str(address_resto))
            html_content = html_content.replace('${abn_no}', str(abn_no))
            html_content = html_content.replace('${image_path}', str(image_path))

            # Generate PDF from the HTML content
            pdf_filename = f'yu_{restaurant}_{index}.pdf'
            pdfkit.from_string(html_content, pdf_filename)

        except Exception as e:
            print(f"Error processing row {index}: {e}")

    print("Invoice generation process completed.")


# Example usage:
print("hello")
generate_invoice("/Users/irfank/Desktop/everything qlub/yay.xlsx", "/Users/irfank/Desktop/everything qlub/restaurants.csv", "/Users/irfank/Desktop/everything qlub/qlub_log.jpg")
print("ibz")