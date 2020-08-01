# build stage
FROM node:lts-alpine as wd_vue
WORKDIR /vue_app
COPY /client/package*.json ./
RUN npm install
RUN npm fund
COPY /client ./
RUN npm run build

# production stage
FROM nginx:stable-alpine as wd_vue_prod
COPY --from=wd_vue /vue_app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]