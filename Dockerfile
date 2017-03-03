FROM alpine:3.5
MAINTAINER 'Jussi Heinonen<jussi.heinonen@ft.com>'

RUN apk add -U py-pip && pip install --upgrade pip && \
    apk add python-dev bash curl bind-tools  && \
    pip install --upgrade boto3 requests

CMD /bin/bash
