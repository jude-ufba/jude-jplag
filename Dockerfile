FROM python:3.12

WORKDIR /jplag
RUN apt-get update && apt-get install -y maven wget

RUN wget https://github.com/jplag/JPlag/releases/download/v4.3.0/jplag-4.3.0-jar-with-dependencies.jar

ARG USERNAME=userjude
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME

ENV APP_HOME=/jplag

RUN chown -R $USERNAME:$USERNAME $APP_HOME && \
    chmod -R u+rwX $APP_HOME

RUN pip3 install --upgrade pip && pip3 install flask==3.0.2 gunicorn==22.0.0

COPY app.py .
COPY code1.cpp .
COPY code2.cpp .

EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
