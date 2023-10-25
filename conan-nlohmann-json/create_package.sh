#!/bin/bash

git clone https://github.com/nlohmann/json.git
cd json
git checkout v3.11.2
cd ..
conan export .
conan create .
rm json
