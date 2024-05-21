new-session -s"Standard"

	select-pane -T"Network Connexions"
		send-keys " renioice.sh ; export DISPLAY=:1 && sct \${night_light_temp:-2222}" C-m
		send-keys " watch-netz.sh" C-m

	split-window -v
		select-pane -TIrssi
		send-keys " renioice.sh ; export DISPLAY=:1 && sct \${night_light_temp:-2222}" C-m
		send-keys " e irssi" C-m

	new-window
		select-pane -T"Emerge et al."
		send-keys " renioice.sh ; export DISPLAY=:1 && sct \${night_light_temp:-2222}" C-m

	new-window
		select-pane -T"Gucke"
		send-keys " renioice.sh ; export DISPLAY=:1 && sct \${night_light_temp:-2222}" C-m
		send-keys " cd ~/video && nnn" C-m "tttrG"

	new-window
		select-pane -T"Mutt"
		send-keys " renioice.sh ; export DISPLAY=:1 && sct \${night_light_temp:-2222}" C-m
		send-keys " mutt" C-m Tab

	new-window
		select-pane -T"Lynx"
		send-keys " renioice.sh ; export DISPLAY=:1 && sct \${night_light_temp:-2222}" C-m
		send-keys " lynx -book" C-m

	new-window
		select-pane -T"Bash"
		send-keys " renioice.sh ; export DISPLAY=:1 && sct \${night_light_temp:-2222}" C-m

# Go "home" to the first pane that wants input
select-window -t0
select-pane -tStandard:0.1

# vim:filetype=tmux
