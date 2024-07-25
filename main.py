import os
import sys
import subprocess
import importlib.util
import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox

# List of required modules
required_modules = [
    'tkinter',
]

def check_and_install_modules():
    """Check for required modules and install missing ones."""
    missing_modules = []

    # Check for each required module
    for module in required_modules:
        if importlib.util.find_spec(module) is None:
            missing_modules.append(module)
    
    if missing_modules:
        print(f"Missing modules: {', '.join(missing_modules)}")
        print("Since tkinter is a standard library module, ensure you have a complete Python installation.")
        sys.exit(1)

# Default Parameters
DEFAULT_PORT = 21
DEFAULT_HOST = '127.0.0.1'

# Globals for client and server
clients = []
nicknames = []
nickname = None
client = None
server_thread = None
receive_thread = None
chat_area = None
host = DEFAULT_HOST
port = DEFAULT_PORT

# Broadcast message to all clients
def broadcast(message):
    for client in clients:
        try:
            client.send(message)
        except:
            clients.remove(client)
    print(f"Broadcasting message: {message}")

# Handle individual client connection
def handle_client(client):
    while True:
        try:
            # Receive message from client
            message = client.recv(1024)
            if not message:
                break
            broadcast(message)
        except Exception as e:
            print(f"Error handling client: {e}")
            break
    if client in clients:
        index = clients.index(client)
        clients.remove(client)
        client.close()
        nickname = nicknames[index]
        broadcast(f'{nickname} left the chat!'.encode('ascii'))
        nicknames.remove(nickname)

# Receive and accept client connections
def receive():
    global host, port
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()
    print(f'Server running on {host}:{port}')

    while True:
        client, address = server.accept()
        print(f'Connected with {str(address)}')

        # Request and store nickname
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        print(f'Nickname of the client is {nickname}')
        broadcast(f'{nickname} joined the chat!'.encode('ascii'))
        client.send('Connected to the server!'.encode('ascii'))

        # Start handling thread for client
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

# Start the server
def start_server():
    global server_thread
    server_thread = threading.Thread(target=receive, daemon=True)
    server_thread.start()
    messagebox.showinfo("Server Info", f"Server started on {host}:{port}")

def connect_to_server():
    global nickname
    global client
    global receive_thread

    nickname = entry_nickname.get()
    if not nickname:
        messagebox.showwarning("Warning", "Please enter a nickname")
        return

    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((host, port))
        client.send(nickname.encode('ascii'))
        main_window.withdraw()
        open_chat_window(is_server=False)
    except socket.gaierror:
        messagebox.showerror("Connection Error", "Could not resolve the server address. Please check the server IP.")
        client = None
    except Exception as e:
        messagebox.showerror("Connection Error", str(e))
        print(f"Connection error: {e}")
        client = None

def receive_message():
    global client
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
            else:
                chat_area.config(state=tk.NORMAL)
                chat_area.insert(tk.END, message + '\n')
                chat_area.yview(tk.END)
                chat_area.config(state=tk.DISABLED)
        except Exception as e:
            print(f"Error receiving message: {e}")
            if client:
                client.close()
            client = None
            break

def send_message():
    global client
    if client:
        try:
            message = f'{nickname}: {entry_message.get()}'
            client.send(message.encode('ascii'))
            print(f"Sent message: {message}")
            entry_message.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Send Error", str(e))
            print(f"Send error: {e}")
            if client:
                client.close()
            client = None
    else:
        messagebox.showerror("Connection Error", "You are not connected to a server.")

def open_chat_window(is_server=False):
    global chat_area, entry_message

    chat_window = tk.Tk()
    chat_window.title("Chat Room")

    chat_area = scrolledtext.ScrolledText(chat_window, state='disabled')
    chat_area.pack(padx=20, pady=20)

    entry_message = tk.Entry(chat_window)
    entry_message.pack(padx=20, pady=10)

    send_button = tk.Button(chat_window, text="Send", command=send_message)
    send_button.pack(padx=20, pady=10)
    
    if is_server:
        server_label = tk.Label(chat_window, text="Server is running...")
        server_label.pack(padx=20, pady=10)
    
    leave_button = tk.Button(chat_window, text="Leave Chat Room", command=lambda: leave_chat_room(chat_window))
    leave_button.pack(padx=20, pady=10)

    chat_window.protocol("WM_DELETE_WINDOW", lambda: leave_chat_room(chat_window))
    receive_thread = threading.Thread(target=receive_message, daemon=True)
    receive_thread.start()
    chat_window.mainloop()

def leave_chat_room(chat_window):
    global client
    if client:
        client.close()
    chat_window.destroy()
    main_window.deiconify()

def configure_settings():
    global host, port

    settings_window = tk.Toplevel(main_window)
    settings_window.title("Settings")

    tk.Label(settings_window, text="Server IP:").pack(padx=20, pady=5)
    ip_entry = tk.Entry(settings_window)
    ip_entry.insert(0, host)
    ip_entry.pack(padx=20, pady=5)

    tk.Label(settings_window, text="Port:").pack(padx=20, pady=5)
    port_entry = tk.Entry(settings_window)
    port_entry.insert(0, port)
    port_entry.pack(padx=20, pady=5)

    def save_settings():
        global host, port
        host = ip_entry.get()
        port = int(port_entry.get())
        settings_window.destroy()

    save_button = tk.Button(settings_window, text="Save", command=save_settings)
    save_button.pack(pady=20)

def on_closing():
    global client
    if client:
        client.close()
    main_window.quit()

# Create the main window
def create_main_window():
    global main_window, entry_nickname

    main_window = tk.Tk()
    main_window.title("WiFi Chatting Application")

    server_frame = tk.Frame(main_window)
    server_frame.pack(padx=20, pady=20)

    client_frame = tk.Frame(main_window)
    client_frame.pack(padx=20, pady=20)

    tk.Label(server_frame, text="Server Setup").pack(pady=10)
    start_server_button = tk.Button(server_frame, text="Start Server", command=start_server)
    start_server_button.pack(pady=5)

    tk.Label(client_frame, text="Client Setup").pack(pady=10)
    tk.Label(client_frame, text="Nickname:").pack(pady=5)
    entry_nickname = tk.Entry(client_frame)
    entry_nickname.pack(pady=5)

    connect_button = tk.Button(client_frame, text="Connect to Server", command=connect_to_server)
    connect_button.pack(pady=5)

    settings_button = tk.Button(main_window, text="Settings", command=configure_settings)
    settings_button.pack(pady=5)

    main_window.protocol("WM_DELETE_WINDOW", on_closing)
    main_window.mainloop()

if __name__ == "__main__":
    check_and_install_modules()
    create_main_window()
