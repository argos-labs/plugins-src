#!/bin/bash

curl -s -H 'Authorization: token 2c16ce7c42b85ea6e60cdae6b00bee728b03c9df"'
  'https://api.elis.rossum.ai/v1/queues?page_size=1' | jq -r .results[0].url

#https://api.elis.rossum.ai/v1/queues/8199
