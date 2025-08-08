CREATE TABLE temperature (
    id INT AUTO_INCREMENT PRIMARY KEY,
    value DOUBLE NOT NULL,
    recorded_on TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    device_id INT NOT NULL,
    FOREIGN KEY (device_id) REFERENCES device(id),
    INDEX idx_temperature_device_id (device_id)
);