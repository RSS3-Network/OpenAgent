# OpenAgent Executor

The executor is the component that executes transactions on a blockchain. Itself is a smart contract wallet that can be controlled by the OpenAgent's Experts. You should ensure that the executor is secure and only the Experts can interact with it.

The executor is designed this way so that on chain automation can be achieved (users do not have to sign each transaction manually when actions are triggered).

Other approaches are possible, such as using a KMS relayer to sign transactions on behalf of the user, but requires the user to have advanced knowledge of the KMS.

## Environment Variables

[.env.example](./.env.example) contains the environment variables required.
