FROM node:13.12.0-alpine
WORKDIR /app/frontend

COPY package.json package-lock.json ./

RUN npm install 
RUN npm install react-scripts@3.4.1 -g 
RUN npm install @material-ui/core
RUN npm install @material-ui/icons
RUN npm install bootstrap
RUN npm install recharts
RUN npm install axios

COPY . ./

EXPOSE 3000