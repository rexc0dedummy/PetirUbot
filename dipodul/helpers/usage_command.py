print("install usage_command.py")
import json

from config import app, owner, owners

# Fungsi untuk membuat tombol inline query oleh bot
def update_command_usage(command):
    try:
        with open('command_usage.json', 'r') as file:
            command_data = json.load(file)
    except FileNotFoundError:
        command_data = {}

    if command in command_data:
        command_data[command] += 1
    else:
        command_data[command] = 1

    with open('command_usage.json', 'w') as file:
        json.dump(command_data, file, indent=4)

# Fungsi untuk mendapatkan jumlah penggunaan perintah
def get_command_usage(command):
    try:
        with open('command_usage.json', 'r') as file:
            command_data = json.load(file)
            return command_data.get(command, 0)
    except FileNotFoundError:
        return 0    