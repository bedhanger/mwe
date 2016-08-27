""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Options for gvim only.  The vi options are in .exrc, the ones
" for vim are in .vimrc
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Get the goodies for vim, i.e., merge .vimrc and .gvimrc
source $HOME/.vimrc
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" General vim options.
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" The GUI font to be used.
" set guifont=Lucida_Console:h18
" set guifont=Lucida_Console:h22:b:cANSI
set guifont=DejaVu\ Sans\ Mono\ 14
" Display the title in the topmost bar.
set title
set titlestring=EDITORE
" Maximise the GUI window.
" autocmd GUIEnter * simalt ~x
" CTRL-A transfers the whole buffer into the clipboard.
" Redefinition, as GVim doesn't know about /dev/clipboard, but
" the + register is suitable for that.
map <C-A> :%yank +<CR>
" Insert key inserts clipboard contents.  Again, a redefinition.
map <Insert> "+P
" Map backspace properly.
map <BS> X
highlight Normal guibg=wheat2
