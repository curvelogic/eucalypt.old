# Build Eucalypt test harness as a container. The eu executable must
# be provided at runtime in an attached volume and env var EXECUTABLE
# must contain the path.
FROM ubuntu

ADD test test
ADD entrypoint.sh entrypoint.sh

ENV EXECUTABLE "<REPLACEME>"

ENTRYPOINT ["./entrypoint.sh"]

