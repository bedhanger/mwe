new-session -s"Standard"

	select-pane -T"Network Connexions"
		send-keys " renioice.sh ; export DISPLAY=:1" C-m
		send-keys " watch-netz.sh" C-m

	split-window -v
		select-pane -TIrssi
		send-keys " renioice.sh ; export DISPLAY=:1" C-m
		send-keys " e irssi" C-m

	new-window
		select-pane -T"System"
		send-keys " renioice.sh ; export DISPLAY=:1" C-m

	new-window
		select-pane -T"Gucke"
		send-keys " renioice.sh ; export DISPLAY=:1" C-m
		send-keys " cd ~/video && nnn" C-m "tttrG"

	new-window
		select-pane -T"Mutt"
		send-keys " renioice.sh ; export DISPLAY=:1" C-m
		send-keys " mutt" C-m Tab

	new-window
		select-pane -T"Lynx"
		send-keys " renioice.sh ; export DISPLAY=:1" C-m
		send-keys " lynx -book" C-m

	new-window
		select-pane -T"Bash"
		send-keys " renioice.sh ; export DISPLAY=:1" C-m

	new-window
		select-pane -T"Bash"
		send-keys " renioice.sh ; export DISPLAY=:1" C-m

	new-window
		select-pane -T"Bash"
		send-keys " renioice.sh ; export DISPLAY=:1" C-m

	new-window
		select-pane -T"Bash"
		send-keys " renioice.sh ; export DISPLAY=:1" C-m

	new-window
		select-pane -T"HTop"
		send-keys " renioice.sh ; export DISPLAY=:1" C-m
		send-keys " htop" C-m

		split-window -v
			select-pane -TCgTop
			send-keys " renioice.sh ; export DISPLAY=:1" C-m
			send-keys " systemd-cgtop -d5" C-m

		split-window -h
			select-pane -TTempz
			send-keys " renioice.sh ; export DISPLAY=:1" C-m
			send-keys " TERM=vt100 watch --no-title --differences --interval=4 'frex | tail -6'" C-m

		split-window -v
			select-pane -TBash
			send-keys " renioice.sh ; export DISPLAY=:1" C-m
			send-keys " e" C-m

		# Go to the htop pane
		select-pane -tStandard:9.0

		split-window -v
			select-pane -T"Emerge et al."
			send-keys " renioice.sh ; export DISPLAY=:1" C-m

# Go "home" to the first pane that wants input
select-window -t0
select-pane -tStandard:0.1

# vim:filetype=tmux
