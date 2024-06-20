import time
import logging
from modules import modules

# Main function to check and update IP if changed
def main():
    last_ip = modules.get_firewall_ip()
    
    while True:
        current_ip = modules.get_current_ip()
        
        if current_ip and last_ip and current_ip != last_ip:
           if modules.update_firewall_rule(current_ip):
                last_ip = current_ip
           else:
                logging.error(f"Failed to update firewall rule.")        
        time.sleep(600)  # Wait for 10 minutes (600 seconds)

if __name__ == "__main__":
    main()