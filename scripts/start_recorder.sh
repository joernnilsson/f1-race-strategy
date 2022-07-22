#!/usr/bin/env bash

die () {
    echo >&2 "$@"
    exit 1
}

docker build . -t f1-strategy || die "Error building container"
mkdir -p $(pwd)/fastf1_cache/recorded || die "Error creating data directory"
docker run -it --rm -v $(pwd)/fastf1_cache:/fastf1_cache f1-strategy python3 dataprovider_fastf1_live_recoder.py  || die "Error starting recorder"