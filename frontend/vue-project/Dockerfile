FROM node:22-alpine AS build
WORKDIR /app

RUN npm install

COPY . .

RUN npm run build

FROM httpd:2.4-alpine

# enable needed modules
RUN sed -i 's/^#LoadModule rewrite_module/LoadModule rewrite_module/' /usr/local/apache2/conf/httpd.conf && \
    sed -i 's/^#LoadModule proxy_module/LoadModule proxy_module/' /usr/local/apache2/conf/httpd.conf && \
    sed -i 's/^#LoadModule proxy_http_module/LoadModule proxy_http_module/' /usr/local/apache2/conf/httpd.conf && \
    sed -i 's/^#LoadModule proxy_wstunnel_module/LoadModule proxy_wstunnel_module/' /usr/local/apache2/conf/httpd.conf && \
    sed -i 's/^#LoadModule headers_module/LoadModule headers_module/' /usr/local/apache2/conf/httpd.conf

    # my beloved
COPY apache-frontend.conf /usr/local/apache2/conf/extra/vue-frontend.conf
RUN printf '\n# include Vue FE vhost\nInclude conf/extra/vue-frontend.conf\n' >> /usr/local/apache2/conf/httpd.conf

COPY --from=build /app/dist/ /usr/local/apache2/htdocs/

EXPOSE 80
CMD ["httpd-foreground"]
