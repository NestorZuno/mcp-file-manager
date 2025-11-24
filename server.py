import os
import sys

# --- FIX DE INGENIERÍA PARA RUTAS ---
# Esto asegura que Python encuentre la carpeta 'utils' sin importar
# desde dónde ejecute Claude el script.
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from fastmcp import FastMCP

# Intentamos importar los módulos. Si falta alguna librería (ej. Drive),
# el servidor sigue funcionando con las otras herramientas.
try:
    from utils.duplicates import find_duplicates as find_duplicates_logic
    from utils.organizer import organize_by_extension as organize_logic
    
    try:
        from utils.drive_handler import upload_file_to_drive as upload_logic
    except ImportError:
        upload_logic = None

except ImportError as e:
    # Usamos stderr para no romper el protocolo JSON-RPC de Claude
    sys.stderr.write(f"Error critico importando modulos: {e}\n")
    find_duplicates_logic = None
    organize_logic = None
    upload_logic = None

# Inicializar servidor
mcp = FastMCP("OrganizadorPro")

# ==========================================
# HERRAMIENTAS DE GESTIÓN DE ARCHIVOS
# ==========================================

@mcp.tool()
def list_files(path: str = ".") -> list[str]:
    """Lista los archivos dentro de un directorio."""
    try:
        return os.listdir(path)
    except Exception as e:
        return [f"Error leyendo directorio: {e}"]

@mcp.tool()
def delete_multiple_files(paths: list[str]) -> dict:
    """
    Elimina una lista de archivos.
    CRÍTICO: Úsalo para borrar los duplicados identificados.
    """
    report = {"deleted": [], "errors": [], "skipped": []}
    
    for path in paths:
        # PROTECCIÓN: Evitar borrar archivos del propio sistema del proyecto
        if "server.py" in path or "venv" in path or ".git" in path:
            report["skipped"].append(path)
            continue

        try:
            if os.path.exists(path):
                os.remove(path)
                report["deleted"].append(path)
            else:
                report["errors"].append(f"No encontrado: {path}")
        except Exception as e:
            report["errors"].append(f"Error al borrar {path}: {str(e)}")
            
    return report

# ==========================================
# HERRAMIENTAS DE LÓGICA AVANZADA
# ==========================================

@mcp.tool()
def find_duplicates(path: str) -> list[dict]:
    """
    Busca archivos duplicados comparando su contenido (Hash MD5).
    Retorna una lista de diccionarios con 'original' y 'duplicate'.
    """
    if find_duplicates_logic:
        return find_duplicates_logic(path)
    return [{"error": "Lógica de duplicados no cargada."}]

@mcp.tool()
def organize_files(path: str) -> list[str]:
    """
    Organiza los archivos de una carpeta moviéndolos a subcarpetas
    según su extensión (ej: .jpg -> /jpg).
    """
    if organize_logic:
        return organize_logic(path)
    return ["Error: Lógica de organizador no cargada."]

# ==========================================
# HERRAMIENTA DE LA NUBE (GOOGLE DRIVE)
# ==========================================

@mcp.tool()
def upload_to_drive(path: str, folder_id: str = None) -> str:
    """
    Sube un archivo local a Google Drive.
    
    Args:
        path: Ruta completa del archivo local.
        folder_id: (Opcional) El ID de la carpeta en Drive donde guardar el archivo.
                    Si no se pone nada, se guarda en la raíz de 'Mi Unidad'.
    """
    if upload_logic:
        return upload_logic(path, folder_id)
    return "Error: Lógica de Drive no configurada o librerías faltantes."

if __name__ == "__main__":
    mcp.run(transport='stdio')