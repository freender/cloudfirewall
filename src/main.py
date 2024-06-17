import requests
import time
import subprocess

# Function to get current public IP address
def get_current_ip():
    try:
        # Use a reliable service to fetch the public IP address
        response = requests.get('https://api.ipify.org?format=json')
        data = response.json()
        return data['ip'] if 'ip' in data else None
    except Exception as e:
        print(f"Error fetching IP address: {e}")
        return None

# Function to update firewall rule with new IP
def update_firewall_rule(new_ip):
    try:
        # Replace with your actual command or API call to update WAF rule
        # Example command line:
        # subprocess.run(['waf-cli', 'update-rule', '--ip', new_ip])
        
        # Example API call:
        # response = requests.post('https://waf-api.example.com/update-rule', json={'ip': new_ip})
        
        print(f"Updating firewall rule with new IP: {new_ip}")
        # Uncomment and replace with actual update logic
        
        return True  # Return true if update was successful
    except Exception as e:
        print(f"Error updating firewall rule: {e}")
        return False

# Main function to check and update IP if changed
def main():
    last_ip = None
    
    while True:
        current_ip = get_current_ip()
        
        if current_ip and current_ip != last_ip:
            if update_firewall_rule(current_ip):
                last_ip = current_ip
            else:
                print("Failed to update firewall rule.")
        
        time.sleep(600)  # Wait for 10 minutes (600 seconds)

if __name__ == "__main__":
    main()