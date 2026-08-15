# ADD CODE HERE

FROM node:20-alpine
WORKDIR /usr/src/app
ENV NODE_ENV=production
COPY package*.json ./
RUN npm ci --only=production && npm cache clean --force
COPY . .
USER node
EXPOSE 4567
CMD ["npm", "start"]
