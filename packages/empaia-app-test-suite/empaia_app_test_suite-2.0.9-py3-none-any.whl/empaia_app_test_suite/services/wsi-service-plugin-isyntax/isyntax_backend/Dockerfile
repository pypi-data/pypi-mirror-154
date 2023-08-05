FROM registry.gitlab.com/empaia/integration/ci-docker-images/test-runner:0.1.19@sha256:13e74d28f64500593b1af06a00eb1a30e3fb6663abf1ce4bdc0fe781cb08c1b5 AS build0

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY isyntax_backend /isyntax/isyntax_backend
COPY pyproject.toml /isyntax/pyproject.toml

WORKDIR /isyntax

RUN python3 -m venv .venv
RUN poetry build

FROM ubuntu:18.04@sha256:d21b6ba9e19feffa328cb3864316e6918e30acfd55e285b5d3df1d8ca3c7fd3f

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install --no-install-recommends -y python3-pip python3-wheel unzip

COPY philips-pathologysdk-2.0-ubuntu18_04_py36_research.zip /isyntax/philips-pathologysdk-2.0-ubuntu18_04_py36_research.zip

WORKDIR /isyntax

RUN unzip philips-pathologysdk-2.0-ubuntu18_04_py36_research.zip \
    && cd philips-pathologysdk-2.0-ubuntu18_04_py36_research \
    && chmod 777 InstallPathologySDK.sh \
    && ./InstallPathologySDK.sh py3 -y \
    && cd .. \
    && rm -r philips-pathologysdk-2.0-ubuntu18_04_py36_research

COPY --from=build0 /isyntax/dist/*.whl /tmp
RUN pip3 install /tmp/*.whl

RUN mkdir /data

CMD ["python3", "-m", "isyntax_backend"]
