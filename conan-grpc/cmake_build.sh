#!/bin/bash

if [ ! -d "src/grpc" ]; then
  mkdir -p src
  cd src
  git clone https://github.com/grpc/grpc.git
  cd grpc
  git checkout v1.50.0
  git submodule update --init
  cd ../..
fi
mkdir cmake-build
cd cmake-build
cmake .. -DCMAKE_INSTALL_PREFIX=bin \
         -DgRPC_INSTALL=ON \
         -DCMAKE_BUILD_TYPE=Debug \
         -DgRPC_ABSL_PROVIDER=module \
         -DgRPC_CARES_PROVIDER=module \
         -DgRPC_PROTOBUF_PROVIDER=module \
         -DgRPC_RE2_PROVIDER=module \
         -DgRPC_SSL_PROVIDER=package \
         -DgRPC_ZLIB_PROVIDER=package

make -j4
