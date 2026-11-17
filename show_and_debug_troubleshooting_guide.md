# 🔍 Cisco IOS Show & Debug Troubleshooting Guide (CCNA 200-301)
**Author:** Manoj M | Network & Security Engineer  
**Scope:** Production-grade verification, packet dissection, and diagnostic runbooks for Cisco Routers & Catalyst Switches.

---

## 📌 Part 1: Essential Verification Commands & Output Decoding

### 1. `show ip interface brief`
Used on routers and multilayer switches to get an instant snapshot of all Layer 3 interfaces.
```text
Interface              IP-Address      OK? Method Status                Protocol
GigabitEthernet0/0/0   203.0.113.2     YES NVRAM  up                    up      
GigabitEthernet0/0/1   unassigned      YES unset  up                    up      
GigabitEthernet0/0/1.10 10.10.10.1     YES manual up                    up      
GigabitEthernet0/0/2   192.168.1.1     YES manual administratively down down    
```
- **Status = up, Protocol = up**: Layer 1 (Physical/Cable) is Good; Layer 2 (Data Link/Keepalives/Framing) is Good.
- **Status = up, Protocol = down**: Layer 1 is physical link detected, but Layer 2 encapsulation mismatch, clock rate missing, or keepalive timeout.
- **Status = down, Protocol = down**: Cable unplugged, faulty SFP transceiver, or remote device is powered off.
- **Status = administratively down, Protocol = down**: Interface is disabled with the `shutdown` command. Run `no shutdown`.

---

### 2. `show interfaces status` (Switches)
Quickly verify port speed, duplex, VLAN membership, and operational state.
```text
Port      Name               Status       Vlan       Duplex  Speed Type
Fa0/1     ENG_DESKTOP_01     connected    10         a-full  a-100 10/100BaseTX
Fa0/2     FIN_PRINTER_01     connected    20         a-full  a-100 10/100BaseTX
Gi0/1     TRUNK_TO_ROUTER    connected    trunk      full    1000  1000BaseTX
Fa0/24    UNUSED             notconnect   1          auto    auto  10/100BaseTX
Fa0/5     SECURITY_VIOLATION err-disabled 10         auto    auto  10/100BaseTX
```
> [!NOTE]
> If a port is in **`err-disabled`** state, it was shut down by a security feature (e.g., Port Security violation, BPDU Guard trigger, or duplex mismatch).  
> **Recovery:** Go to the interface and execute `shutdown` followed by `no shutdown`.

---

### 3. `show interfaces trunk`
Verifies 802.1Q trunk links between switches and routers.
```text
Port        Mode             Encapsulation  Status        Native vlan
Gi0/1       on               802.1q         trunking      99

Port        Vlans allowed on trunk
Gi0/1       10,20,30,99,150

Port        Vlans allowed and active in management domain
Gi0/1       10,20,30,99,150

Port        Vlans in spanning tree forwarding state and not pruned
Gi0/1       10,20,30,99,150
```
- **Native VLAN Mismatch Warning:** If Switch A has native VLAN 99 and Switch B has native VLAN 1, CDP will generate continuous error logs (`%CDP-4-NATIVE_VLAN_MISMATCH`). Both sides MUST match.

---

### 4. `show ip route`
Decodes the IPv4 routing table.
```text
Codes: L - local, C - connected, S - static, R - RIP, M - mobile, B - BGP
       D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area 
       * - candidate default, U - per-user static route, o - ODR

Gateway of last resort is 203.0.113.1 to network 0.0.0.0

S*    0.0.0.0/0 [1/0] via 203.0.113.1
O     10.10.30.0/24 [110/2] via 10.10.99.2, 00:14:22, GigabitEthernet0/0/1.99
C     10.10.10.0/24 is directly connected, GigabitEthernet0/0/1.10
L     10.10.10.1/32 is directly connected, GigabitEthernet0/0/1.10
```
- **Administrative Distance (AD) Reference:**
  - Connected: `0`
  - Static: `1`
  - eBGP: `20`
  - EIGRP (Internal): `90`
  - OSPF: `110`
  - IS-IS: `115`
  - RIP: `120`
  - iBGP: `200`
- `[110/2]`: `110` is Administrative Distance; `2` is OSPF Metric (Cost).

