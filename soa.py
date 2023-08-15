import pandas as pd
import pdfkit
import PyPDF2
import numpy as np
import os


html = """
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
            <tr><td>A</td><td>Net Transaction Value</td><td>$0.00</td></tr>
            <tr><td></td><td>Revenue (bill value)</td><td>$0.00</td></tr>
            <tr><td></td><td>Tips</td><td>$0.00</td></tr>
            <tr><td></td><td>Surcharge</td><td>$0.00</td></tr>
            <tr><td></td><td>Refunds Processed</td><td>$0.00</td></tr>
            <tr><td>B</td><td>Adjustments</td><td>$0.00</td></tr>
            <tr><td>C</td><td>Qlub Commission</td><td>$0.00</td></tr>
            <tr><td>D</td><td>Net Receivable - (A + B + C)</td><td>$0.00</td></tr>
            <tr><td>E</td><td>Transferred by Qlub</td><td>$0.00</td></tr>
            <tr><td>F</td><td>Over- / (under-) settled - ( E - D )</td><td>$0.00</td></tr>
        </table>
        <p>&copy; FAST TECHNOLOGY GROUP AUSTRALIA PTY LTD</p>
    </body>
</html>



"""

htm = """
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
  border-collapse: collapse;
  width: 100%;
}

td, th {
  border: 1px solid #333;
  padding: 5px; 
}

th {
  background-color: #333;
  color: white;
}

</style>

</head>

<body>

<div class="rectangle"></div>

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
    <th></th>
    <th></th>
    <th></th>
  </tr>

  <tr>
    <td colspan="3"></td>
  </tr>

  <tr>
    <td colspan="3"></td>
  </tr>

  <tr>
    <td colspan="3"></td>
  </tr>

  <tr>
    <td></td>
    <th>A</th>
    <th>Net Transaction Value</th>
  </tr>

  <tr>
    <td></td>
    <td>Revenue (bill value)</td>  
    <td>0.00</td>
  </tr>

  <tr>
    <td></td>
    <td>Tips</td>
    <td>0.00</td>
  </tr>

  <tr>
    <td></td>
    <td>Surcharge</td>
    <td>0.00</td>
  </tr>

  <tr>
    <td></td>
    <td>Refunds Processed</td>
    <td>0.00</td>
  </tr>

  <tr>
    <td></td>
    <td></td>
    <td></td>
  </tr>

  <tr>
    <td></td>
    <th>B</th>
    <th>Adjustments</th>
  </tr>

  <tr>
    <td></td>
    <td></td>
    <td>0.00</td>
  </tr>

  <tr>
    <td></td>
    <th>C</th> 
    <th>Qlub Commission</th>
  </tr>

  <tr>
    <td></td>
    <td></td>
    <td>0.00</td>
  </tr>

  <tr>
    <td></td>
    <th>D</th>
    <th>Net Receivable - (A + B + C)</th>
  </tr>

  <tr>
    <td></td>
    <td></td>
    <td>0.00</td>
  </tr>

  <tr>
    <td></td>
    <th>E</th>
    <th>Transferred by Qlub</th>
  </tr>

  <tr>
    <td></td>
    <td></td>
    <td>0.00</td>
  </tr>

  <tr>
    <td></td>
    <th>F</th>
    <th>Over- / (under-) settled - (E - D)</th>
  </tr>

  <tr>
    <td></td>
    <td></td> 
    <td>0.00</td>
  </tr>

</table>

<p>&copy; FAST TECHNOLOGY GROUP AUSTRALIA PTY LTD</p>

</body>
</html>



"""

