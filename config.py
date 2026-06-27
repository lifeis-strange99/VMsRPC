import json
import os
import easygui

CONFIG_FILE = "config.json"

def get_config():
    # If config.json doesn't exist, create it
    if not os.path.exists(CONFIG_FILE):
        app_id = easygui.enterbox("Enter your Discord Application ID:", "Setup")
        data = {
            "application_id": app_id,
            "vmrun_path": "", 
            "vmware_file": "vmware-vmx"
        }
        with open(CONFIG_FILE, "w") as f:
            json.dump(data, f, indent=4)
        return data
    
    # Load existing config
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)
