#!/usr/bin/env bash

# Watch network parameters

e \
    watch \
	--interval=3 \
	--no-title \
	--no-wrap \
	--color \
	--differences \
	    "\
		ip -color=always -r -s -s -d route show tab all ;\
		ip -color=always -r rule list ;\
		ip -color=always -r -s -s -d neighbour ;\
		64 2> /dev/null | rg ESTAB | rg -v localhost ;\
	    "
