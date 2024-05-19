#!/usr/bin/env bash

# Renice & ionice the parent shell

renice \
	34 \
	${PPID} \
&& \
ionice \
	-c3 \
	-p${PPID} \
&& \
ionice -p${PPID}
