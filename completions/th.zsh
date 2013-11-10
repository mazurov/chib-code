if [[ ! -o interactive ]]; then
    return
fi

compctl -K _th th

_th() {
  local word words completions
  read -cA words
  word="${words[2]}"

  if [ "${#words}" -eq 2 ]; then
    completions="$(th commands)"
  else
    completions="$(th completions "${word}")"
  fi

  reply=("${(ps:\n:)completions}")
}
