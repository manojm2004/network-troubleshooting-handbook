# 📘 Cisco CCNA 200-301: Master Router & Switch Command Encyclopedia

> The complete, production-grade syntax, configuration runbook, and diagnostic manual for every Router and Switch command in the Cisco CCNA 200-301 curriculum.

**Author:** Manoj M | Network & Security Engineer  
**GitHub:** [github.com/manojm2004](https://github.com/manojm2004)  
**Target Certification:** Cisco Certified Network Associate (CCNA 200-301)  

---

## 📂 Repository Contents

| File | Purpose |
| :--- | :--- |
| **[`cisco_router_complete_commands.cfg`](cisco_router_complete_commands.cfg)** | Exhaustive, production-ready Cisco IOS Router configuration (SSH, OSPF, NAT, DHCP, HSRP, ACLs, Subinterfaces). |
| **[`cisco_switch_complete_commands.cfg`](cisco_switch_complete_commands.cfg)** | Exhaustive, production-ready Cisco Catalyst Switch configuration (VLANs, 802.1Q Trunking, Rapid-PVST, EtherChannel LACP, Port Security, DHCP Snooping, DAI, SVI Layer 3 routing). |
| **[`show_and_debug_troubleshooting_guide.md`](show_and_debug_troubleshooting_guide.md)** | Output decoders for every `show` command, safe filtered debugging techniques, and top 5 real-world NOC incident runbooks. |
| **[`interactive_command_finder.py`](interactive_command_finder.py)** | Interactive Python CLI tool to instantly search and look up command syntax by keyword. |

---

## ⚡ Quick-Lookup CLI Tool
Search any command, configuration mode, or protocol in seconds:

```bash
# Search for OSPF routing syntax
python interactive_command_finder.py ospf

# Search for 802.1Q trunking syntax
python interactive_command_finder.py trunk

# Search for Network Address Translation (NAT/PAT)
python interactive_command_finder.py nat

# Interactive Mode
python interactive_command_finder.py
```

---

## 🧭 Master Command Map by Domain

```
Cisco CCNA 200-301 Command Map
├── 1. Device Administration & Management
│   ├── Hostname, Domain Name, Legal Banners
│   ├── Usernames (Privilege 15), Secret Password Encryption
│   ├── Line Console 0 & Line VTY 0 15 (SSHv2, Exec-Timeout, Logging Synchronous)
│   └── Clock, Timezone & NTP Client/Server Configuration
│
├── 2. Layer 2 Switching & Campus LAN
│   ├── VLAN Database (vlan <id>, name <NAME>)
│   ├── Access Switchports & Voice VLANs (switchport access/voice vlan)
│   ├── 802.1Q Trunking (switchport mode trunk, native vlan, allowed vlan, nonegotiate)
│   ├── Spanning Tree Protocol (Rapid-PVST, Root Primary/Secondary, PortFast, BPDU Guard)
│   └── Link Aggregation (EtherChannel LACP active/passive, PAgP, load-balance)
│
├── 3. IP Routing & Gateway Redundancy
│   ├── Static & Floating Default Routing (ip route 0.0.0.0 0.0.0.0, AD tuning)
│   ├── Inter-VLAN Routing (Router-on-a-Stick dot1Q subinterfaces & Multilayer SVI)
│   ├── Dynamic Routing: OSPFv2 (router ospf, router-id, network, passive-interface, cost, default-originate)
│   └── Gateway Redundancy: HSRP (standby version 2, virtual IP, priority, preempt, interface tracking)
│
├── 4. IP Services & Translation
│   ├── DHCP Server Pools (network, default-router, dns-server, excluded-address)
│   ├── DHCP Relay Agent (ip helper-address)
│   └── Network Address Translation (Static 1-to-1 NAT & Dynamic PAT Overload)
│
├── 5. Network Security & Infrastructure Hardening
│   ├── Access Control Lists (Standard 1-99, Extended 100-199, Named ACLs, TCP established)
│   ├── Switchport Port Security (mac-address sticky, maximum, violation shutdown/restrict)
│   ├── DHCP Snooping (ip dhcp snooping vlan, trust, rate-limit)
│   └── Dynamic ARP Inspection (DAI - ip arp inspection vlan, trust)
│
└── 6. Verification, Diagnostics & Packet Inspection
    ├── Operational Show Commands (show ip route, show ip int br, show mac address-table, show interfaces trunk)
    ├── Protocol Deep Dives (show ip ospf neighbor, show ip nat translations, show etherchannel summary)
    └── Filtered Debugging & Packet Inspection (debug ip packet <acl_id>, undebug all)
```

---

## 🛠️ Operational Cheat Sheet: Top 15 Daily Commands in a NOC

```bash
# 1. Check all interface physical and protocol states
show ip interface brief

# 2. Check switchport speed, duplex, VLAN, and err-disabled state
show interfaces status

# 3. Check active VLANs and port assignments
show vlan brief

# 4. Check active trunks, native VLAN, and passing VLANs
show interfaces trunk

# 5. Inspect Layer 2 MAC address forwarding table
show mac address-table dynamic

# 6. Check Spanning-Tree Root Bridge and blocked ports
show spanning-tree summary

# 7. Check EtherChannel bundle status (Look for 'SU' and 'P')
show etherchannel summary

# 8. Check active IPv4 Routing Table
show ip route

# 9. Verify OSPF neighbor adjacencies (Look for 'FULL')
show ip ospf neighbor

# 10. Check live inside/outside NAT & PAT translations
show ip nat translations

# 11. Inspect DHCP leases assigned to clients
show ip dhcp binding

# 12. Check ACL hit counters to see which rule is dropping traffic
show access-lists

# 13. Verify HSRP Active/Standby router status
show standby brief

# 14. Discover adjacent Cisco switches and routers
show cdp neighbors detail

# 15. Save running configuration to NVRAM
copy running-config startup-config
```

---
*Created by Manoj M | Network & Security Engineer | Bangalore, India*
