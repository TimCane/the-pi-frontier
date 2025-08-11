# main.py - Main application file
import machine
import network
import time
import gc
from wifi_manager import WiFiManager
from sensor_handler import SensorHandler
import config
import requests

# Global variables
wlan = None
sensor = None
led = machine.Pin("LED", machine.Pin.OUT)
hostname = f"scout-{config.LOCATION}-{config.SENSOR}"

def setup_hardware():
    """Initialize hardware components"""
    global sensor
    print("Setting up hardware...")
    
    # Initialize built-in LED
    led.off()
    
    # Initialize sensors/peripherals
    sensor = SensorHandler(config.DS18X20_DAT_PIN)
    
    # Flash LED to indicate hardware ready
    for _ in range(3):
        led.on()
        time.sleep(0.1)
        led.off()
        time.sleep(0.1)

def setup_wifi():
    """Initialize WiFi connection"""
    global wlan
    global hostname
    global led
    print("Setting up WiFi...")
    
    wifi_manager = WiFiManager(hostname,config.WIFI_SSID, config.WIFI_PASSWORD, led)
    wlan = wifi_manager.connect()
    
    if wlan and wlan.isconnected():
        print(f"Connected to WiFi. IP: {wlan.ifconfig()[0]}")
        return True
    else:
        print("Failed to connect to WiFi")
        return False

def handle_error(error):
    """Error handling with LED indication"""
    print(f"Error: {error}")
    
    f = open('error.txt', 'w')
    f.write(f"Error: {error}\n")
    f.close()

    
    # Flash LED rapidly to indicate error
    for _ in range(10):
        led.on()
        time.sleep(0.05)
        led.off()
        time.sleep(0.05)

def send_reading(reading):
    """Sending """
    global hostname
    
    body = {'host': hostname, 'type': reading['type'] , 'value': reading['value']}
    
    print(f"Sending request to '{config.WEBHOOK_URL}'")
    print(f"Request contents: '{body}'")
    
    requests.post(config.WEBHOOK_URL,json = body, headers = {"Authorization": config.WEBHOOK_AUTH})

def main_loop():
    """Main application loop"""
    print("Starting main loop...")
    
    while True:
        try:
            # Main application logic here
            led.on()
            
            # Read sensors
            if sensor:
                reading = sensor.read()
                print(f"Sensor reading: {reading}")
            
            # Network operations
            if wlan and wlan.isconnected():
                # Send data, handle requests, etc.
                
                send_reading(reading)
                 
                pass
            else:
                print("WiFi disconnected, attempting reconnect...")
                setup_wifi()
            
            led.off()
            time.sleep(config.LOOP_DELAY)
            
            # Memory management
            gc.collect()
                
        except KeyboardInterrupt:
            print("Program interrupted by user")
            break
        except Exception as e:
            handle_error(e)
            time.sleep(10)

def cleanup():
    """Cleanup resources before exit"""
    print("Cleaning up...")
    led.off()
    if wlan:
        wlan.disconnect()

def main():
    """Main entry point"""
    try:
        print("=== Pico 2 W Application Starting ===")
        
        setup_hardware()
        
        setup_wifi()
        
        main_loop()
        
    except Exception as e:
        handle_error(e)
    finally:
        cleanup()

if __name__ == "__main__":
    main()

