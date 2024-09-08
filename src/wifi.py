import subprocess
import time
from scapy.all import *
import psutil
import sys

def list_network_interfaces():
    """List network interfaces with details."""
    interfaces = psutil.net_if_addrs()
    interface_details = []

    print("***************************** Interface selection ******************************")
    print("Select an interface to work with:")
    print("---------")
    
    index = 1
    for interface, addrs in interfaces.items():
        # Get the chipset info (if available)
        chipset_info = "Unknown"  # Placeholder, actual chipset info requires different methods
        for addr in addrs:
            if addr.family == psutil.AF_LINK:
                chipset_info = addr.address  # Use MAC address as a placeholder for chipset info
        
        print(f"{index}. {interface} // Chipset: {chipset_info}")
        interface_details.append(interface)
        index += 1

    print("---------")
    return interface_details

def select_interface():
    """Allow the user to select a network interface."""
    interfaces = list_network_interfaces()
    
    while True:
        try:
            choice = int(input("Enter the number of the interface you want to use: "))
            if 1 <= choice <= len(interfaces):
                selected_interface = interfaces[choice - 1]
                print(f"You selected: {selected_interface}")
                return selected_interface
            else:
                print("Invalid choice. Please enter a number corresponding to the listed interfaces.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def scan_wifi_networks(interface):
    """Scan for Wi-Fi networks and print details."""
    try:
        print(f"Scanning for Wi-Fi networks on {interface}...")
        networks = set()

        def packet_handler(packet):
            if packet.haslayer(Dot11Beacon):
                ssid = packet[Dot11Elt].info.decode('utf-8', 'ignore')
                bssid = packet[Dot11].addr2
                networks.add((bssid, ssid))

        sniff(iface=interface, prn=packet_handler, timeout=20)

        print("\nDetected Wi-Fi Networks:")
        for bssid, ssid in networks:
            print(f"BSSID: {bssid}, SSID: {ssid}")

    except PermissionError:
        print("Permission Error: This script requires root privileges to run. Please run it with 'sudo'.")
        sys.exit(1)

def capture_handshake(interface, output_file):
    """Capture WPA/WPA2 handshakes."""
    try:
        print(f"Capturing WPA/WPA2 handshake on {interface}...")
        def packet_handler(packet):
            if packet.haslayer(Dot11):
                addr1 = packet[Dot11].addr1
                addr2 = packet[Dot11].addr2
                addr3 = packet[Dot11].addr3
                if packet.haslayer(Dot11Auth):
                    with open(output_file, 'ab') as f:
                        f.write(bytes(packet))
                elif packet.haslayer(Dot11AssoReq):
                    with open(output_file, 'ab') as f:
                        f.write(bytes(packet))

        sniff(iface=interface, prn=packet_handler, timeout=60)
        print(f"Handshake capture complete. Saved to {output_file}")

    except PermissionError:
        print("Permission Error: This script requires root privileges to run. Please run it with 'sudo'.")
        sys.exit(1)

def scan_wireless_devices(interface):
    """Scan for wireless devices."""
    try:
        print(f"Scanning for wireless devices on {interface}...")
        devices = set()

        def packet_handler(packet):
            if packet.haslayer(Dot11ProbeReq):
                ssid = packet[Dot11Elt].info.decode('utf-8', 'ignore')
                addr = packet[Dot11].addr2
                devices.add((addr, ssid))

        sniff(iface=interface, prn=packet_handler, timeout=20)

        print("\nDetected Wireless Devices:")
        for addr, ssid in devices:
            print(f"MAC Address: {addr}, SSID: {ssid}")

    except PermissionError:
        print("Permission Error: This script requires root privileges to run. Please run it with 'sudo'.")
        sys.exit(1)

def wpa_password_crack(handshake_file, wordlist_file):
    """Attempt to crack WPA/WPA2 password."""
    print(f"Cracking WPA/WPA2 password from {handshake_file}...")
    
    def compute_psk(ssid, password):
        import hashlib
        key = hashlib.pbkdf2_hmac('sha1', password.encode(), ssid.encode(), 4096, 32)
        return binascii.hexlify(key).decode()

    def is_valid_psk(psk, captured_handshake):
        # Simplistic check; actual implementation would be more complex
        return psk in captured_handshake

    with open(wordlist_file, 'r') as wordlist:
        for line in wordlist:
            password = line.strip()
            print(f"Testing password: {password}")
            psk = compute_psk('ExampleSSID', password)  # Replace 'ExampleSSID' with the actual SSID
            if is_valid_psk(psk, 'dummy_handshake_data'):  # Replace 'dummy_handshake_data' with actual handshake data
                print(f"Password found: {password}")
                return password

    print("Password cracking attempt finished.")

def main(interface):
    # Scan for Wi-Fi networks
    scan_wifi_networks(interface)

    # Scan for wireless devices
    scan_wireless_devices(interface)

    handshake_file = 'handshake.pcap'
    capture_handshake(interface, handshake_file)

    # Crack WPA/WPA2 password (Example; requires a real wordlist file)
    wordlist_file = 'wordlist.txt'
    wpa_password_crack(handshake_file, wordlist_file)

def wifi():
    selected_interface = select_interface()
    # Proceed with the selected interface
    print(f"Proceeding with interface: {selected_interface}")
    main(selected_interface)