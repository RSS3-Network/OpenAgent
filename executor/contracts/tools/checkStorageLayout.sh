#!/usr/bin/env bash
set -x

if [ ! -d "src" ]; then
	echo "error: script needs to be run from project root './tools/checkStorageLayout.sh'"
	exit 1
fi

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
for contract in OpenAgentExecutorManager
do
  file=$(mktemp /tmp/contracts-storage-layout-${contract}.XXXXX) || exit 2
  forge inspect ${contract} storage-layout --pretty > ${file} || exit 3

  diffResult=$(mktemp /tmp/contracts-storage-layout-${contract}.XXXXX) || exit 4
  diff -bB ./tools/storageLayout/${contract}-storage-layout.txt ${file}  > ${diffResult}
  if cat ${diffResult} | grep "^<" >/dev/null
  then
    echo "check ${contract} failed!"
    cat ${diffResult}
    exit 255
  else
    cp ${file} ./tools/storageLayout/${contract}-storage-layout.txt
  fi
done
echo "check storage layout done!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
