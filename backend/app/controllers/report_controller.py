import pdfkit
from fastapi import Response

def generate_sales_report_pdf(sales_data: list) -> Response:
    """
    Generates a PDF sales report from sales_data and returns it as a FastAPI Response.

    :param sales_data: List of dictionaries with product sales info
    :return: FastAPI Response containing PDF
    """

    # Build HTML report dynamically
    html_content = """
    <html>
    <head>
        <style>
            table { border-collapse: collapse; width: 80%; margin: 20px auto; }
            th, td { border: 1px solid black; padding: 8px; text-align: center; }
            th { background-color: #f2f2f2; }
            h1 { text-align: center; }
        </style>
    </head>
    <body>
        <h1>Sales Report</h1>
        <table>
            <tr>
                <th>Product</th>
                <th>Quantity Sold</th>
                <th>Total Sales ($)</th>
            </tr>
    """

    for item in sales_data:
        html_content += f"""
            <tr>
                <td>{item['product_name']}</td>
                <td>{item['quantity_sold']}</td>
                <td>{item['total_sales']}</td>
            </tr>
        """

    html_content += """
        </table>
    </body>
    </html>
    """

    # Generate PDF from HTML string
    pdf = pdfkit.from_string(html_content, False)

    # Return PDF as response for download
    return Response(
        content=pdf,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=sales_report.pdf"}
    )
