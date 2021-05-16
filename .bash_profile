[ -f ${HOME}/.bashrc ] && source ${HOME}/.bashrc

SSH_ENV="${HOME}/.ssh/environment"

function start_ssh_agent {

   echo "Initialising new SSH agent..."

   ssh-agent | sed 's/^echo/# echo/' > "${SSH_ENV}"

   chmod 600 "${SSH_ENV}"

   source "${SSH_ENV}" > /dev/null

   ssh-add ${HOME}/.ssh/{bra_id_ecdsa,ket_id_rsa,rsjlaa_id_ecdsa,github_id_ed25519}

}

function keez
{
	if [ -f "${SSH_ENV}" ]
	then
		HAVE_SSH_AGENT=false
		unset SSH_AGENT_PID

		source "${SSH_ENV}" > /dev/null

		for PID in $(pidof ssh-agent)
		do
			# Now check that
			# (1) SSH_AGENT_PID is a ssh-agent
			# (2) it is a process of yours
			# (3) it is not the gnome session ssh-agent
			if [ ${SSH_AGENT_PID} -eq ${PID} ] && \
				[ "$(stat --printf '%U' /proc/${PID})" = "${USER}" ] && \
				! grep --quiet 'gnome-session' /proc/${PID}/cmdline
			then
				HAVE_SSH_AGENT=true
				break
			fi
		done

		${HAVE_SSH_AGENT} || start_ssh_agent
	else
		start_ssh_agent
	fi
}

SAYS="{shuf,cat,tac,{cow,pony}{think,say}}" && SAYS="$(eval echo ${SAYS})"
[ -z "$(which ${SAYS})" ] || \
   (echo; $(which $(shuf --echo --head-count=1 ${SAYS})) < <(fortune); echo)
