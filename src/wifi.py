import scapy
import os
import psutil

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




def wifi():
    selected_interface = select_interface()
    # Proceed with the selected interface
    print(f"Proceeding with interface: {selected_interface}")