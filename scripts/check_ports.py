"""
Check if required ports are available
"""
import socket
import sys


def check_port(port, host="127.0.0.1"):
    """Check if a port is available"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    result = sock.connect_ex((host, port))
    sock.close()
    return result != 0  # True if port is available


def main():
    """Check all required ports"""
    ports = {
        "Flower Server": 8080,
        "Server Monitoring API": 8082,
        "Client 1 API": 8081,
        "Client 2 API": 8083,
        "Client 3 API": 8084,
    }
    
    print("=" * 70)
    print("Checking Port Availability")
    print("=" * 70)
    print()
    
    all_available = True
    for name, port in ports.items():
        available = check_port(port)
        status = "[AVAILABLE]" if available else "[OCCUPIED]"
        print(f"{name:25} Port {port:5} {status}")
        if not available:
            all_available = False
    
    print()
    print("=" * 70)
    if all_available:
        print("All ports are available!")
    else:
        print("Some ports are occupied. Please free them or change configuration.")
        print("\nTo find what's using a port (Windows):")
        print("  netstat -ano | findstr :8080")
    print("=" * 70)
    
    return 0 if all_available else 1


if __name__ == "__main__":
    sys.exit(main())

