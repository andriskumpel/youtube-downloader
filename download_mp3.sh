#!/bin/bash

# Script to download YouTube audio as MP3 using yt-dlp within the project's virtual environment.

# Check if a URL argument is provided
if [ -z "$1" ]; then
  echo "Uso: ./download_mp3.sh <URL_DO_YOUTUBE>"
  exit 1
fi

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Define the path to the virtual environment
VENV_PATH="$SCRIPT_DIR/.venv"

# Check if the activation script exists
if [ ! -f "$VENV_PATH/bin/activate" ]; then
  echo "Erro: Ambiente virtual (.venv) não encontrado em $SCRIPT_DIR"
  echo "Por favor, crie o ambiente primeiro com: python3 -m venv .venv"
  exit 1
fi

# Activate the virtual environment
source "$VENV_PATH/bin/activate"

# Run yt-dlp with the provided URL
echo "Baixando e convertendo para MP3..."
yt-dlp -x --audio-format mp3 "$1"

# Deactivate the virtual environment (optional, script will exit anyway)
# deactivate

echo "Download concluído."

