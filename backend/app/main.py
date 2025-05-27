from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import (
    auth_routes,
    product_routes,
    report_routes,
    forecast_routes,
    restocking_routes,
    sales_routes,
    analytics_routes,
    dashboard_routes,
    employee_routes  # added
)

app = FastAPI(
    title="Product Inventory System",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register all routers
app.include_router(auth_routes.router)
app.include_router(product_routes.router)
app.include_router(report_routes.router)
app.include_router(forecast_routes.router)
app.include_router(restocking_routes.router)
app.include_router(sales_routes.router)
app.include_router(analytics_routes.router)
app.include_router(dashboard_routes.router)
app.include_router(employee_routes.router)  # now registered

@app.get("/")
def read_root():
    return {"message": "Welcome to the Product Inventory System 👋"}
