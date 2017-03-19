[ -f ${HOME}/.bashrc ] && source ${HOME}/.bashrc

SSH_ENV="${HOME}/.ssh/environment"

function start_ssh_agent {

   echo "Initialising new SSH agent..."

   ssh-agent | sed 's/^echo/# echo/' > "${SSH_ENV}"

   chmod 600 "${SSH_ENV}"

   source "${SSH_ENV}" > /dev/null

   ssh-add ${HOME}/.ssh/{bra_id_ecdsa,ket_id_rsa,rsjlaa_id_ecdsa}

}

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

# [ -z "$(which fortune cowsay)" ] || (echo; fortune | cowsay; echo)

SAYS="ponythink ponysay"

[ -z "$(which ${SAYS})" ] || \
   (echo; python3 $(which $(shuf --echo --head-count=1 ${SAYS})) < <(fortune); echo)

function wcd()
{

   # Prepare wcd to be a drop-in replacement for cd (the call to
   # perl prevents infinite recursion).

   go="${WCDHOME:-${HOME}}/bin/wcd.go" && \
   command rm -f "$go" && \
   command wcd --ignore-case "$@" && \
   command perl -pi -e 's/\s*(cd)/builtin $1/;' $go && \
   [ -f "$go" -a -r "$go" ] && source "$go" && \
   unset go

}

# [ -f ${HOME}/git-completion.bash ] && source ${HOME}/git-completion.bash
# if [ -f ${HOME}/git-prompt.sh ]
# then
#
#    source ${HOME}/git-prompt.sh
#    export GIT_PS1_SHOWDIRTYSTATE=1
#    export PS1='$(__git_ps1 "(%s)") \$ '
#
# fi
