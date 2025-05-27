from fastapi import HTTPException, Response, Request, APIRouter
from weasyprint import HTML
import jinja2
from app.database.connection import db
import traceback

router = APIRouter()

# @router.get("/products/report/pdf")
# async def generate_product_report(request: Request):
#     print("✅ ROUTE HIT", flush=True)
#     try:
#         # Static content to test PDF generation
#         html_content = """
#         <html>
#             <head><title>Test PDF</title></head>
#             <body><h1>PDF Generated Successfully!</h1></body>
#         </html>
#         """

#         # Generate PDF from static HTML content
#         pdf_file = HTML(string=html_content).write_pdf()

#         return Response(content=pdf_file, media_type="application/pdf", headers={
#             "Content-Disposition": "inline; filename=test_report.pdf"
#         })

#     except Exception as e:
#         print("❌ PDF generation error:", e, flush=True)
#         traceback.print_exc()
#         raise HTTPException(status_code=500, detail="Failed to generate PDF")

@router.get("/products/report/pdf")
async def generate_product_report(request: Request):
    print("✅ ROUTE HIT", flush=True)
    try:
        products = []
        async for item in db.products.find():
            item["_id"] = str(item["_id"])
            products.append(item)

        # Print the products data for debugging
        print("✅ Products data:", products, flush=True)

        # Set up template rendering
        template_loader = jinja2.FileSystemLoader("app/templates")
        env = jinja2.Environment(loader=template_loader)
        template = env.get_template("product_report.html")

        html_content = template.render(products=products)

        pdf_file = HTML(string=html_content).write_pdf()

        return Response(content=pdf_file, media_type="application/pdf", headers={
            "Content-Disposition": "inline; filename=product_report.pdf"
        })

    except Exception as e:
        print("❌ PDF generation error:", e, flush=True)
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Failed to generate PDF")