FROM python:latest

ARG ENTRYPOINT_CMD
ENV ENTRYPOINT_CMD ${ENTRYPOINT_CMD}

# RUN apt-get update \
#    && apt-get install -y --no-install-recommends \
#        default-libmysqlclient-dev \
#    && rm -rf /var/lib/apt/lists/*

RUN pip3 install pipenv

WORKDIR /opt/backend

COPY ./Pipfile* ./

RUN pipenv --python /usr/bin/python3 && pipenv install --system

COPY ./ /opt/backend/

EXPOSE 8000

#ENTRYPOINT ["/bin/bash"]
CMD ["/bin/bash", "-c", "./entrypoint.sh $ENTRYPOINT_CMD"]
