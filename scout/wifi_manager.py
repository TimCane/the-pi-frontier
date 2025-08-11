import network
import time
import machine

class WiFiManager:
    def __init__(self, hostname, ssid, password, led = None):
        self.ssid = ssid
        self.password = password
        self.hostname = hostname
        self.led = led
        self.wlan = network.WLAN(network.STA_IF)
    
    def connect(self, timeout=10):
        """Connect to WiFi network"""
        self.wlan.active(True)
        
        if not self.wlan.isconnected():
            print(f"Connecting to {self.ssid}...")
            network.hostname(self.hostname)
            self.wlan.connect(self.ssid, self.password)
            
            # Wait for connection
            start_time = time.time()
            while not self.wlan.isconnected() and (time.time() - start_time) < timeout:
                self._blink_led()
                print(".", end="")
            
            print()  # New line
        
        return self.wlan if self.wlan.isconnected() else None
    
    def disconnect(self):
        """Disconnect from WiFi"""
        if self.wlan.isconnected():
            self.wlan.disconnect()
        self.wlan.active(False)
    
    def get_status(self):
        """Get connection status"""
        return {
            'connected': self.wlan.isconnected(),
            'ip': self.wlan.ifconfig()[0] if self.wlan.isconnected() else None,
            'signal': self.wlan.status('rssi') if hasattr(self.wlan, 'status') else None
        }

    def _blink_led(self):
        if self.led:
            self.led.on()
            time.sleep(0.25)
            self.led.off()
            time.sleep(0.25)
