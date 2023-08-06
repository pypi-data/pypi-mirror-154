# Open Autonomy

This repository contains the [Valory](https://www.valory.xyz/) stack, a set of 
distributed consensus technologies built on top of the 
[open AEA framework](https://github.com/valory-xyz/open-aea) to facilitate the 
creation of dynamic, decentralised applications that depend on off-chain components.

As opposed to traditional smart contracts, Valory apps go beyond simple, purely 
reactive applications and can show complex, proactive behaviours that contain 
off-chain logic without giving up on decentralization.


## Requirements

Ensure your machine satisfies the following requirements:

- Python `>= 3.7`
- Yarn `>=1.22.xx`
- Node `>=v12.xx`
- [Tendermint](https://docs.tendermint.com/master/introduction/install.html) `==0.34.11`
- [IPFS node](https://docs.ipfs.io/install/command-line/#official-distributions) `==v0.6.0`
- [Pipenv](https://pipenv.pypa.io/en/latest/install/) `>=2021.x.xx`


## Setting up for development & running examples

- Clone the repository, and recursively clone the submodules:

      git clone --recursive git@github.com:valory-xyz/open-autonomy.git

  Note: to update the Git submodules later:

      git submodule update --init --recursive

- Build the Hardhat projects:

      cd third_party/safe-contracts && yarn install
      cd ../..
      cd third_party/contracts-amm && yarn install
      cd ../..

- Create and launch a virtual environment. Also, run this during development, 
every time you need to re-create and launch the virtual environment and update 
the dependencies:

      make new_env && pipenv shell

## Getting started

Have a look at the 
[price estimation](https://github.com/valory-xyz/open-autonomy/tree/main/examples/price_estimation) 
example. You must have completed setting up and be inside a virtual environment
(`pipenv shell`) in order to run the examples.

