#!/bin/bash

echo "🔧 Starting project setup..."

# --- System dependencies ---
echo "📦 Installing system packages: ffmpeg, sox, jq, git"
brew install ffmpeg sox jq git

# --- Install pyenv (optional, for clean Python management) ---
if ! command -v pyenv &> /dev/null; then
  echo "📥 Installing pyenv..."
  brew install pyenv
  echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
  echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
  echo 'eval "$(pyenv init --path)"' >> ~/.zshrc
  echo 'eval "$(pyenv init -)"' >> ~/.zshrc
  source ~/.zshrc
fi

# --- Install Python with pyenv ---
if ! pyenv versions | grep -q "3.10.13"; then
  echo "🐍 Installing Python 3.10.13 via pyenv..."
  pyenv install 3.10.13
fi

pyenv global 3.10.13
eval "$(pyenv init -)"

# --- Python virtual environment ---
echo "📁 Creating virtual environment..."
rm -rf venv
python -m venv venv
source venv/bin/activate

# --- Install Python packages ---
echo "📚 Installing Python packages from requirements.txt..."
pip install --upgrade pip
pip install -r requirements.txt

# --- Done ---
echo "✅ Setup complete. Virtual environment is active."
deactivate