FROM golang:1.24-alpine
WORKDIR /src
COPY hello-world.go .
RUN go build -o /bin/hello ./hello-world.go

FROM scratch
COPY --from=0 /bin/hello /bin/hello
CMD ["/bin/hello"]