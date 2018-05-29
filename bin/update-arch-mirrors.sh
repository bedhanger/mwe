#!/usr/bin/env bash

# Update the list of Arch Linux mirrors

[ "$UID" != 0 ] && su=sudo

if [ ${#} -eq 0 ]
then
	cat <<-EOM
		Please specify a country code...
	EOM
	exit 1
fi

country='"${1}"'
url="https://www.archlinux.org/mirrorlist/?country=$country&protocol=https&protocol=http&ip_version=4&use_mirror_status=on"

tmpfile=$(mktemp --suffix=-mirrorlist)

# Get latest mirror list and save to tmpfile
wget -qO- "$url" | perl -p -e 's/^#Server/Server/g;' > "$tmpfile"

# Backup and replace current mirrorlist file (if new file is non-zero)
if [ -s "$tmpfile" ]
then
  { echo " Backing up the original mirrorlist..."
    $su mv /etc/pacman.d/mirrorlist /etc/pacman.d/mirrorlist.orig; } &&
  { echo " Rotating the new list into place..."
    $su mv "$tmpfile" /etc/pacman.d/mirrorlist; } &&
  { echo " Removing pacman-introduced list..."
    $su rm -f /etc/pacman.d/mirrorlist.pacnew; }
else
  echo " Unable to update, could not download list."
fi

# allow global read access (required for non-root yaourt execution)
chmod +r /etc/pacman.d/mirrorlist
