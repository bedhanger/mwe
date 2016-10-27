This represents the minimum working environment the author
requires to be fluent on any Unix-like system.

It does not contain tools as such, it provides clue to combine
some of them intelligently to be more efficient.

Cloning this repository into an otherwise empty home directory
is a good way to start, :-)

If the target directory is no longer empty, proceed as follows
[note that files/directories of the same name already present
*will* be overwritten]:

<code>
   $ cd /path/to/target/dir
</code>
<code>
   $ git init
</code>
<code>
   $ git remote add mwe https://github.com/bedhanger/mwe.git
</code>
<code>
   $ git fetch mwe
</code>
<code>
   $ git branch mwe-master --track remotes/mwe/master
</code>
<code>
   $ git checkout mwe-master
</code>

[If you can spare the master branch in /path/to/target/dir, the
commands can be simplified, use origin for the remote, etc.]

If your PATH settings don't contain ~/bin yet, remember to
either arrange for it manually, or simply open another
login shell.
