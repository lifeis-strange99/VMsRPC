
# VMsRPC (Virtual Machine Rich Presence)

VMsRPC is a modular, multi-hypervisor Discord Rich Presence tool that automatically detects running virtual machines across VMware, VirtualBox, QEMU, and Parallels. It keeps your Discord status updated with your current VM hostname, OS, and custom branding.

## Features

* **Multi-Hypervisor Support:** Works with VMware, VirtualBox, QEMU, and Parallels.
* **Auto-Discovery:** Automatically detects new VMs without manual intervention.
* **Hardcoded Overrides:** Define specific metadata (hostname, OS, icons) for your primary lab machines.
* **Live Configuration:** Edit `config.yaml` while the script is running for instant updates.
* **Cross-Platform:** Works on Windows and Linux. (macOS is not tested)

## Installation

1. **Clone the repository:**

```bash
git clone https://github.com/lifeis-strange99/VMsRPC.git
cd VMsRPC

```

2. **Install dependencies:**

```bash
pip install -r requirements.txt

```

3. **Install Tkinter (if missing):**
If you get `ModuleNotFoundError: No module named 'tkinter'`, install it using the method for your OS:

* **Windows:** Rerun the Python installer, choose **Modify**, check **tcl/tk and IDLE**, and finish.
* **Ubuntu / Debian / Mint:** `sudo apt install python3-tk`
* **Fedora / RHEL / CentOS:** `sudo dnf install python3-tkinter`
* **Arch Linux:** `sudo pacman -S tk`
* **macOS:** `brew install tcl-tk` (if using Homebrew Python)

*Verify your installation by running: `python3 -m tkinter*`

## Configuration

To set up the script, copy the provided example configuration file:

1. Copy `config.example.yaml` and rename it to `config.yaml`.
2. Open `config.yaml` and enter your **Discord Application ID**.
3. Configure the `path` for your installed hypervisors (e.g., provide the path to `vmrun.exe` on Windows or ensure the command is in your system PATH for Linux).

### Discord Setup

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications).
2. Create a **New Application**.
3. Copy the **Application ID** from the "General Information" tab.
4. Go to the **Rich Presence -> Art Assets** tab to upload your VM icons.

* *Note: The "Image Key" you set in the portal must match the `image_key` defined in your `config.yaml`.*

### Example `config.yaml`

```yaml
application_id: "13223121"
hypervisors:
  vmware:
    enabled: true
    path: "C:\\Program Files (x86)\\VMware\\VMware Workstation\\vmrun.exe"
  virtualbox:
    enabled: true
    path: "VBoxManage"
# ... (see generated file for full options)

```

## Usage

To start monitoring your virtual machines, run:

```bash
python main.py

```

### How it works

* **Detection:** The script polls your enabled hypervisors every 15 seconds.
* **Discovery:** If a detected VM is not in your `hardcoded` list, it will use the default `discovery_rules` defined in `config.yaml`.
* **Customization:** To customize a specific VM's display, add its name to the `hardcoded` section in `config.yaml` to set a custom hostname, OS label, and image key.

## Icons

Your repository includes an `/icons` folder with pre-prepared assets for various operating systems and software. Upload these to your Discord Developer Portal as needed to match your `image_key` settings.

---

*Built with Python, pypresence, and PyYAML.*
