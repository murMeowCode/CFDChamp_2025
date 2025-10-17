FROM node:20-alpine as builder

WORKDIR /app

COPY package*.json ./

RUN npm i && npm list aos

COPY . .

RUN npm run build

FROM nginx:alpine

COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
COPY ssl/ /etc/nginx/ssl/

EXPOSE 80
EXPOSE 443

CMD ["nginx", "-g", "daemon off;"]
