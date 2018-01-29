#!/usr/bin/env bash

cat $1 | jq '.id, .created_at, .time' | xargs -n 3 | sort -n -k 1 | uniq
