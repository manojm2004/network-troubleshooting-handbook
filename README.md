# 🌐 Enterprise Network Operations Center (NOC) Troubleshooting Handbook

A comprehensive, production-oriented reference manual for L1/L2 Network Engineers and NOC Analysts.

## 📌 Contents
1. **OSI Layered Troubleshooting Methodology**
2. **Cisco IOS Diagnostic Quick-Reference**
3. **Palo Alto Firewall Traffic Verification**
4. **Packet-Level Inspection with Wireshark**
5. **Common Incident Runbooks (VLAN / OSPF / MTU)**

---

## 🚀 Diagnostic Commands Cheat Sheet
### Layer 1 & 2 (Physical & Data Link)
`ash
show ip interface brief
show interfaces status
show interfaces trunk
show mac address-table
show spanning-tree
`

### Layer 3 (Network Layer)
`ash
show ip route
show ip route ospf
show ip ospf neighbor
show ip arp
ping <destination> repeat 100 size 1400
traceroute <destination>
`

### Layer 4 - 7 (Transport & Application)
`ash
show ip nat translations
show access-lists
telnet <ip> <port>
`

---
*Maintained by Manoj M | Network & Security Engineer*