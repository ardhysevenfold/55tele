from telethon import TelegramClient, events
import requests
import json
import time
import asyncio
import random
import datetime
from colorama import init, Fore, Style

# Masukkan API ID dan API Hash yang Anda dapatkan
api_id = '25678646'  # Ganti dengan API ID Anda
api_hash = 'f6f5a45709a24ce8b78b651536918be2'  # Ganti dengan API Hash Anda
phone_number = '+6285796297189'  # Ganti dengan nomor telepon Anda

# Inisialisasi warna untuk CMD
init(autoreset=True)

# Menyimpan riwayat game dengan batas 25
history = []

# Membuat klien Telegram
client = TelegramClient('session_name', api_id, api_hash)

# Fungsi untuk mendapatkan timestamp
def get_timestamp():
    return int(time.time())

# Fungsi untuk mendapatkan data dari GetNoaverageEmerdList
def response_GetNoaverageEmerdList():
    headers = {
        'authority': 'newapi.55lottertttapi.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9,id-ID;q=0.8,id;q=0.7',
        'authorization': 'Bearer YOUR_API_TOKEN',  # Ganti dengan token API Anda
        'content-type': 'application/json; charset=UTF-8',
        'origin': 'https://www.551bk.com',
        'referer': 'https://www.551bk.com/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
    }
    data = json.dumps({
        "pageSize": 10,
        "pageNo": 1,
        "typeId": 30,
        "language": 0,
        "random": "b631eb26bac6403e99093913e5bb48c5",
        "signature": "A6203E85132E5FE26B5F43DDF1ECDD07",
        "timestamp": get_timestamp()
    })
    response = requests.post('https://newapi.55lottertttapi.com/api/webapi/GetNoaverageEmerdList', headers=headers, data=data)
    return response.json()

# Fungsi untuk mendapatkan data dari GetGameIssue
def response_GetGameIssue():
    headers = {
        'authority': 'newapi.55lottertttapi.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9,id-ID;q=0.8,id;q=0.7',
        'authorization': 'Bearer YOUR_API_TOKEN',  # Ganti dengan token API Anda
        'content-type': 'application/json; charset=UTF-8',
        'origin': 'https://www.551bk.com',
        'referer': 'https://www.551bk.com/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
    }
    data = json.dumps({
        "typeId": 30,
        "language": 0,
        "random": "166b81d9568e4123a83a2c7fdb80b7d9",
        "signature": "5DB43C344C7381B72B5262FFB3572444",
        "timestamp": get_timestamp()
    })
    response = requests.post('https://newapi.55lottertttapi.com/api/webapi/GetGameIssue', headers=headers, data=data)
    return response.json()

# Fungsi untuk menghitung taruhan dan logika prediksi
def calculate_bet(last_bet, bet_index, is_loss):
    bets = [1000, 3000, 6000, 16000, 32000, 80000, 160000, 350000, 800000, 1700000, 4000000, 8000000, 18000000, 50000000]  # Array taruhan
    
    if is_loss:
        bet_index += 1  # Naikkan indeks jika kalah
    else:
        bet_index = 0  # Reset ke awal jika menang

    if bet_index >= len(bets):
        bet_index = len(bets) - 1  # Batasi jika indeks terlalu besar

    next_bet = bets[bet_index]
    return next_bet, bet_index

# Fungsi untuk menentukan jenis taruhan (kecil/besar)
def determine_bet(number):
    return "BESAR" if int(number) >= 5 else "KECIL"

# Fungsi utama untuk mendapatkan data dan mengirim prediksi
async def main():
    current_balance = 100000  # Saldo awal
    profit_balance = 0
    last_bet = 1000
    bet_index = 0
    is_loss = False
    current_bet = 1000
    previous_bet = 0
    next_bet_type = ["BESAR", "KECIL", "BESAR", "KECIL", "BESAR", "BESAR", "KECIL", "KECIL", "BESAR", "KECIL", "BESAR", "BESAR", "KECIL", "KECIL", "BESAR", "BESAR", "KECIL", "KECIL", "BESAR", "KECIL"][random.randint(0, 19)]  # Set jenis taruhan pertama secara acak

    print(Fore.YELLOW + r"""
 ███████ ███    ███  █████  ███    ██ 
 ██      ████  ████ ██   ██ ████   ██ 
 █████   ██ ████ ██ ███████ ██ ██  ██ 
 ██      ██  ██  ██ ██   ██ ██  ██ ██ 
 ███████ ██      ██ ██   ██ ██   ████
    """)
    
    history.clear()

    while True:
        print("Mendapatkan data GetNoaverageEmerdList...")
        data1 = response_GetNoaverageEmerdList()

        print("Mendapatkan data GetGameIssue...")
        data2 = response_GetGameIssue()

        latest_game = data1['data']['list'][0]
        issue_number = latest_game['issueNumber']
        number = latest_game['number']

        if next_bet_type == "BESAR":
            if int(number) >= 5:
                is_loss = False
                result = "WIN"
                result_emoji = "✅"
                result_color = Fore.GREEN
                current_balance += current_bet
            else:
                is_loss = True
                result = "MIN"
                result_emoji = "❌"
                result_color = Fore.RED
                current_balance -= current_bet
        else:
            if int(number) < 5:
                is_loss = False
                result = "WIN"
                result_emoji = "✅"
                result_color = Fore.GREEN
                current_balance += current_bet
            else:
                is_loss = True
                result = "MIN"
                result_emoji = "❌"
                result_color = Fore.RED
                current_balance -= current_bet

        previous_bet = current_bet
        current_bet, bet_index = calculate_bet(last_bet, bet_index, is_loss)
        last_bet = current_bet

        period_last4 = issue_number[-4:]
        history.append(f"{period_last4:<4} │ {number:<4} │ ({next_bet_type[0]}){previous_bet:<6} │ {result}{result_emoji}")
        if len(history) > 25:
            history.pop(0)

        next_issue_number = data2['data']['issueNumber']
        next_bet_type = determine_bet(random.randint(0, 9))

        prediction_message = "📍55FIVE 1M📍\n"
        history_message = "┌────────┬─────┬─────────┬─────┐\n"
        history_message += "│ Perio  │ Data│ Betting │ L/W │\n"
        history_message += "├────────┼─────┼─────────┼─────┤\n"
        for record in history:
            history_message += f"│ {record} │\n"
        history_message += "└────────┴─────┴─────────┴─────┘\n"
        
        prediction_message += f"DAFTAR https://551bk.com/#/register?invitationCode=sbJnv4801\n"
        prediction_message += f"📶 Prediksi {next_issue_number[-4:]} {next_bet_type}\n"
        prediction_message += f"♻️ Taruhan: {current_bet} \n"
        prediction_message += f"💰 Saldo: {current_balance}\n"
    
        full_message = f"{history_message}\n{prediction_message}"

        # Menampilkan hasil di layar
        print(Fore.YELLOW + r"""
  _____ _____  __      ___  __
 | ____| ____| \ \    / (_)/ _|
 | |__ | |__    \ \  / / _| |_ ___
 |___ \|___ \    \ \/ / | |  _/ _ \
  ___) |___) |    \  /  | | ||  __/
 |____/|____/      \/   |_|_| \___|
    """)
        print("\n" + Fore.YELLOW + "Riwayat 55FIVE WINGO 1M:")
        print(Fore.GREEN + history_message)
        print(Fore.CYAN + prediction_message)

        # Countdown untuk update data selanjutnya
        time.sleep(30)

# Menjalankan fungsi utama
async def run():
    await client.start(phone_number)
    await main()

loop = asyncio.get_event_loop()
loop.run_until_complete(run())
