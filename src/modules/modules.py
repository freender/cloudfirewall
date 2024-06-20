import requests
import logging
import cfg
import re
import json

# Function to get current public IP address
def get_current_ip():
    try:
        # Use a reliable service to fetch the public IP address
        response = requests.get('https://api.ipify.org?format=json')
        if response.status_code != 200:
            result = f"Failed to retrieved current IP. Status code: {response.status_code}"
            logging.error(f"{result}: Response text: {response.text}")
            return None
        data = response.json()
        logging.warning(f"Current IP:  {data['ip']}" )
        return data['ip'] if 'ip' in data else None
    except Exception as e:
        logging.error(f"Error fetching IP address: {e}")
        return None

# Function to get IP from Cloudflare firewall rule
def get_firewall_ip():   
    url = f"https://api.cloudflare.com/client/v4/zones/{cfg.WAF_ZONE}/rulesets/{cfg.WAF_RULESET}"

    # Headers for authentication and content type
    headers = {
        'Authorization': "Bearer " + cfg.WAF_TOKEN
    }
    
    try:
        response = requests.get(url, headers=headers)
        # Check the response status
        if response.status_code != 200:
            result = f"Failed to retrieved the rule. Status code: {response.status_code}"
            logging.error(f"{result}: Response text: {response.text}")
            return None
        
        response_dict = response.json()
        rules = response_dict['result']['rules']
            
        for rule in rules:
            if rule.get('id') == cfg.WAF_RULEID:
                expression = rule.get('expression', '')
                # Extract current ip using regular expression
                current_ip = re.search(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b", expression).group()
                logging.warning(f"Firewall IP:  {current_ip}" )        
                return current_ip
    
        result = 'Rule retrieved successfully.'
        logging.warning(result)
            
    except Exception as e:
        result = f"Unexpected error occurred"
        logging.error(result + ": " + str(e))
    return None    


# Function to update firewall rule with new IP
def update_firewall_rule(new_ip):

    # Update the firewall rule data
    rule_data = {
        "action": "block",       
        "expression": "(not ip.src in {" + new_ip + "} )",
        "description": "Whitelist IP"
    }

    # Cloudflare API endpoint for updating a WAF rule
    url = f"https://api.cloudflare.com/client/v4/zones/{cfg.WAF_ZONE}/rulesets/{cfg.WAF_RULESET}/rules/{cfg.WAF_RULEID}"

    # Headers for authentication and content type
    headers = {
        'Authorization': "Bearer " + cfg.WAF_TOKEN
    }
    
    try:
        response = requests.patch(url, headers=headers, data=json.dumps(rule_data))
        # Check the response status
        if response.status_code == 200:
            result = f"IP {new_ip} has been sucessfully added to the firewall rule."
            logging.warning(result)
            return result
        else:
            result = f"Failed to update rule. Status code: {response.status_code}"
            logging.error(f"{result}: Response text: {response.text}")
    except Exception as e:
        result = f"Unexpected error occurred"
        logging.error(result + ": " + str(e))
    return None