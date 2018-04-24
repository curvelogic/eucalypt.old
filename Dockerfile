# Build Eucalypt test harness as a container. The eu executable must
# be provided at runtime in an attached volume and env var EXECUTABLE
# must contain the path.
FROM ubuntu:18.04

RUN apt-get update \
 && apt-get install -y libgmp10 python3-pip python3-dev

ADD eut.py eut.py
ADD test test
ADD entrypoint.sh entrypoint.sh

ENV EXECUTABLE "<REPLACEME>"

ENTRYPOINT ["./entrypoint.sh"]