---

### 5. `show ip ospf neighbor`
Verifies OSPF dynamic adjacency states.
```text
Neighbor ID     Pri   State           Dead Time   Address         Interface
2.2.2.2           1   FULL/DR         00:00:34    10.10.99.2      GigabitEthernet0/0/1.99
```
- **Expected Steady State:** `FULL/DR`, `FULL/BDR`, or `FULL/DROTHER` (on broadcast networks) or `FULL/-` (on point-to-point networks).
- **Troubleshooting OSPF Neighbor Issues:**
  - Stuck in **`INIT`**: Local router received Hello, but remote router did not see local router in its neighbor list (unidirectional link or ACL blocking OSPF multicast `224.0.0.5`).
  - Stuck in **`2-WAY`**: Normal between two DROTHER routers on a shared multi-access network (they only form FULL adjacencies with DR and BDR).
  - Stuck in **`EXSTART / EXCHANGE`**: **MTU Mismatch!** OSPF DBD packets fail to negotiate because interface MTU sizes do not match on both ends.

---

### 6. `show ip nat translations`
Displays active NAT and PAT translation tables in RAM.
```text
Pro Inside global         Inside local          Outside local         Outside global
tcp 203.0.113.2:49152     10.10.10.25:49152     142.250.190.46:443    142.250.190.46:443
udp 203.0.113.2:53211     10.10.20.14:53211     8.8.8.8:53            8.8.8.8:53
--- 203.0.113.10          10.10.10.50           ---                   ---
```
- Line 1 & 2: Dynamic PAT sessions showing internal source port mapped to external public IP.
- Line 3: Static 1-to-1 NAT entry for internal server (`10.10.10.50`).

---

### 7. `show etherchannel summary`
Verifies aggregated port channel bundles.
```text
Group  Port-channel  Protocol    Ports
------+-------------+-----------+-----------------------------------------------
1      Po1(SU)         LACP      Gi0/3(P)    Gi0/4(P)
```
- **Flag `S`**: Layer 2 port-channel.
- **Flag `U`**: In-use / Up (Healthy).
- **Flag `P`**: Physical port is bundled in port-channel (Active member).
- **Flag `D`**: Down (Misconfiguration: speed, duplex, trunk mode, or native VLAN mismatch between member ports).

---

## 📌 Part 2: Safe Debug Commands (NOC Safety Protocols)

> [!CAUTION]
> **Production Rule:** Never run plain `debug ip packet` or `debug all` on a live production router under heavy traffic! It can spike CPU utilization to 100% and crash the control plane. Always filter debugs with an Access Control List.

### Safe Debugging Example: Filtered ICMP Debugging
```bash
! Step 1: Create an ACL matching only the test traffic
access-list 199 permit icmp host 10.10.10.1 host 8.8.8.8

! Step 2: Enable debug filtered by ACL 199
debug ip packet 199 detail

! Step 3: Run your ping test from host

! Step 4: Immediately disable all debugging
undebug all
! or shorthand:
un all
```

---

## 📌 Part 3: Top 5 Real-World Incident Runbooks

### Runbook 1: Host Has No Internet Connectivity
1. Check physical connection on client: `ipconfig /all`. Verify IP, Subnet Mask, and Default Gateway.
2. Ping local gateway (`10.10.10.1`). If fails -> Layer 2 issue (port in wrong VLAN, port security violation, bad cable).
3. Ping upstream router / ISP IP (`203.0.113.1`). If fails -> Routing table missing default route (`show ip route`).
4. Ping public IP (`8.8.8.8`). If fails -> NAT failure (`show ip nat translations`).
5. Ping domain name (`google.com`). If fails but ping to 8.8.8.8 works -> DNS resolution failure. Check DHCP DNS server options.

### Runbook 2: Inter-VLAN Routing Failure
1. On switch: Verify host port is in the correct VLAN: `show mac address-table vlan <id>`.
2. On switch: Verify uplink trunk is active and passing the VLAN: `show interfaces trunk`.
3. On router: Verify subinterface has 802.1Q encapsulation and IP assigned: `show ip interface brief`.
4. Check if an Inbound ACL is dropping traffic between subnets: `show access-lists`.
