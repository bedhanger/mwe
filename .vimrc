""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Options for vim only.  The vi options are in .exrc
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Get the goodies for vi, i.e., merge .exrc and .vimrc
source $HOME/.exrc
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" General vim options.
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
syntax on
set modeline
set background=light
" let g:solarized_termcolors=256
" colorscheme solarized
set ruler
set textwidth=64
set tildeop
set notitle
set t_ti=
set t_te=
set smartindent
behave xterm
set comments+=:--\|,:--,:\":'
set formatoptions+=r2
filetype on
set viminfo=""
" TABs are evil (in most places).
set expandtab
" set fileformat=dos
set noswapfile
set splitbelow
set splitright
set mouse=a
set sidescroll=1
set scrollopt=ver,jump,hor
set fileencoding=utf-8
" Never...
set showtabline=0
" Stop counting, at least vertically...
set relativenumber
autocmd BufNewFile,BufRead *.ada,*.ADA,*.spc set filetype=ada
autocmd BufNewFile,BufRead config{,.{win,cyg}} set filetype=make
autocmd BufNewFile,BufRead *.mail,.vacation.msg,d,d.eads set filetype=mail
autocmd BufNewFile,BufRead bash-fc-* set filetype=sh
autocmd BufNewFile,BufRead changes.recent set filetype=diff
autocmd BufNewFile,BufRead *.qbquery,*.qbquery setfiletype sql
autocmd BufNewFile,BufRead /var/log/messages*,/tmp/*.messages silent %!~/perl/filter-messages
autocmd BufNewFile,BufRead /var/log/messages* $
autocmd BufNewFile,BufRead /var/log/messages* ?Seen
autocmd BufNewFile,BufRead /var/log/messages*,/tmp/*.messages let @/ = "Seen\\|DPT=\\d\\+\\|\\(Dropp\\|Accept\\|RST\\)ing\\|\\(\\d\\{1,3\\}\\.\\)\\{3\\}\\d\\{1,3\\}"
autocmd BufNewFile,BufRead /var/log/messages*,/tmp/*.messages set norelativenumber
autocmd BufNewFile,BufRead /tmp/*.messages set filetype=messages
autocmd StdinReadPost * map q :quit!<CR>
" Strange, <buffer=abuf> instead of * doesn't seem to work
" (would be nice, as we could then forget about CmdwinLeave).
autocmd CmdwinEnter unmap <CR>
" autocmd CmdwinLeave * map <CR> :wall<CR>+
" autocmd FileType mail set tabstop=8
" This one's local by virtue of textwidth's being local to the buffer.
autocmd CmdwinEnter set formatoption=
autocmd CmdwinEnter set textwidth=0
let loaded_explorer=1
" let loaded_netrw=1
let loaded_rrhelper=1
" Make the current browsing dir the current Vim dir.
let g:netrw_keepdir=0
" Highlight matches...
set hlsearch
" ...and use that feature to help you spot trailing blanks.  The
" first search for something other than these, however, destroys
" that again.
let @/ = "\\s\\+$"
" Automatically read the file again if Vim detects it's been
" changed outside of Vim.
set autoread
" Spelings.
set spellfile=~/my.spelling.en.add
setlocal spell spelllang=en
" Make the indications less "noisy".
highlight SpellBad term=inverse cterm=underline ctermbg=none
highlight SpellCap term=inverse cterm=underline ctermbg=none
" Use pipes, not files for commands launched from the editor.
set noshelltemp
" There *is* only one type.
set shellslash
" The size (height) of the command line window.
set cmdwinheight=3
" F11: toggle paste mode
set pastetoggle=<F11>
" This makes copy and paste easier.
set clipboard=unnamed
" Have the full ASCII range as printable.
set isprint=@,~-255
" Ease opening a file whose name is under the cursor.
set isfname+={,},[,],:,@-@,!,\
" This makes editing in visual mode more consistent.
set virtualedit=all
" For vertical alignment.
set cursorcolumn
set colorcolumn=+0
" Custom listing for netrw browser.
let g:netrw_liststyle=1
let g:netrw_timefmt='%Y-%m-%dT%H:%M:%S'
" The font to be used when creating HTML.
let html_font="Bitstream Vera Sans Mono"
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Key mappings for command mode.
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Redefine Z, taking multiple buffers/windows into account.
noremap <silent> Z :quitall!<CR>
" Release all buffers
noremap <silent> <C-W><C-W> :silent! only<CR>:silent bufdo! bwipeout!<CR>
" TAB jumps into the next window.
map <TAB> w
" Unmap `#' to have it available for backward searching of the
" word under the cursor.
unmap #
" Window resizing.
map <C-Left> <C-W>>
map <C-Right> <C-W><
map <C-Down> <C-W>+
map <C-Up> <C-W>-
" Tags.
map  ]
set tags+=~/tags
" Center the text found after pressing n/N (redefinition w/o
" marks, since Vim has zz).
" map n /zz
" map N ?zz
noremap n nzz
noremap N Nzz
" Remap the RETURN key to take all changed buffers into account.
" Needs to be unmapped/remapped when entering/leaving the
" command-line window.
noremap <silent> <CR> :wall!<CR>
" Leaves the cursor in place after a repetition command.
map . .`[
" Map  to go back one file.
map  :previous<CR>
" Goto file under cursor in a new window.
" map gf :split <cfile><CR> Use CTRL-W_CTRL-F to do this.
" Use full vim functionality on command and search lines.
" noremap : q:i
" noremap / q/i
" noremap ? q?i
" Del empties the file.
map <Del> :%d<CR>
" Simple screen locker...
map <silent> <C-C> :silent! windo set invrightleft<CR>
" Gimme a new window.
map <C-W><CR> :new<CR>
map <C-W>V :vnew<CR>
" Discard buffer...
map <C-W>c :bwipeout!<CR>
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Key mappings in insert mode.
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Make TAB work like in bash.
imap <TAB> 
if &diff
   syntax off
endif
source $HOME/.umlauts