ht ="""

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
  border-collapse: collapse;
  width: 100%;
}

td, th {
  border: 1px solid #333; 
  padding: 5px 10px;
  vertical-align: top;
}

th {
  background-color: #333;
  color: white;
  text-align: right;
  border-top: 1px solid #333;
  border-right: 1px solid #333; 
}

tr:empty {
  border-bottom: none;
}

</style>

</head>

<body>

<div class="rectangle"></div>

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
    <th></th>
    <th></th>
    <th></th>
  </tr>

  <tr></tr>

  <tr></tr>

  <tr></tr>

  <tr>
    <td></td>
    <th>A</th> 
    <th>Net Transaction Value</th>
  </tr>

  <tr>
    <td></td>
    <td>Revenue (bill value)</td>
    <td>0.00</td>
  </tr>

  <tr>
    <td></td>
    <td>Tips</td>
    <td>0.00</td>
  </tr>

  <tr>
    <td></td>
    <td>Surcharge</td>
    <td>0.00</td>
  </tr>

  <tr>
    <td></td>
    <td>Refunds Processed</td>
    <td>0.00</td>
  </tr>

  <tr></tr>

  <tr>
    <td></td>
    <th>B</th>
    <th>Adjustments</th>
  </tr>

  <tr>
    <td></td>
    <td></td>
    <td>0.00</td>
  </tr>

  <tr>
    <td></td>
    <th>C</th>
    <th>Qlub Commission</th>
  </tr>

  <tr>
    <td></td>
    <td></td>
    <td>0.00</td>
  </tr>

  <tr>
    <td></td>
    <th>D</th>
    <th>Net Receivable - (A + B + C)</th>
  </tr>

  <tr>
    <td></td>
    <td></td>
    <td>0.00</td>
  </tr>

  <tr>
    <td></td>
    <th>E</th>
    <th>Transferred by Qlub</th>
  </tr>

  <tr>
    <td></td>
    <td></td>
    <td>0.00</td>
  </tr>

  <tr>
    <td></td>
    <th>F</th>
    <th>Over- / (under-) settled - (E - D)</th>
  </tr>

  <tr>
    <td></td>
    <td></td>
    <td>0.00</td>
  </tr>

</table>

<p>&copy; FAST TECHNOLOGY GROUP AUSTRALIA PTY LTD</p>

</body>
</html>




"""

htm0 = """
<!DOCTYPE html>
<html>

<head>

<style>

table {
  border-collapse: collapse;
  width: 100%;
}

td, th {
  border: 1px solid #333; 
  padding: 5px 10px;
  vertical-align: top;
}

th {
  background-color: #333;
  color: white;
  text-align: right;
  border-top: 1px solid #333;
  border-right: 1px solid #333; 
}

tr:empty {
  border-bottom: none;
}

</style>

</head>

<body>

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



  <tr></tr>

  <tr></tr>

  <tr></tr>

  <tr>
    <th>A</th>
    <td></td>
    <th>Net Transaction Value</th>
  </tr>

  <tr>
    <td></td>
    <td>Revenue (bill value)</td>
    <td>0.00</td>
  </tr>

  <tr>
    <td></td>
    <td>Tips</td>
    <td>0.00</td>
  </tr>

  <tr>
    <td></td>
    <td>Surcharge</td>
    <td>0.00</td>
  </tr>

  <tr>
    <td></td>
    <td>Refunds Processed</td>
    <td>0.00</td>
  </tr>

  <tr></tr>

  <tr>
    <th>B</th>
    <td></td>
    <th>Adjustments</th>
  </tr>

  <tr>
    <td></td>
    <td></td>
    <td>0.00</td>
  </tr>

  <tr>
    <th>C</th>
    <td></td>
    <th>Qlub Commission</th>
  </tr>

  <tr>
    <td></td>
    <td></td>
    <td>0.00</td>
  </tr>

  <tr>
    <th>D</th>
    <td></td>
    <th>Net Receivable - (A + B + C)</th>
  </tr>

  <tr>
    <td></td>
    <td></td>
    <td>0.00</td>
  </tr>

  <tr>
    <th>E</th>
    <td></td>
    <th>Transferred by Qlub</th>
  </tr>

  <tr>
    <td></td>
    <td></td>
    <td>0.00</td>
  </tr>

  <tr>
    <th>F</th>
    <td></td>
    <th>Over- / (under-) settled - (E - D)</th>
  </tr>

  <tr>
    <td></td>
    <td></td>
    <td>0.00</td>
  </tr>

</table>

<p>&copy; FAST TECHNOLOGY GROUP AUSTRALIA PTY LTD</p>

</body>
</html>


"""

