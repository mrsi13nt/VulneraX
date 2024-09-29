import time
import logging
from bluepy.btle import Scanner, DefaultDelegate, Peripheral, BTLEManagementError
from src.configs import printt

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ScanDelegate(DefaultDelegate):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            logging.info(f"Discovered new device: {dev.addr} ({dev.addrType})")
        elif isNewData:
            logging.info(f"Received new data from: {dev.addr}")

def scan_devices(duration=10) -> list:
    """Scan for Bluetooth devices for a given duration."""
    printt("Scanning for Bluetooth devices...")
    try:
        scanner = Scanner().withDelegate(ScanDelegate())
        devices = scanner.scan(duration)

        for dev in devices:
            logging.info(f"Device {dev.addr} ({dev.addrType})")
            for (adtype, desc, value) in dev.getScanData():
                logging.info(f"  {desc}: {value}")
        return devices
    except BTLEManagementError as e:
        printt(f"Error scanning for Bluetooth devices: {e}")
        printt("It looks like your system might not have a Bluetooth adapter.")
        return []

def discover_services(device_address: str):
    """Discover services on a Bluetooth device."""
    logging.info(f"Connecting to device {device_address}...")
    try:
        peripheral = Peripheral(device_address)
        services = peripheral.getServices()

        logging.info(f"Services on {device_address}:")
        for service in services:
            logging.info(f"  {service.uuid}")

        peripheral.disconnect()
    except Exception as e:
        printt(f"Failed to connect or discover services: {e}")

def perform_pairing_attack(device_address: str):
    """Simulate a pairing attack (for demonstration purposes)."""
    logging.info(f"Attempting pairing attack on {device_address}...")
    # Pairing attack simulation - this is a placeholder for actual attack techniques
    logging.warning("Note: Actual Bluetooth pairing attacks are complex and may require specific tools and techniques.")
    time.sleep(2)
    logging.info("Pairing attack simulation complete.")

def blue():
    duration = 10  # Scan duration in seconds

    # Scan for devices
    devices = scan_devices(duration)

    # Discover services on first device (if any)
    if devices:
        first_device = devices[0].addr
        discover_services(first_device)

        # Perform a pairing attack simulation
        perform_pairing_attack(first_device)
    else:
        logging.warning("No devices found during the scan.")

