# 🐧 Linux Essentials for Cyber Security & SOC Operations
**Author:** Manoj M | Network & Cyber Security Engineer  
**Alignment:** Networkers Home Cyber & Cloud Security Roadmap (Module 2B: Linux Essentials)

---

## 📌 1. Critical Linux Security & Network Diagnostic Commands

| Task | Command | Purpose |
| :--- | :--- | :--- |
| **Active Network Sockets** | `ss -tulpn` or `netstat -plnt` | Lists all listening TCP/UDP ports and the associated Process ID (PID). |
| **Open Files & Connections** | `lsof -i :<port>` | Identifies which process or daemon is holding a specific port. |
| **Process Tree Inspection** | `ps aux --forest` | Displays processes in an execution hierarchy to spot spawned reverse shells. |
| **Authentication Logs** | `grep "Failed password" /var/log/auth.log` | Extracts failed SSH authentication attempts (Debian/Ubuntu). |
| **Failed Logins Tracking** | `lastb -n 20` | Displays the last 20 failed login sessions recorded in `/var/log/btmp`. |
| **Active Sudo Commands** | `journalctl _COMM=sudo -f` | Real-time stream of all elevated `sudo` commands executed on the system. |

---

## 📌 2. Linux System & Service Hardening (CIS Baseline)

### Secure SSH Daemon (`/etc/ssh/sshd_config`)
```bash
# Disable remote root login
PermitRootLogin no

# Enforce SSH Key authentication & disable cleartext passwords
PasswordAuthentication no
PubkeyAuthentication yes

# Restrict idle timeouts (disconnect after 5 minutes of inactivity)
ClientAliveInterval 300
ClientAliveCountMax 0

# Limit authentication attempts to mitigate brute-force
MaxAuthTries 3
```
After editing, verify syntax and reload: `sudo sshd -t && sudo systemctl restart sshd`.

---

## 📌 3. Linux Host Firewall Configuration (`iptables` & `ufw`)

### UFW (Uncomplicated Firewall)
```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 22/tcp
sudo ufw allow 443/tcp
sudo ufw enable
sudo ufw status verbose
```

### IPTables Stateful Baseline Rules
```bash
# Allow established and related connections
sudo iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT

# Allow loopback interface
sudo iptables -A INPUT -i lo -j ACCEPT

# Allow inbound SSH on Port 22
sudo iptables -A INPUT -p tcp --dport 22 -m conntrack --ctstate NEW -j ACCEPT

# Drop all other inbound traffic
sudo iptables -P INPUT DROP
```

---

## 📌 4. Auditing SUID Binaries (Privilege Escalation Defense)
Attackers exploit misconfigured SUID binaries to escalate privileges to `root`. Find all SUID binaries on the filesystem:
```bash
find / -perm -4000 -type f -exec ls -la {} + 2>/dev/null
```
*If binaries like `/usr/bin/find`, `/usr/bin/vim`, or `/bin/bash` have the SUID bit set, remove it immediately:*
```bash
sudo chmod u-s /path/to/binary
```
