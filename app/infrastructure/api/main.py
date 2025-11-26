# app/infrastructure/api/main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.infrastructure.api.routers import market, universe, items
from app.infrastructure.api.web.routes.views import router as web_router
from fastapi.templating import Jinja2Templates

app = FastAPI(
    title="SNT Trade Tool",
    version="0.1.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)


# Configurar templates con contexto para static files
templates = Jinja2Templates(directory="app/infrastructure/api/web/templates")

# Añadir función static al contexto de templates
def url_for_static(path: str):
    return f"/static/{path}"

templates.env.globals['static'] = url_for_static

# Montar archivos estáticos
app.mount("/static", StaticFiles(directory="app/infrastructure/api/web/static"), name="static")

app.include_router(web_router)
app.include_router(market.router)
app.include_router(universe.router)
app.include_router(items.router)


# @app.get("/")
# async def root():
#     return {"message": "SNT Trade Tool - EVE Online Market Bot"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
