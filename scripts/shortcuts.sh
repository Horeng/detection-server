# Shortcuts for docker compose
alias dcup="docker compose --env-file .env up"
alias dcupf="docker compose --env-file .env --profile flower up"
alias dcupd="docker compose --env-file .env up -d"
alias dcupdf="docker compose --env-file .env --profile flower up -d"
alias upthis="dcupdf"

alias dcdown="docker compose down"
alias dcdownf="docker compose --profile flower down"
alias dcdownv="docker compose down -v"
alias dcdownvf="docker compose --profile flower down -v"
alias dcdown-all="docker compose down -v --remove-orphans"
alias downthis="dcdownvf"
