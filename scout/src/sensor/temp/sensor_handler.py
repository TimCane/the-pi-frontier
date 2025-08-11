from machine import Pin
from ds18x20 import DS18X20
from onewire import OneWire
from time import sleep_ms

class SensorHandler:
    def __init__(self, pinid):
        """Initialize sensor interfaces"""
        self.pinid = pinid
        self.pin = None
        self.sensor = None
        self.devices = None
        
        self.setup_interfaces()
    
    def setup_interfaces(self):
        """Setup I2C and SPI interfaces"""
        try:
            
            self.pin = Pin(self.pinid)
            self.sensor = DS18X20(OneWire(self.pin))
            self.devices = self.sensor.scan()
            
            print("Sensor interfaces initialized")
        except Exception as e:
            print(f"Error setting up sensor interfaces: {e}")
    
    def scan_sensor(self):
        """Scan for I2C devices"""
        if self.sensor:
            
            print(f"I2C devices found: {[hex(device) for device in devices]}")
            return devices
        return []
    
    def read_temperature(self):
        """Read temperature from sensor"""
        
        self.sensor.convert_temp()
        sleep_ms(750)
        
        return self.sensor.read_temp(self.devices[0])
    
    def read(self):
        """Read sensor data"""
        return {
            'type': 'temperature',
            'value': self.read_temperature(),
        }


