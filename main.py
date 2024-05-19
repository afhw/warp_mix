import requests
import json
import os
import random
import subprocess
import time
import numpy as np

WARP_EXE = "warp.exe"
IPV4_FILE = "ips-v4.txt"
IPV6_FILE = "ips-v6.txt"


def download_file(url, filename):  # 补全文件
    subprocess.run(["powershell", "wget", "-Uri", url, "-OutFile", filename], check=True)


def ensure_files_exist():
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
    return random.randint(0, 255)


def get_random_ipv6_cidr():
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


def speed():
    """Main function."""
    ensure_files_exist()

    ip_version = "v4"
    ip_addresses = generate_ip_list(ip_version)
    write_ip_list(ip_addresses)

    subprocess.run([WARP_EXE])
    time.sleep(0.1)
    ip = np.loadtxt(open("result.csv", "rb"), delimiter=",", dtype=str, skiprows=1, usecols=0)
    latency = np.loadtxt(open("result.csv", "rb"), delimiter=",", dtype=str, skiprows=1, usecols=2)
    # print(ip[0])
    # print(latency[0])
    os.remove("ip.txt")
    os.remove("result.csv")
    return [ip[0], latency[0]]


def getkey():
    ppkeys = requests.get('https://warp.halu.lu/')  # 还是大佬项目香！
    pkeys = ppkeys.content.decode('UTF8')
    new_data = json.loads(pkeys)
    # print(new_data)
    # print(new_data["key"])
    data = new_data["key"]
    # print(data)
    return data


def main():
    key = getkey()
    print(key)
    speed_event = speed()
    print(speed_event)
    subprocess.run(["warp_wg.exe", key])
    with open("wgcf-profile.conf", "a") as f:
        f.writelines(speed_event[0])
    f.close()
    print(f"节点速度为{speed_event[1]}")


if __name__ == '__main__':
    main()
