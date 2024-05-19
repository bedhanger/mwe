new-session -sStandard
select-pane -T"Network Connexions"
send-keys -l " renioice.sh ; export DISPLAY=:1 && sct \${night_light_temp:-2222}"

split-window -v
select-pane -TIrssi
send-keys -l " renioice.sh ; export DISPLAY=:1 && sct \${night_light_temp:-2222}"
send-keys -l " e irssi"

new-window
select-pane -T"Emerge et al."
send-keys -l " renioice.sh ; export DISPLAY=:1 && sct \${night_light_temp:-2222}"

new-window
select-pane -T"Gucke"
send-keys -l " renioice.sh ; export DISPLAY=:1 && sct \${night_light_temp:-2222}"
send-keys -l " cd video && nnntttrG"

new-window
select-pane -T"Mutt"
send-keys -l " renioice.sh ; export DISPLAY=:1 && sct \${night_light_temp:-2222}"
send-keys -l " mutt	"

new-window
select-pane -T"Lynx"
send-keys -l " renioice.sh ; export DISPLAY=:1 && sct \${night_light_temp:-2222}"
send-keys -l " lynx"

new-window
select-pane -T"Bash"
send-keys -l " renioice.sh ; export DISPLAY=:1 && sct \${night_light_temp:-2222}"

# Go "home"
select-window -t0
select-pane -tStandard:0.0

# vim:filetype=tmux
