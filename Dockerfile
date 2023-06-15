FROM maven:3.8.6-eclipse-temurin-17

# clone specific version
RUN mkdir /jplag && \
  cd /jplag && \
  git clone https://github.com/jplag/JPlag.git . && \
  git checkout b886f5504e1f86df331273aaa425dbf672268d48

# build jplag
RUN cd /jplag && \
  mvn clean package assembly:single

RUN ls -l /jplag/jplag.cli/target