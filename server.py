import os
import sys

# Asegurar rutas
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from fastmcp import FastMCP
from send2trash import send2trash  # <--- NUEVA LIBRERÍA DE SEGURIDAD

# Importaciones
try:
    from utils.duplicates import find_duplicates as find_duplicates_logic
    from utils.organizer import organize_by_extension as organize_logic
    try:
        from utils.drive_handler import upload_file_to_drive as upload_logic
    except ImportError:
        upload_logic = None
except ImportError as e:
    sys.stderr.write(f"Error critico: {e}\n")
    find_duplicates_logic = None
    organize_logic = None
    upload_logic = None

mcp = FastMCP("OrganizadorPro")

# --- HERRAMIENTAS BÁSICAS ---

@mcp.tool()
def list_files(path: str = ".") -> list[str]:
    """Lista los archivos dentro de un directorio."""
    try:
        return os.listdir(path)
    except Exception as e:
        return [f"Error: {e}"]

@mcp.tool()
def get_folder_stats(path: str = ".") -> dict:
    """
    (NUEVO) Devuelve estadísticas de la carpeta: cantidad de archivos y peso total.
    Ideal para reportes antes de limpiar.
    """
    total_size = 0
    file_count = 0
    try:
        for dirpath, _, filenames in os.walk(path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                # Skip venv/git for stats
                if "venv" in fp or ".git" in fp: continue
                try:
                    total_size += os.path.getsize(fp)
                    file_count += 1
                except: pass
        
        # Convertir a MB
        size_mb = round(total_size / (1024 * 1024), 2)
        return {"total_files": file_count, "total_size_mb": size_mb, "path": path}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def delete_multiple_files(paths: list[str]) -> dict:
    """
    Manda una lista de archivos a la PAPELERA DE RECICLAJE (Trash).
    Es más seguro que borrar permanentemente.
    """
    report = {"trashed": [], "errors": [], "skipped": []}
    
    for path in paths:
        if "server.py" in path or "venv" in path or ".git" in path:
            report["skipped"].append(path)
            continue

        try:
            if os.path.exists(path):
                # USAMOS SEND2TRASH EN LUGAR DE OS.REMOVE
                send2trash(path)
                report["trashed"].append(path)
            else:
                report["errors"].append(f"No encontrado: {path}")
        except Exception as e:
            report["errors"].append(f"Error en {path}: {str(e)}")
            
    return report

# --- LÓGICA ---

@mcp.tool()
def find_duplicates(path: str) -> list[dict]:
    """Encuentra duplicados por Hash MD5."""
    if find_duplicates_logic:
        return find_duplicates_logic(path)
    return [{"error": "Lógica no cargada."}]

@mcp.tool()
def organize_files(path: str) -> list[str]:
    """Organiza archivos por extensión."""
    if organize_logic:
        return organize_logic(path)
    return ["Error: Lógica no cargada."]

@mcp.tool()
def upload_to_drive(path: str, folder_id: str = None) -> str:
    """Sube archivo a Google Drive."""
    if upload_logic:
        return upload_logic(path, folder_id)
    return "Error: Lógica Drive no configurada."

if __name__ == "__main__":
    mcp.run(transport='stdio')