# Frontend Dockerfile
# Use official Node image
FROM node:20-alpine

# Set working directory
WORKDIR /app

# Copy package files and install serve
COPY package.json .
RUN npm install --production

# Copy static files
COPY . .

# Expose port
EXPOSE 3000

# Default command to serve the static site
CMD ["npx", "serve", "-s", ".", "-l", "3000"]
