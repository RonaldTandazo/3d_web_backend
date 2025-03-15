# Usa una imagen base de Python (si es un proyecto en FastAPI)
FROM python:3.9-slim

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar los archivos de tu proyecto (incluyendo los archivos de configuración de Git) al contenedor
COPY . .

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el código de la aplicación al contenedor
COPY . .

# Exponer el puerto en el que corre la aplicación
EXPOSE 8000

# Definir el comando para ejecutar la aplicación FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
