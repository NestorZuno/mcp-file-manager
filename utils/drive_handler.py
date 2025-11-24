import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Permisos: Solo subir y ver archivos creados por esta app
SCOPES = ['https://www.googleapis.com/auth/drive.file']

def get_drive_service():
    """Maneja la autenticación y retorna el cliente de la API de Drive."""
    creds = None
    
    # Rutas absolutas para que funcione invocándolo desde cualquier lugar
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    token_path = os.path.join(base_path, 'token.json')
    creds_path = os.path.join(base_path, 'credentials.json')

    # 1. Cargar token existente
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    
    # 2. Si no hay token válido, iniciar flujo de login
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception:
                # Si falla el refresh, borrar token viejo y re-autenticar
                if os.path.exists(token_path):
                    os.remove(token_path)
                return get_drive_service()
        else:
            if not os.path.exists(creds_path):
                raise FileNotFoundError("¡Falta el archivo credentials.json en la raíz!")
            
            flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Guardar el token nuevo
        with open(token_path, 'w') as token:
            token.write(creds.to_json())

    return build('drive', 'v3', credentials=creds)

def upload_file_to_drive(file_path, folder_id=None):
    """
    Sube un archivo a Drive, opcionalmente a una carpeta específica.
    """
    try:
        if not os.path.exists(file_path):
            return f"Error: El archivo local {file_path} no existe."

        # print(f"Subiendo a Drive: {file_path}...") # Opcional: logs
        service = get_drive_service()
        
        file_metadata = {'name': os.path.basename(file_path)}
        
        # Si nos dieron un ID de carpeta, lo agregamos como padre
        if folder_id:
            file_metadata['parents'] = [folder_id]
        
        media = MediaFileUpload(file_path, resumable=True)
        
        file = service.files().create(
            body=file_metadata, 
            media_body=media, 
            fields='id'
        ).execute()
        
        return f"Éxito: Archivo subido a Drive. ID: {file.get('id')}"

    except Exception as e:
        return f"Error subiendo a Drive: {str(e)}"

# Bloque para probar la conexión manualmente (python utils/drive_handler.py)
if __name__ == "__main__":
    print("--- Prueba de Conexión a Drive ---")
    try:
        service = get_drive_service()
        print("✅ Autenticación correcta. Token generado.")
    except Exception as e:
        print(f"❌ Error: {e}")