#!/bin/bash

# Инициализация репозитория и суб-модулей
git clone https://github.com/QuoNaro/kgtt-bot.git
cd kgtt-bot
git submodule init && git submodule update

# Создание виртуального окружения
sudo python3 -m virtualenv virtualenv
source virtualenv/bin/activate.fish

# Развертнывание командной оболочки бота
sudo python3 -m pip install -r requirements.txt
# pyinstaller --onefile bin/botmgmt.py

mkdir ~/bin
cp bin/botmgmt.py ~/bin/botmgmt
chmod +x ~/bin/botmgmt
echo "export PATH='$PATH:$HOME/bin'" >> ~/.bashrc
source ~/.bashrc