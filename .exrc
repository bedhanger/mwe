""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Options for vi only.  See .vimrc for vim's options.
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" General Options.
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
set autoindent
set ignorecase
set showmode
set showmatch
set shiftwidth=3
set nowrapscan
set autowrite
set wrapmargin=15
set shell=bash
set showcmd
" The tabstop setting discourages vi from inserting TABs when
" you use  repetitively; it makes, however, files that do
" contain TABs look funny.  The lesson to be learnt from that:
" do not use TABs in your text files.
" set tabstop=80
" This is useful for counting the occurrences of a regex in a
" file: %s/regex/&/g does the trick.
set report=0
" Read ./.exrc
set exrc
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Key Mappings for Command Mode.
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Backspace
map  X
" Delete
map [3~ x
" Control Indentation, CTRL-T advances one level, CTRL-D
" steps back.
map  >}
map  <}
" vi can't handle NUL characters, and DEC's vi doesn't even
" support mapping in EXINIT.  We thus can't define CTRL-D.  You
" can do it from within vi, though.
" Transpose the word under the cursor (A) with the next one (B).
" Doesn't work if:
"    * A or B is the last word on the line, or
"    * B is followed by a punctuation symbol, bracket, pipe,
"      etc.
map K lbdWWPb
" Insert a blank a line: cursor-down goes downwards, cursor-up
" upwards.
map OB o+
map OA O-
" Map the rest of the cursor keys to something useful.
map OC 2l
map OD 2h
" Duplicate the current paragraph: upwards or downwards, plus
" insert an empty line.
map =k {y}P
map =j {y}}P
" Copy the current paragraph.
map = {y}
" Delete the current paragraph (keep in in the unnamed
" register).
map =d {d}
" Join the lines of the current paragraph.
map =J {!}join<CR>
" Ways of quitting a buffer/file, leaving it untouched.
map Z :quit!<CR>
" Make the single quote work like a backtick.
map ' `
" Pressing `#' displays the current line number.
map # :number<CR>
" F1 untaints the file.
map <F1> m':silent source $HOME/.untaint_file<CR>''
" F2 comments/uncomments a paragraph.
map <F2> {!}exec comment_ada_uncomment<CR>}w
" F3 creates a paragraph with lines of a certain length
" map <F3> :w<CR>{w^}b$:silent '`,.!exec fmt -42 -c -u \| $HOME/bin/nroffify \| nroff<CR>
map <F3> {!}exec par -j -w 64 g1<CR>
" F4 inserts a marker at the beginning of every line of a paragraph
map <F4> {!}exec $HOME/bin/reply<CR>
" F5 removes the marker
map <F5> {!}exec $HOME/bin/unreply<CR>
" F6 signs a message with GNU PG
map <F6> :w<CR>:.,$!exec gpg 2> /dev/tty --clearsign<CR>
" F7 encrypts a message with GNU PG
map <F7> :w<CR>:.,$!exec gpg 2> /dev/tty --encrypt
" F8 encrypts & signs a message with GNU PG
map <F8> :w<CR>:.,$!exec gpg 2> /dev/tty --encrypt --sign
" F9 decrypts/verifies a message
map <F9> :w<CR>!2}exec gpg 2> /dev/tty<CR>
" LaTeX the current file.
map <F12> :!time (latex % && latex %)<CR>
" CTRL-N loads the next file, CTRL-P rewinds the arg list
map  :next<CR>
map  :rewind<CR>
" Make the current file writable.
map w :!chmod +w %<CR>
" Make the current file executable.
map x :!chmod +x %<CR>
" Let the space char do the same.
map   OAjjOB--
" CTRL-U puts the current line in UPPER CASE.
map  :.!exec tr [:lower:] [:upper:]<CR>
" Center the text found after pressing n/N.
map n /mmz.'m
map N ?mmz.'m
" Break a long line.
map  063lbi>>
map  061lbi" &"
" Pressing RETURN will save the current buffer.
map  :w
" CTRL-A transfers the whole buffer into the clipboard.  It also
" removes the EOL from the last line.  This is done in order to
" replicate the mouse selection technique of including or
" excluding the final EOL.  You can get the final EOL into the
" clipboard by simply pressing <Return> (provided that the
" clipboard is the current buffer.
map  :silent! %!~/bin/noeol.pl \| p; g
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Key Mappings in Insert Mode.
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Comments on the fly.
map! =-- I-- A
" map! =" I" A
map! =%% I%% A
" CTRL-Z suspends the editor and saves the file if autowrite is
" set.
map!  :stop<CR>
" F2 inserts my favourite reply line.
map! OQ 0iUpon , ye spake unto me thuswise, saying:2F,i
" With or without you.
map! w/ with
map! w/o without
" Scotland!
map! o/w outwith
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Abbreviations and Speling Corrections.
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
abbreviate FLASE FALSE
abbreviate calulate calculate
" ;-)
abbreviate desgin design
abbreviate edi Edinburgh
abbreviate exc exception
abbreviate fov -- For operator visibility.o
abbreviate func function
abbreviate pac package
abbreviate proc procedure
abbreviate prc procedure
abbreviate retrun return
abbreviate shoudl should
abbreviate teh the
abbreviate woudl would
abbreviate perfrom perform
abbreviate wi Whitespace issues
abbreviate wrt with respect to
abbreviate btw between
abbreviate BTW by the way
abbreviate ie i.e.,
abbreviate eg e.g.,
abbreviate returnl return;
abbreviate fro for
abbreviate ofr for
abbreviate Regrads Regards
abbreviate taks task
abbreviate buidl build
abbreviate slef self
abbreviate misc miscellaneous
abbreviate wiht with
abbreviate ipl implement
abbreviate thier their
abbreviate bzgl bezueglich
abbreviate waht what
abbreviate udn und
abbreviate rqt requirement
abbreviate prio priority
abbreviate duering during
abbreviate acuh auch
abbreviate dont don't
abbreviate Dnake Danke
abbreviate dnake danke
abbreviate agrument argument
abbreviate sth something
abbreviate sm1 someone
abbreviate aka also known as
abbreviate oi open issue
abbreviate og of
abbreviate soe someone
abbreviate repo repository
abbreviate thet that
abbreviate provate private
