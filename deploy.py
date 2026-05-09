import pexpect
import sys

def run_cmd(cmd, password):
    print(f"Running: {cmd}")
    child = pexpect.spawn(cmd, encoding='utf-8', timeout=60)
    child.logfile = sys.stdout
    
    index = child.expect(['(?i)password:', '(?i)are you sure you want to continue connecting', pexpect.EOF, pexpect.TIMEOUT])
    
    if index == 1:
        child.sendline('yes')
        child.expect('(?i)password:')
        child.sendline(password)
    elif index == 0:
        child.sendline(password)
    
    child.expect(pexpect.EOF)
    return child.before

password = "Welkom"
host = "10.10.10.146"
user = "root"

# Step 1: Upload zip
run_cmd(f"scp redesign.zip {user}@{host}:/root/", password)

# Step 2: Setup on remote
remote_cmds = [
    "mkdir -p /root/redesign",
    "unzip -o /root/redesign.zip -d /root/redesign",
    "docker stop redesign-web || true",
    "docker rm redesign-web || true",
    "docker run -d --name redesign-web -p 80:80 -v /root/redesign:/usr/share/nginx/html nginx"
]

ssh_cmd = f"ssh -o StrictHostKeyChecking=no {user}@{host} '{' && '.join(remote_cmds)}'"
run_cmd(ssh_cmd, password)
