import socket
import subprocess
import platform
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

# Get hostname
def get_hostname(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except socket.herror:
        return "Unknown"

# Ping function
def ping(ip):
    system = platform.system().lower()

    if system == "windows":
        command = ["ping", "-n", "1", "-w", "1000", ip]
    else:
        command = ["ping", "-c", "1", "-W", "1", ip]

    result = subprocess.run(
        command,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    return result.returncode == 0


# Scan a single IP
def scan_ip(ip):
    if ping(ip):
        hostname = get_hostname(ip)

        print(f"[ACTIVE] {ip:18} → {hostname}")

        return (ip, hostname)

    return None


# Network scanner
def scan_network(base_ip, start, end):

    print("=" * 55)
    print("         🌐 Advanced Network Scanner")
    print("=" * 55)

    print("⚠️ For educational purposes only.\n")

    print(
        f"🔍 Scanning: {base_ip}.{start} → {base_ip}.{end}"
    )

    print(
        f"⏱ Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    )

    active_devices=[]

    ip_list = [
        f"{base_ip}.{i}"
        for i in range(start,end+1)
    ]

    # Faster scan with threads
    with ThreadPoolExecutor(max_workers=50) as executor:

        results=executor.map(
            scan_ip,
            ip_list
        )

        for result in results:

            if result:
                active_devices.append(result)

    print("\n"+"="*55)

    print(
        f"✅ Scan Complete!"
    )

    print(
        f"📡 Active devices found: {len(active_devices)}"
    )

    if active_devices:

        print("\n📋 Active Device Summary:\n")

        for ip,hostname in active_devices:

            print(
                f"{ip:18} | {hostname}"
            )

    else:

        print(
            "\nNo active devices found."
        )


# Main
def main():

    print("="*55)
    print("         🌐 Advanced Network Scanner")
    print("="*55)

    try:

        base_ip=input(
            "Enter base IP (Example: 192.168.1): "
        )

        start=int(
            input("Start range: ")
        )

        end=int(
            input("End range: ")
        )

        if start<1 or end>254:

            print(
                "\n❌ Range must be between 1-254"
            )

            return

        if start>end:

            print(
                "\n❌ Start cannot be greater than End"
            )

            return

        scan_network(
            base_ip,
            start,
            end
        )

    except ValueError:

        print(
            "\n❌ Please enter valid numbers"
        )

    except KeyboardInterrupt:

        print(
            "\n\nScan cancelled by user."
        )


if __name__=="__main__":
    main()