import network
import requests
from time import sleep, time
from picozero import pico_temp_sensor, pico_led
import config

def get_temperature():
    # This needs to be updated once I have a DS18B20 sensor 
    return pico_temp_sensor.temp

def connect_to_wlan():    
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    # Check if already connected
    if wlan.isconnected():
        print("Already connected to Wi-Fi")
        print("IP Address:", wlan.ifconfig()[0])
        pico_led.on()
        return True
    
    print("Connecting to Wi-Fi...")
    wlan.connect(config.WIFI_SSID, config.WIFI_PASSWORD)
    
    # Wait for connection
    timeout = 10  # 10 seconds timeout
    start_time = time()
    while not wlan.isconnected():
        if time() - start_time > timeout:
            print("Connection timed out")
            return False
        pico_led.on()
        sleep(0.5)
        pico_led.off()
        sleep(0.5)
    
    # If connected, print IP address
    print("Connected to Wi-Fi")
    print("IP Address:", wlan.ifconfig()[0])
    pico_led.on()
    return True

def disconnect_from_wlan():
    wlan = network.WLAN(network.STA_IF)
    
    # Check if already disconnected
    if not wlan.isconnected():
        print("Already disconnected from Wi-Fi")
        return
    
    wlan.active(False)  # Deactivate the Wi-Fi interface to disconnect
    wlan.deinit()
    pico_led.off()
    print("Disconnected from Wi-Fi.")



def broadcast_temperature(current_temperature):
    connect_to_wlan()

    response = requests.post(config.WEBHOOK_URL,json = {'host': config.HOST_NAME, 'type': 'temperature' , 'value': current_temperature}, headers = {"Authorization": config.WEBHOOK_AUTH})

    response_code = response.status_code

    print("Sent temperature to webhook: " + str(current_temperature))

    disconnect_from_wlan()

    if not response_code == 200:
        raise Exception("Response not OK!") 
    


def run():
    loop = True
    while loop == True:
        consecutive_errors = 0
        try:
            broadcast_temperature(get_temperature())
            consecutive_errors = 0

        except Exception as e:
            print(f"Error: {e}")
            consecutive_errors += 1
            if consecutive_errors > 5:
                print("Errored more than 5 times in a row. Stopping")
                loop = False
        finally:
            print("Sleeping for " + str(config.SLEEP_DURATION) + " seconds")
            sleep(config.SLEEP_DURATION)

run()

