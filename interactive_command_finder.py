"""
Cisco CCNA 200-301 Master Command Search Engine
Author: Manoj M (Network & Security Engineer)

Usage:
  python interactive_command_finder.py              # Interactive mode
  python interactive_command_finder.py ospf         # Search for OSPF commands
  python interactive_command_finder.py trunk        # Search for trunking commands
  python interactive_command_finder.py nat          # Search for NAT/PAT commands
"""

import sys

COMMAND_DATABASE = [
    {
        "domain": "Router - Routing",
        "topic": "OSPFv2",
        "mode": "Global Configuration -> Router Config",
        "command": "router ospf <process-id>\n router-id <x.x.x.x>\n network <network-ip> <wildcard-mask> area <area-id>",
        "desc": "Enables OSPF routing process, assigns 32-bit router ID, and enables OSPF on matching interfaces."
    },
    {
        "domain": "Router - Routing",
        "topic": "OSPF Passive Interface",
        "mode": "Router Configuration",
        "command": "passive-interface <interface-name>\npassive-interface default",
        "desc": "Suppresses OSPF Hello multicasts on LAN interfaces to prevent unnecessary traffic and security exposure."
    },
    {
        "domain": "Router - Routing",
        "topic": "OSPF Default Route Propagation",
        "mode": "Router Configuration",
        "command": "default-information originate [always]",
        "desc": "Floods a Type-5 LSA advertising a gateway of last resort (default route) to all OSPF neighbors."
    },
    {
        "domain": "Router - Routing",
        "topic": "Static & Default Routing",
        "mode": "Global Configuration",
        "command": "ip route <network> <mask> <next-hop-ip | exit-interface> [distance]",
        "desc": "Configures a static route. Set network/mask to 0.0.0.0 0.0.0.0 for a default route. Distance > 1 creates a floating backup route."
    },
    {
        "domain": "Router - Inter-VLAN",
        "topic": "Router-on-a-Stick (802.1Q)",
        "mode": "Subinterface Configuration",
        "command": "interface <phy_int>.<vlan_id>\n encapsulation dot1Q <vlan_id> [native]\n ip address <ip> <mask>",
        "desc": "Creates a logical subinterface to route traffic between 802.1Q tagged VLANs over a single physical trunk link."
    },
    {
        "domain": "Router - IP Services",
        "topic": "DHCP Server Pool",
        "mode": "Global Configuration",
        "command": "ip dhcp excluded-address <low_ip> <high_ip>\nip dhcp pool <POOL_NAME>\n network <net> <mask>\n default-router <gateway_ip>\n dns-server <dns1> <dns2>",
        "desc": "Configures Cisco IOS as a local DHCP server with dynamic pool allocations and exclusions."
    },
    {
        "domain": "Router - IP Services",
        "topic": "DHCP Relay Agent",
        "mode": "Interface Configuration",
        "command": "ip helper-address <central_dhcp_server_ip>",
        "desc": "Converts client DHCP broadcast requests into unicast packets routed to a remote DHCP server."
    },
    {
        "domain": "Router - Security/NAT",
        "topic": "PAT / NAT Overload",
        "mode": "Global & Interface Configuration",
        "command": "interface <lan_if>\n ip nat inside\ninterface <wan_if>\n ip nat outside\nip access-list standard NAT_ACL\n permit <internal_subnet> <wildcard>\nip nat inside source list NAT_ACL interface <wan_if> overload",
        "desc": "Translates multiple internal private IP addresses to a single public IP using unique TCP/UDP port numbers."
    },
    {
        "domain": "Router - Security/NAT",
        "topic": "Static 1-to-1 NAT",
        "mode": "Global Configuration",
        "command": "ip nat inside source static <private_ip> <public_ip>",
        "desc": "Creates a permanent bidirectional mapping between an internal server and an external public IP."
    },
    {
        "domain": "Router & Switch - Security",
        "topic": "Extended Access Control List",
        "mode": "Global Configuration",
        "command": "ip access-list extended <ACL_NAME>\n permit tcp <src_net> <src_wc> host <dst_ip> eq 443\n permit tcp any any established\n deny ip any any log\ninterface <int>\n ip access-group <ACL_NAME> in",
        "desc": "Filters traffic based on source, destination, protocol (TCP/UDP/ICMP), and port numbers with stateful inspection support."
    },
    {
        "domain": "Switch - VLANs",
        "topic": "VLAN Creation & Access Port",
        "mode": "Global & Interface Configuration",
        "command": "vlan <vlan_id>\n name <VLAN_NAME>\ninterface <fast/gig_int>\n switchport mode access\n switchport access vlan <vlan_id>",
        "desc": "Creates a Layer 2 broadcast domain and assigns an access switchport to that VLAN."
    },
    {
        "domain": "Switch - Trunking",
        "topic": "802.1Q Trunk Port",
        "mode": "Interface Configuration",
        "command": "interface <gig_int>\n switchport mode trunk\n switchport trunk native vlan <native_id>\n switchport trunk allowed vlan <list>\n switchport nonegotiate",
        "desc": "Configures an interface to carry multi-VLAN traffic across switches, setting native VLAN and disabling DTP."
    },
    {
        "domain": "Switch - Spanning Tree",
        "topic": "Rapid-PVST & Root Primacy",
        "mode": "Global Configuration",
        "command": "spanning-tree mode rapid-pvst\nspanning-tree vlan <id> root primary\nspanning-tree portfast default\nspanning-tree portfast bpduguard default",
        "desc": "Enables 802.1w Rapid Spanning Tree, tunes root bridge priority, and enables edge port fast forwarding and BPDU protection."
    },
    {
        "domain": "Switch - EtherChannel",
        "topic": "LACP Port Channel Bundle",
        "mode": "Interface Range Configuration",
        "command": "interface range <if1> - <if2>\n channel-group <id> mode active\ninterface port-channel <id>\n switchport mode trunk",
        "desc": "Aggregates physical links into a single logical high-bandwidth trunk using industry standard IEEE 802.3ad LACP."
    },
    {
        "domain": "Switch - Layer 3",
        "topic": "Switch Virtual Interface (SVI)",
        "mode": "Global & Interface Configuration",
        "command": "ip routing\ninterface vlan <vlan_id>\n ip address <ip> <mask>\n no shutdown",
        "desc": "Enables hardware IP routing on a multilayer switch and provides default gateway routing directly on the switch."
    },
    {
        "domain": "Switch - Security",
        "topic": "Port Security (Sticky MAC)",
        "mode": "Interface Configuration",
        "command": "interface <access_if>\n switchport mode access\n switchport port-security\n switchport port-security maximum 2\n switchport port-security mac-address sticky\n switchport port-security violation restrict",
        "desc": "Prevents MAC address flooding and unauthorized hardware connections by dynamically locking learned MACs to switchports."
    },
    {
        "domain": "Switch - Security",
        "topic": "DHCP Snooping & DAI",
        "mode": "Global & Interface Configuration",
        "command": "ip dhcp snooping\nip dhcp snooping vlan <vlans>\nip arp inspection vlan <vlans>\ninterface <uplink_if>\n ip dhcp snooping trust\n ip arp inspection trust",
        "desc": "Blocks rogue DHCP servers and prevents ARP cache poisoning attacks across enterprise access switches."
    },
    {
        "domain": "Router & Switch - Management",
        "topic": "SSHv2 Configuration",
        "mode": "Global & Line Configuration",
        "command": "ip domain-name <domain>\ncrypto key generate rsa modulus 2048\nip ssh version 2\nusername <user> privilege 15 secret <pass>\nline vty 0 4\n transport input ssh\n login local",
        "desc": "Secures management planes with encrypted SSHv2 access, replacing legacy clear-text Telnet."
    }
]