chut = """
<!DOCTYPE html>
<html>

<head>

<style>

table {
  border-collapse: collapse;
  width: 100%;
}

td, th {
  border: 1px solid #333; 
  padding: 5px 10px;
  vertical-align: top;
}

th.darkened {
  background-color: #333;
  color: white;
  text-align: right;
  border-top: 1px solid #333;
  border-right: 1px solid #333; 
}

td.darkened {
  background-color: #ddd;
}

tr:empty {
  border-bottom: none;
}

</style>

</head>

<body>

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
    <th></th>
    <th class="darkened"></th>
    <th></th>
  </tr>

  <tr>
    <th>A</th>
    <td class="darkened">Net Transaction Value</td>
    <td>0.00</td>
  </tr>

  <tr>
    <td></td>
    <td class="darkened">Revenue (bill value)</td>
    <td>0.00</td>
  </tr>

  <tr>
    <td></td>
    <td class="darkened">Tips</td>
    <td>0.00</td>
  </tr>

  <tr>
    <td></td>
    <td class="darkened">Surcharge</td>
    <td>0.00</td>
  </tr>

  <tr>
    <td></td>
    <td class="darkened">Refunds Processed</td>
    <td>0.00</td>
  </tr>

  <tr>
    <th>B</th>
    <td class="darkened">Adjustments</td>
    <td>0.00</td>
  </tr>

  <tr>
    <th>C</th>
    <td class="darkened">Qlub Commission</td>
    <td>0.00</td>
  </tr>

  <tr>
    <th>D</th>
    <td class="darkened">Net Receivable - (A + B + C)</td>
    <td>0.00</td>
  </tr>

  <tr>
    <th>E</th>
    <td class="darkened">Transferred by Qlub</td>
    <td>0.00</td>
  </tr>

  <tr>
    <th>F</th>
    <td class="darkened">Over- / (under-) settled - (E - D)</td>
    <td>0.00</td>
  </tr>

</table>

<p>&copy; FAST TECHNOLOGY GROUP AUSTRALIA PTY LTD</p>

</body>
</html>

"""

po3 ="""
<!DOCTYPE html>
<html>

<head>

<style>

table {
  border-collapse: collapse;
  width: 100%;
}

td, th {
  border: 1px solid #333; 
  padding: 5px 10px;
  vertical-align: top;
}

th {
  background-color: #333;
  color: white;
  text-align: right;
  border-top: 1px solid #333;
  border-right: 1px solid #333; 
}

tr:empty {
  border-bottom: none;
}

.dark-cell {
  background-color: #333;
  color: white;
}

</style>

</head>

<body>

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
    <th class="dark-cell">A</th>
    <th>Net Transaction Value</th>
    <td></td>
  </tr>

  <tr>
    <td></td>
    <td>Revenue (bill value)</td>
    <td>0.00</td>
  </tr>

  <tr>
    <td></td>
    <td>Tips</td>
    <td>0.00</td>
  </tr>

  <tr>
    <td></td>
    <td>Surcharge</td>
    <td>0.00</td>
  </tr>

  <tr>
    <td></td>
    <td>Refunds Processed</td>
    <td>0.00</td>
  </tr>

  <tr>
    <th class="dark-cell">B</th>
    <th>Adjustments</th>
    <td></td>
  </tr>

  <tr>
    <td></td>
    <td></td>
    <td>0.00</td>
  </tr>

  <tr>
    <th class="dark-cell">C</th>
    <th>Qlub Commission</th>
    <td></td>
  </tr>

  <tr>
    <td></td>
    <td></td>
    <td>0.00</td>
  </tr>

  <tr>
    <th class="dark-cell">D</th>
    <th>Net Receivable - (A + B + C)</th>
    <td></td>
  </tr>

  <tr>
    <td></td>
    <td></td>
    <td>0.00</td>
  </tr>

  <tr>
    <th class="dark-cell">E</th>
    <th>Transferred by Qlub</th>
    <td></td>
  </tr>

  <tr>
    <td></td>
    <td></td>
    <td>0.00</td>
  </tr>

  <tr>
    <th class="dark-cell">F</th>
    <th>Over- / (under-) settled - (E - D)</th>
    <td></td>
  </tr>

  <tr>
    <td></td>
    <td></td>
    <td>0.00</td>
  </tr>

</table>

<p>&copy; FAST TECHNOLOGY GROUP AUSTRALIA PTY LTD</p>

</body>
</html>


"""
pdf_filename= '7sucks.pdf'

pdfkit.from_string(po3, pdf_filename)