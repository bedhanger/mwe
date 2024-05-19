#!/usr/bin/env bash

# Renice & ionice the current shell

renice \
	34 \
	${$} \
&& \
ionice \
	-c3 \
	-p${$} \
&& \
ionice -p${$}
