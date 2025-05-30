# Imagen base oficial de Python
FROM python:3.12-slim

# Establecer directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar archivo de dependencias
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto de la app
COPY . .

# Exponer el puerto que usa Flask
EXPOSE 5000

# Comando para ejecutar la app
CMD ["python", "main.py"]
