import tkinter as tk
from tkinter import scrolledtext

class TerminalFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.terminal_output = scrolledtext.ScrolledText(self, bg="black", fg="#33ff33", font=("Consolas", 12))
        self.terminal_output.pack(fill=tk.BOTH, expand=True)

        self.terminal_input = tk.Entry(self, bg="#111", fg="#33ff33", font=("Consolas", 12), insertbackground="#33ff33")
        self.terminal_input.pack(fill=tk.X)
        self.terminal_input.bind("<Return>", self.process_command)

        # Estado ficticio
        self.servers = {
            "11231": {
                "name": "Qoogle",
                "passwords": ["lem0nP@ssw0rd", "s3gur1d4dfac1l", "m1n1m4l1sm0", "PlusWithYou"],
                "mails": ["luis@moc", "ana@moc", "carlos@moc", "plusstudiosofficial@gmail.com"],
                "files": {
                    "contraseñas.txt": "lem0nP@ssw0rd\ns3gur1d4dfac1l\nm1n1m4l1sm0\nPlusWithYou",
                    "config.sys": "system=active\nsecurity=high\nbackup=enabled",
                    "logs.log": "01/06/2025: Login success\n02/06/2025: Password changed"
                }
            },
            "44556": {
                "name": "Lemovo",
                "passwords": ["p4sSw0rdLem0vo", "lemov0s3guro", "teclad0segur0"],
                "mails": ["maria@moc", "jose@moc", "carmen@moc"],
                "files": {
                    "contraseñas.txt": "p4sSw0rdLem0vo\nlemov0s3guro\nteclad0segur0",
                    "config.sys": "system=standby\nsecurity=medium\nbackup=disabled",
                    "logs.log": "03/06/2025: System reboot\n04/06/2025: Firewall enabled"
                }
            }
        }

        self.connected_ip = None
        self.connected_server = None

        self.print_welcome()

    def print_welcome(self):
        self.write(" ===== Terminal Hak_OS =====")
        self.write("Escribe help() para comenzar.")

    def write(self, text):
        self.terminal_output.insert(tk.END, text + "\n")
        self.terminal_output.see(tk.END)

    def process_command(self, event):
        cmd = self.terminal_input.get().strip()
        if not cmd:
            return
        self.write(f"> {cmd}")
        self.terminal_input.delete(0, tk.END)
        try:
            response = self.handle_command(cmd)
            if response:
                self.write(response)
        except Exception as e:
            self.write(f"ERROR interno: {e}")

    def handle_command(self, cmd):
        cmd_lower = cmd.lower()

        if cmd_lower == "help()":
            return (
                "Comandos disponibles:\n"
                "entry('IP')\nconnect('Servidor', 'pass')\nscan_servers()\n"
                "list_mails()\nread_mail('correo')\nls_files()\ncat_file('archivo')\n"
                "shutdownserversof('IP')\nclear()\nwhoami()\ngetip()\nlistservers()\n"
                "ping('IP')\ntrace('IP')\nscanports('IP')\nlistprocesses()\n"
                "killprocess('nombre')\ngetosinfo()\ngetusers()\ncreatefile('archivo')\n"
                "deletefile('archivo')\nexit()"
            )

        if cmd_lower.startswith("entry("):
            ip = self.extract_arg(cmd)
            if ip in self.servers:
                self.connected_ip = ip
                return f"Conectado a {self.servers[ip]['name']} (IP: {ip})"
            return "ERROR: IP no encontrada."

        if cmd_lower == "scan_servers()":
            return self.list_servers()

        if cmd_lower.startswith("connect("):
            args = self.extract_args(cmd)
            if len(args) != 2:
                return "Uso: connect('Server', 'password')"
            if not self.connected_ip:
                return "ERROR: No conectado a ningún servidor."
            if "pass" in args[1].lower():
                self.connected_server = args[0]
                return f"Conectado al servidor {args[0]}"
            return "Contraseña incorrecta."

        if cmd_lower == "list_mails()":
            return "\n".join(self.servers[self.connected_ip]["mails"]) if self.connected_ip else "ERROR: No conectado."

        if cmd_lower.startswith("read_mail("):
            mail = self.extract_arg(cmd)
            return f"Mensaje de {mail}: Cambia tu contraseña urgente." if self.connected_ip and mail in self.servers[self.connected_ip]["mails"] else "ERROR: Mail no encontrado."

        if cmd_lower == "ls_files()":
            return "\n".join(self.servers[self.connected_ip]["files"].keys()) if self.connected_ip else "ERROR: No conectado."

        if cmd_lower.startswith("cat_file("):
            filename = self.extract_arg(cmd)
            files = self.servers[self.connected_ip]["files"] if self.connected_ip else {}
            return files.get(filename, "ERROR: Archivo no encontrado.")

        if cmd_lower.startswith("shutdownserversof("):
            ip = self.extract_arg(cmd)
            return f"Apagando {self.servers[ip]['name']}... OK" if ip in self.servers else "ERROR: IP no válida."

        if cmd_lower == "clear()":
            self.terminal_output.delete('1.0', tk.END)
            return ""

        if cmd_lower == "whoami()":
            return "hacker@pc_virtual"

        if cmd_lower == "getip()":
            return f"IP actual: {self.connected_ip}" if self.connected_ip else "No conectado."

        if cmd_lower == "listservers()":
            return self.list_servers()

        if cmd_lower.startswith("ping("):
            ip = self.extract_arg(cmd)
            return f"Ping a {ip} -> OK"

        if cmd_lower.startswith("trace("):
            ip = self.extract_arg(cmd)
            return f"1 -> 192.168.0.1\n2 -> 10.0.0.1\n3 -> {ip}"

        if cmd_lower.startswith("scanports("):
            ip = self.extract_arg(cmd)
            return f"Escaneando puertos en {ip}: 80 abierto, 443 abierto"

        if cmd_lower == "listprocesses()":
            return "systemd\npython3\nbash\nexplorer.exe"

        if cmd_lower.startswith("killprocess("):
            proc = self.extract_arg(cmd)
            return f"Proceso '{proc}' terminado."

        if cmd_lower == "getosinfo()":
            return "+Studios OS v1.0.0 - Kernel H4kSim"

        if cmd_lower == "getusers()":
            return "admin\nroot\nguest"

        if cmd_lower.startswith("createfile("):
            filename = self.extract_arg(cmd)
            self.servers[self.connected_ip]["files"][filename] = ""
            return f"Archivo '{filename}' creado."

        if cmd_lower.startswith("deletefile("):
            filename = self.extract_arg(cmd)
            if filename in self.servers[self.connected_ip]["files"]:
                del self.servers[self.connected_ip]["files"][filename]
                return f"Archivo '{filename}' eliminado."
            return "Archivo no encontrado."

        if cmd_lower == "exit()":
            return "Para cerrar, usa la ventana del sistema."

        return "Comando no reconocido. Usa help()"

    def extract_arg(self, cmd):
        try:
            return cmd[cmd.index("(")+1 : cmd.rindex(")")].strip("'\"")
        except:
            return ""

    def extract_args(self, cmd):
        try:
            args = cmd[cmd.index("(")+1 : cmd.rindex(")")].split(",")
            return [arg.strip().strip("'\"") for arg in args]
        except:
            return []

    def list_servers(self):
        return "\n".join([f"{data['name']} ({ip})" for ip, data in self.servers.items()])
