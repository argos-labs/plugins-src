#!/bin/bash

curl -s -H 'Content-Type: application/json' \
  -d '{"username": "mcchae@vivans.net", "password": "ghkd67RS!@"}' \
    'https://api.elis.rossum.ai/v1/auth/login' | jq

#{"key":"2c16ce7c42b85ea6e60cdae6b00bee728b03c9df"}
