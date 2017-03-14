FROM alpine:3.5
MAINTAINER 'Jussi Heinonen<jussi.heinonen@ft.com>'

RUN apk add -U py-pip && pip install --upgrade pip && \
    apk add python-dev bash curl bind-tools ruby shadow && \
    pip install --upgrade boto3 requests pyyaml &&\
    gem install puppet --no-rdoc --no-ri

CMD /bin/bash
