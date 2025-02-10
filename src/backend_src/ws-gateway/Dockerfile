# Use the official Node.js image as the base
FROM node:10-alpine

# Create and set the working directory in the container
WORKDIR /usr/src/app

# Copy package.json and package-lock.json (if it exists)
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the project files
COPY . .

# Expose the port that the application will use
EXPOSE 8180

# Command to start the application
CMD ["node", "server.js"]
