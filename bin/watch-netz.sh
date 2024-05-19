#!/usr/bin/env bash

# Watch network parameters

TERM=vt100 \
	e \
		watch \
			--interval 3 \
			--no-title \
			--differences \
				"\
					parallel --jobs=0 --ungroup ::: \
						\"ip -r route show\" \
						\"64 2> /dev/null | \
							grep ESTAB | grep -v localhost\" \
						\"ip -s -s -d -h addr show enp5s0\" \
				"
