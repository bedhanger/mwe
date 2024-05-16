#!/usr/bin/env bash

# Simulate tmux's select-pane -T command

printf '\033]2;%s\033\\' "${@}"
