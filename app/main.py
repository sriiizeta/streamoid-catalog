from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.openapi.docs import get_swagger_ui_html  # <- import this

from app.routers.product_router import router
from app.core.database import init_db

app = FastAPI(title="Streamoid Catalog")

# Serve static files (CSS, JS, images)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Setup Jinja2 templates (for HTML rendering)
templates = Jinja2Templates(directory="app/templates")

# Register routers
app.include_router(router)

@app.on_event("startup")
def on_startup():
    init_db()

# Example homepage route that uses CSS
@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# -----------------------------
# Custom Swagger /docs route
# -----------------------------
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title="Streamoid Catalog API Docs",
        swagger_css_url="/static/custom-swagger.css"  # your custom CSS
    )
