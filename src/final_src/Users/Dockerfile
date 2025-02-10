FROM node
# Create app directory
WORKDIR /usr/src/app
# Install app dependencies
COPY package*.json ./
RUN npm install
RUN npm install express
RUN npm install uuid
# Copy app source code
COPY . .
#Expose port and start application
EXPOSE 19019
CMD [ "npm", "start" ]