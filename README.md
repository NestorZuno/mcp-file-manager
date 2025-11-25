# 📂 MCP File Manager & Cloud Backup  
Sistema inteligente de gestión de archivos local y en la nube potenciado por IA

Este proyecto implementa un servidor **MCP (Model Context Protocol)** que permite a modelos de lenguaje interactuar con el sistema de archivos local y realizar respaldos en Google Drive.

---

## 🚀 Características Principales

### 🧹 Limpieza Inteligente  
Detecta archivos duplicados utilizando **Hash MD5**, incluso si tienen nombres distintos.

### 🗂️ Organización Automática  
Clasifica archivos por tipo en carpetas como: Imágenes, Documentos, Código, Audio y más.

### ☁️ Respaldo en la Nube  
Integra **Google Drive API v3** para subir archivos críticos automáticamente o bajo demanda.

### 🛡️ Borrado Seguro  
Utiliza **send2trash** para evitar eliminaciones permanentes accidentales.

### 🤖 Interfaz Natural  
Permite control mediante lenguaje natural:  
> "Limpia mi carpeta", "Sube este archivo a Drive", "Organiza mis documentos".

---

## 🛠️ Instalación

### 1. Clonar el repositorio
```bash
git clone https://github.com/tu-usuario/mcp-file-manager.git
cd mcp-file-manager
```

### 2. Crear entorno virtual
```bash
python -m venv venv
```

**Windows**
```bash
.env\Scriptsctivate
```

**Mac/Linux**
```bash
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

---

## ☁️ Configuración para Google Drive

Coloca tu archivo **credentials.json** en la raíz del proyecto.

Luego ejecuta el proceso de autorización:

```bash
python utils/drive_handler.py
```

---

## ⚙️ Uso con Cline / Claude Desktop

```json
{
  "mcpServers": {
    "file-manager": {
      "command": "RUTA_AL_PROYECTO/venv/Scripts/python.exe",
      "args": ["RUTA_AL_PROYECTO/server.py"]
    }
  }
}
```

---

## 🏗️ Estructura del Proyecto

```
mcp-file-manager/
├── server.py                 # Servidor MCP y orquestador de herramientas
├── utils/
│   ├── duplicates.py         # Detección de duplicados (Hash MD5)
│   ├── drive_handler.py      # Autenticación OAuth 2.0 y subida a Google Drive
│   └── organizer.py          # Organización automática de archivos
├── requirements.txt
└── credentials.json          # (Proporcionado por el usuario)
```

---

## 📜 Licencia

Este proyecto está bajo la licencia **MIT**.  
Puedes consultar el archivo completo aquí:

➡️ [LICENSE](./LICENSE)

---

## ✍️ Autor  
**Nestor Zuno Segura**  
Ingeniería en Computación
