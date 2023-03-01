#!/bin/bash
datasette publish vercel \
  nicar2023.db \
  --token $VERCEL_TOKEN \
  --scope datasette \
  --project nicar-2023 \
  --metadata metadata.yml \
  --install datasette-search-all \
  --install datasette-graphql \
  --install datasette-json-html \
  --install datasette-ics \
  --install datasette-simple-html \
  --install datasette-copyable \
  --install datasette-pretty-json
