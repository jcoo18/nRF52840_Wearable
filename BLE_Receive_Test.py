"""
This is Copilot generated code for quick testing of the BLE receive function.

"""

# Import necessary modules
import time
from adafruit_ble import BLERadio
from adafruit_ble.services.nordic import UARTService
import board
import digitalio

# Initialize BLE radio
ble = BLERadio()

# Create a UART service
uart_service = UARTService()

# Advertise the UART service
advertisement = uart_service.advertisement
advertisement.complete_name = "MyBLEDevice"
advertisement.appearance = 0x03C0  # Generic Heart Rate Sensor
advertisement.tx_power = 0
advertisement.start()

# Set up a pin for waking up from sleep
wakeup_pin = digitalio.DigitalInOut(board.D2)
wakeup_pin.switch_to_input(pull=digitalio.Pull.UP)

# Main loop
while True:
    # Check for incoming connections
    if ble.connected:
        # Receive data from the central device (client)
        received_data = uart_service.read()
        if received_data:
            print(f"Received: {received_data.decode('utf-8')}")
            # Exit sleep mode if a notification is received
            break

    # Enter low-power sleep mode
    ble.radio.power.save_mode = True
    while not wakeup_pin.value:
        pass
    ble.radio.power.save_mode = False

# Note: You'll need to handle disconnections, security, and other aspects in a complete application.
# Consult the nRF52840 documentation and libraries for more advanced features.
