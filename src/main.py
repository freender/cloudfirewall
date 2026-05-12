import time
import logging
import signal
import threading
from modules import modules


shutdown_event = threading.Event()


def handle_shutdown(signum, _frame):
    logging.info("Received signal %s; stopping cloudfirewall", signum)
    shutdown_event.set()

# Main function to check and update IP if changed
def main():
    signal.signal(signal.SIGTERM, handle_shutdown)
    signal.signal(signal.SIGINT, handle_shutdown)

    last_ip = modules.get_firewall_ip()
    
    while not shutdown_event.is_set():
        current_ip = modules.get_current_ip()
        
        if current_ip and last_ip and current_ip != last_ip:
           if modules.update_firewall_rule(current_ip):
                last_ip = current_ip
           else:
                logging.error(f"Failed to update firewall rule.")        
        shutdown_event.wait(600)  # Wait for 10 minutes (600 seconds)

if __name__ == "__main__":
    main()
