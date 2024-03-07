# include .env file and export its env vars
# (-include to ignore error if it does not exist)
-include .env

.PHONY: all clean install update build test solhint slither mythril upgradeable storage-layout lint snapshot deploy anvil help

DEFAULT_ANVIL_KEY := 0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80

all: clean install build test

# Clean the repo
clean  :; forge clean

# Remove all modules
remove :; rm -rf .gitmodules && rm -rf .git/modules/* && rm -rf lib && touch .gitmodules && git add . && git commit -m "modules"

# Install the Modules
install :; forge install --no-commit

# Update Dependencies
update:; forge update

# Builds
build  :; forge build

# Tests
# --ffi # enable if you need the `ffi` cheat code on HEVM
test :; forge clean && forge test --optimize --optimizer-runs 200 -v

# Run anvil
anvil :; anvil -m 'test test test test test test test test test test test junk' --steps-tracing --block-time 1

# Run solhint
solhint :; solhint -f table "{src,scripts}/**/*.sol"

# slither
# to install slither, visit [https://github.com/crytic/slither]
slither :; slither . --fail-low #--triage-mode

# mythril
mythril :
	@echo " > \033[32mChecking contracts with mythril...\033[0m"
	./tools/mythril.sh

# upgradeable check
upgradeable:
	@echo " > \033[32mChecking upgradeable...\033[0m"
	./tools/checkUpgradeable.sh

# check upgradeable contract storage layout
storage-layout:
	@echo " > \033[32mChecking contract storage layout...\033[0m"
	./tools/checkStorageLayout.sh

# Lints
lint :; npx prettier --plugin=prettier-plugin-solidity  --write "{src,test,scripts}/**/*.sol"

# Generate Gas Snapshots
snapshot :; forge clean && forge snapshot


# Deploy
deploy-anvil:
	@forge script script/Deploy.s.sol:Deploy --chain-id 31337 \
	--rpc-url $(RPC_URL) \
	--private-key $(DEFAULT_ANVIL_KEY) \
	--broadcast --legacy --ffi -vvvv

deploy-sepolia:
	@forge script script/Deploy.s.sol:Deploy --chain-id $(CHAIN_ID) \
	--rpc-url $(RPC_URL) \
	--private-key $(PRIVATE_KEY) \
	--etherscan-api-key $(ETHERSCAN_API_KEY) \
	--verifier-url $(VERIFIER_URL) \
	--broadcast --legacy --ffi --verify -vvvv

deploy-sepolia-no-verify:
	@forge script script/Deploy.s.sol:Deploy --chain-id $(CHAIN_ID) \
	--rpc-url $(RPC_URL) \
	--private-key $(PRIVATE_KEY) \
	--broadcast --legacy --ffi -vvvv