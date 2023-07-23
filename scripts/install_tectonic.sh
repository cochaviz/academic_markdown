#!/usr/bin/env bash
#
# For a more expansive explanation and other options: 
# https://tectonic-typesetting.github.io/en-US/install.html
#
# This will only download the executable, please move it to /usr/bin/ or any
# other folder in the PATH variable if the .local/bin is not found.
#

PREAMBLE="academic_markdown (install_tectonic.sh):"

curl --proto '=https' --tlsv1.2 -fsSL https://drop-sh.fullyjustified.net | sh

if [[ ":$PATH:" == *":$HOME/.local/bin:"* ]]; then
  echo "$PREAMBLE Found local bin folder. Moving tectonic there!"
  mv tectonic "$HOME/.local/bin/"
else
    echo "$PREAMBLE Your path is missing $HOME/.local/bin"
    echo "Move tectonic from this folder to any of the following (consider /usr/bin):"
    echo "$PATH"
fi

