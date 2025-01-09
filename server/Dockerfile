FROM golang:1.23 AS build
WORKDIR /
COPY ./ ./
RUN go build -o ./build/main ./cmd

FROM ubuntu
WORKDIR /app
COPY --from=build /build/main ./main

EXPOSE 80
ENTRYPOINT [ "./main" ]