

import socket
import subprocess
import sys
from datetime import datetime
import concurrent.futures
import requests
import tqdm


def scan_port(remote_system_ip, port):
    """
    Scans a single port on the given IP address.
    Returns the port number if open, otherwise None.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)  # Set a timeout for the connection attempt
    result = sock.connect_ex((remote_system_ip, port))
    sock.close()
    if result == 0:
        return port
    return None


def scan_ports(remote_system_ip):
    """
    Scans for open ports on the given IP address.
    Returns a tuple containing the IP address and a list of open ports.
    """
    open_ports = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=10000) as executor:
        futures = []
        for port in range(1, 1024):
            futures.append(executor.submit(scan_port, remote_system_ip, port))

        with tqdm(total=1023, unit="port(s)", desc="Scanning ports", leave=False) as pbar:
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                if result is not None:
                    open_ports.append(result)
                pbar.update(1)

    return remote_system_ip, open_ports


def get_remote_system_info(remote_system):
    """
    Retrieves the IP address of the remote system and performs port scanning.
    Returns a list of IP addresses in the local network along with their open ports.
    """
    try:
        ip_addresses = []
        network_prefix = remote_system.rsplit(".", 1)[0] + "."

        with tqdm(total=255, unit="host(s)", desc="Scanning hosts") as pbar:
            for host in range(1, 256):
                ip_address = network_prefix + str(host)
                ip_address, open_ports = scan_ports(ip_address)

                if open_ports:
                    ip_addresses.append((ip_address, open_ports))
                    print("Open ports on {}: {}".format(ip_address, open_ports))

                pbar.update(1)

        return ip_addresses

    except socket.gaierror:
        print("Invalid IP address or network range. Please enter a valid IP address or network prefix.")
        sys.exit()


def get_known_vulnerabilities(vulnerability_type, identifier):
    """
    Retrieves known vulnerabilities from a vulnerability database or API.
    Returns a list of vulnerabilities associated with the given type and identifier.
    Each vulnerability is represented as a tuple containing (vulnerability_name, rating).
    """
    vulnerabilities = []
    # Perform API or database lookup based on vulnerability_type and identifier
    # Example:
    # if vulnerability_type == "OS":
    #     vulnerabilities = perform_os_vulnerability_lookup(identifier)
    # elif vulnerability_type == "Port":
    #     vulnerabilities = perform_port_vulnerability_lookup(identifier)
    # ...

    # Dummy data for demonstration
    if identifier == "OS":
        vulnerabilities = [("CVE-2021-1234", "Critical"), ("CVE-2021-5678", "High")]
    elif vulnerability_type == "Port":
        vulnerabilities = [("CVE-2022-4321", "Medium"), ("CVE-2022-8765", "Low")]

    return vulnerabilities


def scan_software_and_os(remote_system_ips):
    """
    Scans the software and operating system version running on the given IP addresses.
    """
    try:
        print()
        print("Scanning software and OS version on IP addresses:", remote_system_ips)
        print()

        for ip_address, open_ports in remote_system_ips:
            # Perform scanning for software and OS version here

            print("IP Address:", ip_address)

            # Get known vulnerabilities for the OS
            os_vulnerabilities = get_known_vulnerabilities("OS", ip_address)
            if os_vulnerabilities:
                print("Known vulnerabilities related to the OS on {}: ".format(ip_address))
                for vulnerability, rating in os_vulnerabilities:
                    print("Vulnerability:", vulnerability)
                    print("Rating:", rating)
                    print("Operating System:", get_operating_system(ip_address))
                    print()

            # Get known vulnerabilities for open ports
            print("Open Ports:")
            for port in tqdm(open_ports, desc="Scanning port vulnerabilities"):
                print("Port:", port)
                port_vulnerabilities = get_known_vulnerabilities("Port", port)

                if port_vulnerabilities:
                    print("Known vulnerabilities related to port {} on {}: ".format(port, ip_address))
                    for vulnerability, rating in port_vulnerabilities:
                        print("Vulnerability:", vulnerability)
                        print("Rating:", rating)
                        print("Application:", get_application(port))
                        print()

            print()

    except Exception as e:
        print("Error occurred while scanning:", str(e))


# Helper functions to retrieve operating system and application information
def get_operating_system(ip_address):
    # Perform OS version lookup based on IP address
    # Return the operating system name or version
    return "Operating System"

def get_application(port):
    # Perform application lookup based on port number
    # Return the application name or description
    return "Application"


def main():
    subprocess.call('clear', shell=True)
    remote_system = input("Enter an IP address or network prefix to scan (e.g., 10.100.10.0/24): ")

    remote_system_ips = get_remote_system_info(remote_system)

    if remote_system_ips:
        scan_software_and_os(remote_system_ips)

    endTime = datetime.now()
    difftime = endTime - startTime
    print('Time to complete operation:', difftime)


if __name__ == '__main__':
    startTime = datetime.now()
    main()
