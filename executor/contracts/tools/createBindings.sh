#!/usr/bin/env bash
set -x

base_path="./build/bindings"
BIN_DIR="$base_path/bin"
ABI_DIR="$base_path/abi"
GO_DIR="$base_path/go"

rm -rf base_path && mkdir -p ${BIN_DIR} ${ABI_DIR} ${GO_DIR}

for contract in OpenAgentExecutorManager
do
  # extract abi and bin files
  forge inspect ${contract} abi > ${ABI_DIR}/${contract}.abi
  forge inspect ${contract} bytecode > ${BIN_DIR}/${contract}.bin

  # generate go binding files
  pkg=$(echo ${contract:0:1} | tr '[A-Z]' '[a-z]')${contract:1}
  abigen --bin=${BIN_DIR}/${contract}.bin --abi=${ABI_DIR}/${contract}.abi --pkg=${pkg} --out=${GO_DIR}/${pkg}.go
done