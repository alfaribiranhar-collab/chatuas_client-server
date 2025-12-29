import socket
import threading
from datetime import datetime
import tkinter as tk
from tkinter import scrolledtext, ttk

class ChatClient:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat Client")
        self.root.geometry("750x550")

        self.tabs = ttk.Notebook(root)
        self.tabs.pack(expand=True, fill="both")

        self.text_area = {}
        self.create_tab("All")

        form = tk.Frame(root)
        form.pack(pady=5)

        tk.Label(form, text="Client ID").grid(row=0, column=0)
        self.id_entry = tk.Entry(form)
        self.id_entry.grid(row=0, column=1)

        tk.Label(form, text="Server IP").grid(row=1, column=0)
        self.ip_entry = tk.Entry(form)
        self.ip_entry.grid(row=1, column=1)

        btns = tk.Frame(root)
        btns.pack()

        tk.Button(btns, text="Connect", command=self.connect).pack(side=tk.LEFT, padx=5)
        tk.Button(btns, text="Get Clients", command=self.get_clients).pack(side=tk.LEFT)

        tk.Label(root, text="Online Clients").pack()
        self.client_list = tk.Listbox(root, height=5)
        self.client_list.pack()
        self.client_list.bind("<<ListboxSelect>>", self.open_private)

        self.msg_entry = tk.Entry(root, width=60)
        self.msg_entry.pack(pady=5)
        self.msg_entry.bind("<Return>", self.send_msg)

        self.sock = None
        self.port = 12346

    def create_tab(self, name):
        if name in self.text_area:
            return
        frame = tk.Frame(self.tabs)
        self.tabs.add(frame, text=name)
        box = scrolledtext.ScrolledText(frame)
        box.pack(expand=True, fill="both")
        self.text_area[name] = box

    def log(self, msg, tab="All"):
        self.create_tab(tab)
        time = datetime.now().strftime("%H:%M:%S")
        self.text_area[tab].insert(tk.END, f"[{time}] {msg}\n")
        self.text_area[tab].see(tk.END)

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.ip_entry.get(), self.port))
        self.sock.send(self.id_entry.get().encode())
        self.log("Connected to server")
        threading.Thread(target=self.receive, daemon=True).start()

    def get_clients(self):
        self.sock.send("LIST".encode())

    def open_private(self, event):
        sel = self.client_list.curselection()
        if sel:
            target = self.client_list.get(sel[0])
            self.create_tab(target)
            self.tabs.select(list(self.text_area.keys()).index(target))

    def send_msg(self, event=None):
        msg = self.msg_entry.get()
        if not msg:
            return

        tab = self.tabs.tab(self.tabs.select(), "text")

        if tab == "All":
            self.sock.send(f"ALL:{msg}".encode())
            self.log(f"You: {msg}", "All")
        else:
            self.sock.send(f"TO:{tab}:{msg}".encode())
            self.log(f"You: {msg}", tab)

        self.msg_entry.delete(0, tk.END)

    def receive(self):
        while True:
            try:
                data = self.sock.recv(1024).decode()
                if not data:
                    break

                if data.startswith("CLIENTS:"):
                    self.client_list.delete(0, tk.END)
                    for c in data[8:].split(","):
                        if c != self.id_entry.get():
                            self.client_list.insert(tk.END, c)

                elif data.startswith("FROM:"):
                    _, sender, msg = data.split(":", 2)
                    self.log(f"{sender}: {msg}", sender)

                else:
                    self.log(data, "All")

            except:
                break

if __name__ == "__main__":
    root = tk.Tk()
    ChatClient(root)
    root.mainloop() or "switch to a private tab"
    client_socket.send(error_msg.encode())
    self.log_message(f"Error to {client_id}: {error_msg}")