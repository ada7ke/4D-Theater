import socket

def send_udp_command(command, ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(command.encode(), (ip, port))
    sock.close()

if __name__ == "__main__":
    esp32_ip = "192.168.0.97"  # Replace with your ESP32 IP address
    esp32_port = 12345          # Use the same port as defined in the ESP32 program
    
    while True:
        command = input("Enter command (toggle, on, off): ")
        if command in ["toggle", "on", "off"]:
            send_udp_command(command, esp32_ip, esp32_port)
        else:
            print("Invalid command. Please enter 'toggle' 'on' or 'off'.")

