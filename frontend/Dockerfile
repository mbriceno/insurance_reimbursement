# Usamos una imagen ligera de Node.js
FROM node:20-slim

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiamos los archivos de dependencias primero para aprovechar la caché de Docker
COPY package*.json ./

# Instalamos las dependencias
RUN npm install

# Copiamos el resto del código fuente
COPY . .

# Exponemos el puerto de Vite (usualmente 5173)
EXPOSE 5173

# Comando para iniciar el servidor de desarrollo
CMD ["npm", "run", "dev", "--", "--host"]