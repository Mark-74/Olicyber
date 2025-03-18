#!/bin/bash

echo "▄▄▄▄·  ▄▄▄· .▄▄ ·  ▄ .▄▪   ▐ ▄  ▄▄▄· ▄▄▄▄▄      ▄▄▄  
▐█ ▀█▪▐█ ▀█ ▐█ ▀. ██▪▐███ •█▌▐█▐█ ▀█ •██  ▪     ▀▄ █·
▐█▀▀█▄▄█▀▀█ ▄▀▀▀█▄██▀▐█▐█·▐█▐▐▌▄█▀▀█  ▐█.▪ ▄█▀▄ ▐▀▀▄ 
██▄▪▐█▐█ ▪▐▌▐█▄▪▐███▌▐▀▐█▌██▐█▌▐█ ▪▐▌ ▐█▌·▐█▌.▐▌▐█•█▌
·▀▀▀▀  ▀  ▀  ▀▀▀▀ ▀▀▀ ·▀▀▀▀▀ █▪ ▀  ▀  ▀▀▀  ▀█▄▀▪.▀  ▀"
echo "------------------------------------------------------"
echo -e "Welcome to our fabulous shell, this time with better security!\n"

filter() {
    cmd="$1"
    # all characters except for "l" and "s"
    blocklist=(
      'a' 'b' 'c' 'd' 'e' 'f' 'g' 'h' 'i' 'j' 'k' 'm' 'n' 'o' 'p' 'q' 'r' 't' 'u' 'v' 'w' 'x' 'y' 'z'
	  '0' '1' '2' '3' '4' '5' '6' '7' '8' '9'
    )
    
    for char in "${blocklist[@]}"; do
        if [[ "$cmd" == *"$char"* ]]; then
            exit 1
        fi
    done
    echo "$cmd"
}

while true; do
    echo -n "$(whoami)@$(hostname) $(pwd) $ "
    read -r cmd
    cmd=$(filter "$cmd")
    sh -c "$cmd"
done
