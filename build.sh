#!/usr/bin/env bash

# Set cargo and rustup directories to a writable path
export CARGO_HOME=$HOME/.cargo
export RUSTUP_HOME=$HOME/.rustup

# Install Rust
curl https://sh.rustup.rs -sSf | sh -s -- -y
source $HOME/.cargo/env

# Install Python dependencies
pip install -r requirements.txt
