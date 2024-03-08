# OpenAgent

OpenAgent is a framework for building AI applications leveraging the power of blockchains and RSS3 Network.

The framework consists of 4 main components:

## backend

A set of APIs for responding to requests from the frontend. It leverages LangChain to offer interoperability between different LLMs.

It leverages the power of RSS3 Network to retrieve knowledge and feed into the designated LLMs.

Theoretically, it is compatible with any LLMs that conform to the LangChain OpenAI GPT-3 API syntax.

## frontend

A web application that allows users to interact with the backend and the wallet backend.

## wallet-contracts

A set of smart contracts that enables transactions between different the users and AI agents.

## wallet-backend

A set of APIs for managing the smart contract wallet. It should be gated under all circumstances to prevent unauthorized access.
