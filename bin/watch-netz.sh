#!/usr/bin/env bash

# Watch network parameters

e \
    watch \
	--interval=3 \
	--no-title \
	--no-wrap \
	--color \
	--differences \
	    "parallel --jobs=0 --ungroup ::: \
		\"ip -color=always -r -s -s -d route show tab all\" \
		\"64 2> /dev/null | rg ESTAB | rg -v localhost\" \
		\"ip -color=always -s -s -d -h addr show enp5s0\" \
    "
