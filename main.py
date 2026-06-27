import time
import os
import yaml
import easygui
from pypresence import Presence
from pypresence.exceptions import DiscordNotFound, InvalidPipe
import detector

CONFIG_FILE = "config.yaml"

def load_config():
    """Loads the YAML configuration file silently."""
    if not os.path.exists(CONFIG_FILE):
        # Only prompt if missing
        app_id = easygui.enterbox("Enter Discord Application ID:", "First-time Setup")
        # ... (logic to create the file) ...
    
    with open(CONFIG_FILE, "r") as f:
        return yaml.safe_load(f)

def format_presence_data(raw_name, hypervisor, config):
    """Applies hardcoded and discovery rules."""
    # 1. Hardcoded check
    if raw_name in config.get('hardcoded', {}):
        data = config['hardcoded'][raw_name]
        return data['hostname'], data['os'], data['image_key']
    
    # 2. Discovery Rules
    rules = config.get('discovery_rules', {}).get(hypervisor, {})
    if rules.get('enabled'):
        os_guess = "Windows" if "windows" in raw_name.lower() else "Linux" if "linux" in raw_name.lower() else "VM"
        return raw_name, f"{hypervisor.capitalize()} - {os_guess}", rules.get('default_image', 'default')
    
    return None, None, None

def main():
    print("Loading configuration...")
    # Initial config load
    config = load_config()
    client_id = str(config['application_id'])
    interval = config.get('update_interval', 15)

    RPC = Presence(client_id)
    
    # Connection Loop
    while True:
        try:
            RPC.connect()
            break
        except (DiscordNotFound, InvalidPipe):
            time.sleep(10)

    # Continuous Monitoring Loop
    while True:
        try:
            # Reload for live-editing capability
            config = load_config()
            
            # Pass the WHOLE config to detector so it knows what's enabled
            active_vms = detector.get_active_vms(config)
            
            if active_vms:
                raw_name, hypervisor = active_vms[0]
                hostname, os_name, img = format_presence_data(raw_name, hypervisor, config)
                
                if hostname:
                    RPC.update(
                        details=f"Running: {hostname}", 
                        state=f"OS: {os_name}", 
                        large_image=img,
                        large_text=f"{hypervisor.upper()} Engine"
                    )
            else:
                RPC.clear()
        
        except Exception as e:
            print(f"Monitor error: {e}")
                
        time.sleep(interval)

if __name__ == "__main__":
    main()