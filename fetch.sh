#!/bin/bash
curl \
  "https://s3.amazonaws.com/media.guidebook.com/service/guide_bundle_data/vkQ6bB4Oc4iCSHjsLuZSsvUpJFSbccQZr3KShUgV.json?version=25" \
  | jq > data.json
