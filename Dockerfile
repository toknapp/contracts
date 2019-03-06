FROM ethereum/solc:0.4.24 as contract-builder

RUN apk add --update make go musl-dev linux-headers

ARG EVM_VERSION=1.8.23
WORKDIR /go-ethereum
RUN wget "https://github.com/ethereum/go-ethereum/archive/v${EVM_VERSION}.tar.gz"
RUN tar -xzf *.tar.gz
WORKDIR /go-ethereum/go-ethereum-${EVM_VERSION}
RUN build/env.sh go run build/ci.go install ./cmd/evm
RUN cp build/bin/evm /usr/bin/evm

WORKDIR /contracts
ADD Makefile .
ADD src src

RUN make contracts


FROM python:3.7.2-alpine3.9

RUN apk add --update make gcc musl-dev

COPY --from=contract-builder /contracts/src/build /contracts
ENV CONTRACT_BUILD_PATH /contracts

WORKDIR /pycontracts
ADD pycontracts /pycontracts

RUN echo "manylinux1_compatible = True" > /usr/local/lib/python3.7/_manylinux.py
RUN make deps

ENTRYPOINT ["make"]
