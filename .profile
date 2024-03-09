# This inserts a thousands separator into the sizes displayed by
# ls, du, and df.  It is dependent upon LC_NUMERIC, but there
# appears to be none which features "_", :-(
export LS_BLOCK_SIZE="'1"
export DU_BLOCK_SIZE="'1024"
export DF_BLOCK_SIZE="'1024"

# Some useful aliases.  More are scattered throughout the file.

# eza vs. ls and their derivatives
eval eza=eza

which ${eza} >/dev/null 2>&1
if [ ${?} -ne 0 ]
then
	eza='ls -la --color=auto --time-style="+%Y-%m-%dT%H:%M:%S"'
	alias lt="${eza} --sort=time --reverse"
	alias lth="lt --human-readable"
else
	eza='eza \
		--all \
		--color=auto \
		--colour-scale \
		--git \
		--git-repos \
		--group \
		--header \
		--icons=automatic \
		--links \
		--long \
		--smart-group \
		--time-style=+%Y-%m-%dT%H:%M:%S \
'
	alias lt="${eza} --sort=time"
	alias lth="lt"
fi
alias l="${eza}"

alias ,="pwd | tr \\\n \\\000 | xargs --null ${l} --directory"
alias ,,="(cd .. && pwd) | tr \\\n \\\000 | xargs --null ${l} --directory"

alias cls='clear'

alias which='type -p'

alias pu="pushd > /dev/null"

alias po="popd > /dev/null"

alias less="view -c 'set nomod nolist ts=8 wrap nospell noreadonly' -"

alias more=less

alias j=jobs

alias ..="cd .. && pwd && lt"

# Primary prompt.

export PS1='\h \! $ '

# Secondary prompt.

export PS2='? '

# Default permission for files.

umask 022

# Variables.

export IGNOREEOF=1000

# export PATH=/usr/local/bin:/bin:/usr/bin

export PATH=~/bin:${PATH}

# Now we can define this one.

export EDITOR=vi

export EDITORE=${EDITOR}

export VISUAL=${EDITOR}

export DIFFPAGER=~/perl/pager.pl

export SYSTEMD_PAGER=cat
export GIT_PAGER=cat

# export MANPAGER="col -b | ${DIFFPAGER}"

export PAGER=${DIFFPAGER}

export MANPAGER=less

# export MANPATH=/usr/man:/usr/local/man:/usr/X11R6/man

# export LESS="-#1MISgP?f%f:stdin. %lt?L/%L lines. ?B%B bytes. ?m%i/%m files. ?xnext\: %x:%t (LAST FILE). ?e(END):?p%pt\%.%t"

# This one allows cursor positioning with the mouse,
# putty-256color don't.

export TERM=screen-256color

# export TERM=putty-256color

LS_COLORS='no=00:fi=00:di=00;31:ln=01;36:pi=40;37:so=01;35:bd=40;33;01:cd=40;33;01:or=40;31;01:ex=01;34:*.tar=01;31:*.tgz=01;31:*.arj=01;31:*.taz=01;31:*.lzh=01;31:*.zip=01;31:*.z=01;31:*.Z=01;31:*.gz=01;31:*.bz2=01;31:*.deb=01;31:*.rpm=01;31:*.jpg=01;35:*.png=01;35:*.gif=01;35:*.bmp=01;35:*.ppm=01;35:*.tga=01;35:*.xbm=01;35:*.xpm=01;35:*.tif=01;35:*.png=01;35:*.mpg=01;35:*.ts=01;35:*.avi=01;35:*.fli=01;35:*.gl=01;35:*.dl=01;35:*.tex=01;35:*.mail=04:*.asc=07:*.ini=04'

export LS_COLORS

# Report job status immediately.

# set -b

# In the absence of a ~/.inputrc saying 'set editing-mode vi',
# this will make you feel at home even on the command line, :-)

set -o vi

export SHELL=/bin/bash

export HISTSIZE=5000

export FCEDIT='/bin/vi -c "set paste|read ~/commands.txt"'

export FILE_TYPES_TO_GREP="{ada,c,h,make,bld,gpj,sh,{a,e,r,s,u}df,p{l,m}}"

export HISTIGNORE="&:[lj]u[tb]:.:..:-:w:ps:df:make:l[tsh]:[bf]g:exit:logout:frex:pwd:vifm:j:e"

# stty cols 80

export WTFPATH="~/.wtf:/usr/share/wtf"

# Regex for dealing with various line endings.

export EOL="($|\r|\r\n|\n|\n\r)"

export eol=${EOL}

# Rough approximation of an IPv4 address.

export IPV4_ADDR='(?:\d{1,3}\.){3}\d{1,3}'

export GREP_COLORS="ms=43;30:mc=43;30:sl=:cx=:fn=35:ln=32:bn=34:se=36"

export PCREGREP_COLOR=${GREP_COLOR}

# Shows sizes in human-readable form.

alias lh="l --sort=size --human-readable --reverse"

# Use this as a Perl-like regex to find not only duplicates but
# multiplicates.

export MULTIPLICATES="(\b\w+\b)(\s+\b\1\b)+"

alias nd="source $(which nd)"
alias nd.="ND_ROOT=. nd"

alias ng="nd && gitify"

alias rd="source $(which rd)"
alias rd.="ND=. rd"

alias rde="rd && exit"

alias ns="nd && gnome-open ."
alias ns="nd. && gnome-open ."

export PARINIT='rTbgqR B=.,?_A_a Q=_s>|'

export LANG='en_GB.UTF-8'

export LC_ALL='en_GB.UTF-8'

alias k=l

alias es="tmux"

alias tma="tmux attach"

alias tme="tma ; exit"

# light-term

# This should be the default!!!

set -o pipefail

# Check the window size after each command and, if necessary,
# update the values of LINES and COLUMNS.

shopt -s checkwinsize

# This makes sar display the date right.

export S_TIME_FORMAT=ISO

# Easy, pal...

alias ic3='ionice -c 3'

alias kw='date +"%V"'

export ISO_8601_DATE_TIME="%Y-%m-%dT%H:%M:%S"

export HISTTIMEFORMAT="%a ${ISO_8601_DATE_TIME} "

export HISTCONTROL="ignorespace:ignoredups:erasedups"

export GPG_TTY=$(tty)

source ${HOME}/proxy-settings

alias git=hub
alias gti=hub

alias -- -='cd -'

export MTR_OPTIONS="--order="SDLNAV"  --interval=13"
