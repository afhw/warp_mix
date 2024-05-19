import os
import random
import subprocess
import numpy as np
import time

WARP_EXE = "warp.exe"
IPV4_FILE = "ips-v4.txt"
IPV6_FILE = "ips-v6.txt"


def download_file(url, filename):
    """Downloads a file from the given URL."""
    subprocess.run(["powershell", "wget", "-Uri", url, "-OutFile", filename], check=True)


def ensure_files_exist():
    """Ensures that the necessary files are present."""
    if not os.path.exists(WARP_EXE):
        download_file(
            "https://gitlab.com/Misaka-blog/warp-script/-/raw/main/files/warp-yxip/warp.exe",
            WARP_EXE,
        )
    for ip_version in ["v4", "v6"]:
        filename = f"ips-{ip_version}.txt"
        if not os.path.exists(filename):
            download_file(
                f"https://gitlab.com/Misaka-blog/warp-script/-/raw/main/files/warp-yxip/{filename}",
                filename,
            )


def get_random_ipv4_cidr():
    """Generates a random IPv4 CIDR block."""
    return random.randint(0, 255)


def get_random_ipv6_cidr():
    """Generates a random IPv6 CIDR block."""
    hex_chars = "0123456789abcdef"
    cidr = ""
    for _ in range(8):
        cidr += random.choice(hex_chars)
        cidr += random.choice(hex_chars)
        if _ < 7:
            cidr += ":"
    return cidr


def generate_ip_list(ip_version):
    """Generates a list of IP addresses based on the given version."""
    filename = f"ips-{ip_version}.txt"
    ip_addresses = []
    n = 0
    with open(filename, "r") as f:
        for line in f:
            parts = line.strip().split(".")
            if ip_version == "v4":
                cidr = get_random_ipv4_cidr()
                ip_address = f"{parts[0]}.{parts[1]}.{parts[2]}.{cidr}"
            else:
                cidr = get_random_ipv6_cidr()
                ip_address = f"[{parts[0]}:{parts[1]}:{parts[2]}::{cidr}]"
            if ip_address not in ip_addresses:
                ip_addresses.append(ip_address)
                n += 1
            if n == 100:
                break
    return ip_addresses


def write_ip_list(ip_addresses):
    """Writes the given IP addresses to a file."""
    with open("ip.txt", "w") as f:
        for ip_address in ip_addresses:
            f.write(f"{ip_address}\n")


def main():
    """Main function."""
    ensure_files_exist()

    print("1. WARP IPv4 Endpoint IP 优选")
    print("2. WARP IPv6 Endpoint IP 优选")
    print("0. 退出")

    while True:
        choice = input("请输入选项: ")
        if choice in ["1", "2", "0"]:
            break
        print("无效选项，请重新输入。")

    if choice == "0":
        return

    ip_version = "v4" if choice == "1" else "v6"
    ip_addresses = generate_ip_list(ip_version)
    write_ip_list(ip_addresses)

    subprocess.run([WARP_EXE])
    time.sleep(0.1)
    ip = np.loadtxt(open("result.csv", "rb"), delimiter=",", dtype=str, skiprows=1, usecols=0)
    latency = np.loadtxt(open("result.csv", "rb"), delimiter=",", dtype=str, skiprows=1, usecols=2)
    print(ip[0])
    print(latency[0])
    os.remove("ip.txt")
    os.remove("result.csv")


if __name__ == "__main__":
    main()
