# Configuración de Puertos

## 🎯 Resumen

El backend ahora está configurado para usar puertos diferentes según el ambiente:

- **Desarrollo Local**: Puerto **8000** (fijo)
- **Producción (Render)**: Puerto asignado automáticamente por Render vía `$PORT`

## 🔧 Configuración del Backend

### En Desarrollo Local

Ejecuta el backend con:

```bash
cd backend
python main.py
```

Esto arrancará el servidor en `http://localhost:8000`

### En Producción (Render)

El archivo `render.yaml` ya está configurado para usar el puerto dinámico de Render:

```yaml
startCommand: uvicorn main:app --host 0.0.0.0 --port $PORT
```

## 🌐 Configuración del Frontend

El frontend ahora detecta automáticamente el ambiente y usa la URL correcta:

### Variables de Entorno

- **`.env.development`**: Apunta a `http://localhost:8000` (desarrollo local)
- **`.env.production`**: Apunta a `https://nodo-miru.onrender.com` (producción)

### ✅ URLs Configuradas

- **Backend**: https://nodo-miru.onrender.com
- **Frontend**: https://nodo-1.onrender.com

## 🚀 Comandos

### Desarrollo Local

```bash
# Terminal 1 - Backend
cd backend
python main.py

# Terminal 2 - Frontend
cd frontend
npm run dev
```

### Build para Producción

```bash
cd frontend
npm run build
```

El build automáticamente usará la URL del backend de producción.

## 📝 Notas

- No necesitas modificar `render.yaml` para cambiar puertos
- El puerto `$PORT` en Render es **obligatorio** y asignado automáticamente
- El frontend se configura automáticamente según el ambiente
