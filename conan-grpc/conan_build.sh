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
mkdir conan-build
cd conan-build

conan install .. --build=missing -pr=desktop
conan build ..
