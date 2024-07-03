import time, socket, kodi
from datetime import datetime, timedelta
import socket

def send_udp_command(command, ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(command.encode(), (ip, port))
    sock.close()
    print(f"udp sent to {ip}:{port} - {command}")

def read_track(file_name):
    commands = []
    with open(file_name, 'r') as file:
        for line in file:
            if line.startswith('#'):
                continue
            timestamp_str, command = line.strip().split(',')
            timestamp = datetime.strptime(timestamp_str, '%H:%M:%S.%f')
            timestamp -= timedelta(seconds=0.3)
            commands.append((timestamp, command))
    return commands

def synchronize_timer():
    current_movie_timestamp_str = kodi.get_current_timestamp()  # Get current timestamp from Kodi
    current_movie_timestamp = datetime.strptime(current_movie_timestamp_str, '%H:%M:%S.%f')
    print(f"Current timestamp: {current_movie_timestamp}")
    return current_movie_timestamp

def execute_commands(commands, ip, port):
    last_command = None

    while True:
        sync_time = synchronize_timer() # synchronize timer with movie timestamp
        
        # Find the command that is just before the current synchronized time
        for i in range(len(commands)):
            if commands[i][0] > sync_time:
                last_command = commands[i-1][1]
                break
            else:
                last_command = None

        if last_command is not None:
            if last_command == "HIGH":
                send_udp_command("on", ip, port)
            elif last_command == "LOW":
                send_udp_command("off", ip, port)
            last_command = None
        
        time.sleep(0.2)

    if 0 == 0:
        # sync_time = synchronize_timer()
        # start_time = datetime.now() - (sync_time - datetime.strptime('00:00:00.000', '%H:%M:%S.%f'))
        # command_active = False

        # for timestamp, command in commands:
        #     current_time = datetime.now()
        #     time_diff = timestamp - datetime.strptime('00:00:00.000', '%H:%M:%S.%f')
        #     wait_time = (start_time + time_diff - current_time).total_seconds()
        #     if wait_time > 0:
        #         time.sleep(wait_time)
        #     print(f'{timestamp.time()} - {command}')
        #     if command == "HIGH":
        #         command_active = True
        #         # send_udp_command("on", ip, port)
        #     elif command == "LOW":
        #         command_active = False
        #         # send_udp_command("off", ip, port)
        #     else:
        #         send_udp_command(command, ip, port)
            
        #     while command_active:
        #         send_udp_command("on", ip, port)
        #         time.sleep(0.5)
        #         send_udp_command("off", ip, port)
        #         time.sleep(0.5)
        #     while command_active == False:
        #         send_udp_command("off", ip, port)
        #         time.sleep(0.5)
        pass

def main():
    file_name = 'umbrella_water.txt'
    file_path = "C:\\Users\\adaxk\\Documents\\Ada\\Python\\4D Theater\\"
    commands = read_track(file_path+file_name)

    esp32_ip = "192.168.0.97"
    esp32_port = 12345

    while True:
        userInput = input("Enter command (toggle, on, off, start): ").lower()
        if userInput in ["toggle", "on", "off"]:
            send_udp_command(userInput, esp32_ip, esp32_port)
        elif userInput == "start":
            execute_commands(commands, esp32_ip, esp32_port)
        else:
            print("Invalid command. Please enter 'toggle' 'on' 'off' 'start")

if __name__ == "__main__":
    main()
