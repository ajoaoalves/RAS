# Use an official Node.js image
FROM node:18

# Set the working directory inside the container
WORKDIR /usr/src/app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application source code
COPY . .

# Expose the port your app runs on (change if necessary)
EXPOSE 5173

# Start the application in development mode
CMD ["npm", "run", "dev", "--", "--host"]