def search_commands(query):
    query = query.lower()
    matches = [c for c in COMMAND_DATABASE if query in c["topic"].lower() or query in c["command"].lower() or query in c["desc"].lower() or query in c["domain"].lower()]
    
    print("\n" + "="*75)
    print(f"🔎 CCNA COMMAND SEARCH RESULTS FOR: '{query}' ({len(matches)} matches)")
    print("="*75)
    
    if not matches:
        print("No exact matches found. Try searching: ospf, vlan, trunk, nat, dhcp, acl, ssh, hsrp, lacp")
        return
        
    for i, c in enumerate(matches, 1):
        print(f"\n[{i}] Category: {c['domain']} | Topic: {c['topic']}")
        print(f"    Mode: {c['mode']}")
        print(f"    Commands:\n{indent(c['command'], '      ')}")
        print(f"    Explanation: {c['desc']}")
        print("-" * 75)

def indent(text, prefix):
    return "\n".join(prefix + line for line in text.split("\n"))

if __name__ == "__main__":
    if len(sys.argv) > 1:
        search_commands(" ".join(sys.argv[1:]))
    else:
        print("Cisco CCNA Interactive Command Finder")
        print("Type 'exit' or 'q' to quit.\n")
        while True:
            try:
                q = input("Search CCNA Command (e.g. ospf, trunk, nat): ").strip()
                if q.lower() in ["exit", "q"]:
                    break
                if q:
                    search_commands(q)
            except (KeyboardInterrupt, EOFError):
                break
