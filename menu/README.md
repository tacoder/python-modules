# python-modules
Collection of python modules

## curses_modules

### filtering_menu.py
Provides an ncurses based terminal menu that allowes you to seach through the menu through a search bar at the bottom: 
Run `python filtered_menu_example.py` like below
[![asciicast](https://asciinema.org/a/6ehKYQKBAs44sVN8cNoefutSw.png)](https://asciinema.org/a/6ehKYQKBAs44sVN8cNoefutSw)

### basic_menu.py
Basic ncurses based menu.
Run `python basic_menu_example.py`


### Installation / Setup 

Make sure you are using Python3

Install gitpython (required for git menus)
pip3 install gitpython

Sample aliases - 

alias gh="rm -f /tmp/menu_command.sh ; python3 generate_menu.py --type=folder --context=`pwd`; eval \`cat /tmp/menu_command.sh\` ; rm /tmp/menu_command.sh"
alias gb="rm -f /tmp/menu_command.sh ; python generate_menu.py --type=git_branch --context=\`pwd\` ; sh /tmp/menu_command.sh"
alias sshl="rm -f /tmp/menu_command.sh ; python generate_menu.py --type=ssh; sh /tmp/menu_command.sh"
alias sshe="rm -f /tmp/menu_command.sh ; python generate_menu.py --type=ssh_edit; sh /tmp/menu_command.sh"



The script puts the required command to be executed in /tmp/menu_command.sh, so it is necessary to call that script to execute the command, else it's just a menu display only.

TODO - create a bash function that can be called so the aliases are not polluted like above.
