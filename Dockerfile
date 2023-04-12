FROM python:3.9.16 AS naas
RUN mkdir -p /opt/NAAS
COPY ./NAAS /opt/NAAS
RUN mkdir -p /opt/NAAS/run
RUN pip3 install -r /opt/NAAS/requirements.txt
RUN chmod +x /opt/NAAS/gunicorn_start.sh
EXPOSE 8000
ENTRYPOINT ["/opt/NAAS/gunicorn_start.sh"]

FROM nginx AS nginx
WORKDIR /etc/nginx
RUN rm /etc/nginx/conf.d/default.conf
COPY ./Nginx-Server/naas.conf /etc/nginx/conf.d
EXPOSE 80