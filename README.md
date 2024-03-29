<!-- markdownlint-disable -->
<p align="center">
  <img width="180" src="./OpenAgent.svg" alt="OpenAgent logo">
</p>
<p align="center">
  <a href="https://link.rss3.io/x"><img src="https://img.shields.io/twitter/follow/rss3_?color=%230072ff" alt="follow RSS3 on X"></a>
  <a href="https://link.rss3.io/discord"><img src="https://img.shields.io/badge/chat-discord-blue?style=flat&logo=discord&color=%230072ff" alt="Join RSS3 Discord"></a>
  <!-- add NPM and other badges when needed -->
</p>
<!-- markdownlint-enable -->

# OpenAgent Framework

OpenAgent is a framework for building AI applications leveraging the power of blockchains and RSS3 Network.

The framework consists of 3 main components that are deployed together to form a complete application.

## Backend: LLM, Experts

A set of APIs for responding to requests from the frontend. It leverages LangChain to offer interoperability between different LLMs.

It leverages the power of RSS3 Network to retrieve knowledge and feed into designated Experts.

Theoretically, it is compatible with any LLMs with function calling capability.

See [backend/README.md](backend/README.md) for more information on development and deployment.

## Frontend: Client

A sample web application that serves and a Client to enable user interactions with the backend.

See [frontend/README.md](frontend/README.md) for more information on development and deployment.

## Executor

A set of APIs for executing and submitting transactions on chain. It should be gated under all circumstances to prevent unauthorized access.

In addition, the repository also contains a set of sample smart contracts that need to be deployed before you can use the Executor. See [executor/contracts/README.md](executor/contracts/README.md) for more information.

See [executor/README.md](executor/README.md) for more information on development and deployment.
