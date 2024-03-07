#!/usr/bin/env bash
#set -x

if [ ! -d "src" ]; then
	echo "error: script needs to be run from project root './tools/checkUpgradeable.sh'"
	exit 1
fi

# install slither
which slither-check-upgradeability
if [ $? -ne 0 ]; then
  git clone https://github.com/crytic/slither.git && cd slither || exit 1
  pip3 install .
  cd ..
fi

# copy .env file
if [ ! -f ".env" ]; then
  cp ".env.example" ".env"
fi

# create tmp files
file=$(mktemp /tmp/crossbell-bridge-slither-check.XXXXX) || exit 2

# slither-check
echo "OpenAgentWalletManager: " >"$file"
slither-check-upgradeability . OpenAgentWalletManager \
--proxy-filename . \
--proxy-name TransparentUpgradeableProxy \
--compile-force-framework 'foundry' \
--exclude "initialize-target" \
2>>"$file" 1>&2



# output
lines=$(sed -n '$=' "$file")
# if the check fails, there will be 2+ lines in the files
if [ "$lines" -gt 2 ]
then
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "slither-check failed"
  cat "$file"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  exit 255
else
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "slither-check done"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
fi
