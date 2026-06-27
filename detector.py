import subprocess

def get_active_vms(config):
    active = []
    # Loop through the hypervisors defined in your YAML
    for name, settings in config.get('hypervisors', {}).items():
        if not settings.get('enabled', False):
            continue
            
        path = settings.get('path')
        try:
            if name == 'vmware':
                out = subprocess.check_output([path, 'list'], text=True, stderr=subprocess.DEVNULL)
                if "Total running VMs" in out:
                    lines = out.strip().split('\n')
                    if len(lines) > 1:
                        vm_name = lines[1].split('/')[-1].replace('.vmx', '')
                        active.append((vm_name, 'vmware'))
            
            elif name == 'virtualbox':
                out = subprocess.check_output([path, 'list', 'runningvms'], text=True, stderr=subprocess.DEVNULL)
                if out.strip():
                    active.append((out.split('"')[1], 'virtualbox'))
            
            elif name == 'qemu':
                out = subprocess.check_output([path, '-c', 'qemu:///session', 'list', '--name'], text=True, stderr=subprocess.DEVNULL)
                if out.strip():
                    active.append((out.strip().split('\n')[0], 'qemu'))
            
            elif name == 'parallels':
                out = subprocess.check_output([path, 'list', '--running'], text=True, stderr=subprocess.DEVNULL)
                if out.strip():
                    # Parallels list output parsing
                    vm_name = out.strip().split('\n')[0].split()[0]
                    active.append((vm_name, 'parallels'))
                    
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass # Hypervisor not installed or path incorrect, skip it!
            
    return active