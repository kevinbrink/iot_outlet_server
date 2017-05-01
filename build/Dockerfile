FROM alpine

# basic flask environment
RUN apk add --no-cache bash git nginx uwsgi uwsgi-python py2-pip \
	&& pip2 install --upgrade pip \
	&& pip2 install flask

# application folder
ENV APP_DIR /app

# app dir
RUN mkdir ${APP_DIR} \
	&& chown -R nginx:nginx ${APP_DIR} \
	&& chmod 777 /run/ -R \
	&& chmod 777 /root/ -R
VOLUME [${APP_DIR}]
WORKDIR ${APP_DIR}

# expose web server port
# only http, for ssl use reverse proxy
EXPOSE 80

# exectute start up script
ENTRYPOINT ["python"]
CMD ["app.py"]
