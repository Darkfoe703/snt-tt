# app/infrastructure/config/templates.py
from fastapi.templating import Jinja2Templates

# Configurar templates
templates = Jinja2Templates(directory="app/infrastructure/api/web/templates")

# Añadir función static al contexto
def url_for_static(path: str):
    return f"/static/{path}"

templates.env.globals['static'] = url_for_static