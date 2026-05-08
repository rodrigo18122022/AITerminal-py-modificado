import tkinter as tk
from tkinter import ttk
import asyncio
import traceback
import sys
import os
import threading
import shutil
import getpass
import ast
import operator

from io import StringIO
from datetime import datetime

from libraries.ai import ArtificialInteligence


class ConsoleWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("[2501] // AiTerminal")
        self.root.geometry("1050x650")
        self.root.minsize(850, 500)
        self.root.configure(bg="#0d1117")

        self.text_to_display = ""
        self.index = 0
        self.is_ai_working = False

        self.command_history = []
        self.history_index = -1

        self.colors = {
            "bg": "#0d1117",
            "panel": "#161b22",
            "text": "#c9d1d9",
            "muted": "#8b949e",
            "green": "#3fb950",
            "blue": "#58a6ff",
            "yellow": "#d29922",
            "red": "#f85149",
            "purple": "#bc8cff",
            "border": "#30363d",
            "input": "#010409",
        }

        self.commands = {
            "help": (
                self.display_help,
                "Displays available commands and their descriptions"
            ),
            "ai": (
                self.ai_request,
                "Allows the user to send an AI request",
                "[prompt]"
            ),
            "echo": (
                self.echo_text,
                "Prints text to the console",
                "[text]"
            ),
            "cat": (
                self.display_file_content,
                "Displays the contents of a file",
                "[filename]"
            ),
            "mkdir": (
                self.make_directory,
                "Creates a new directory",
                "[dirname]"
            ),
            "rmdir": (
                self.remove_directory,
                "Removes an empty directory",
                "[dirname]"
            ),
            "rm": (
                self.remove_file,
                "Removes a file",
                "[filename]"
            ),
            "touch": (
                self.create_file,
                "Creates a new file",
                "[filename]"
            ),
            "ls": (
                self.list_directory,
                "Lists files and directories in the current directory",
                "[path]"
            ),
            "cd": (
                self.change_directory,
                "Changes the current directory",
                "[path]"
            ),
            "python": (
                self.run_python_code,
                "Executes Python code or Python files",
                "[code] or [-c file.py]"
            ),
            "clear": (
                self.clear_console,
                "Clears the console"
            ),
            "exit": (
                self.exit_console,
                "Exits the console application"
            ),

            # Nuevos comandos agregados
            "pwd": (
                self.print_working_directory,
                "Shows the current working directory"
            ),
            "date": (
                self.show_date,
                "Shows the current date"
            ),
            "time": (
                self.show_time,
                "Shows the current time"
            ),
            "whoami": (
                self.show_user,
                "Shows the current system user"
            ),
            "version": (
                self.show_version,
                "Shows AiTerminal version information"
            ),
            "open": (
                self.open_file_or_folder,
                "Opens a file or folder with the default app",
                "[path]"
            ),
            "rename": (
                self.rename_file_or_folder,
                "Renames a file or folder",
                "[old_name] [new_name]"
            ),
            "copy": (
                self.copy_file,
                "Copies a file",
                "[source] [destination]"
            ),
            "tree": (
                self.show_tree,
                "Shows a simple directory tree",
                "[path]"
            ),
            "bind": (
                self.search_files,
                "Searches files and folders by name from current directory",
                "[name]"
            ),
            "calc": (
                self.calculate_expression,
                "Works as a basic calculator",
                "[expression]"
            ),
        }

        self.create_widgets()
        self.display_welcome_message()
        self.update_status_bar()

    def create_widgets(self):
        self.main_frame = tk.Frame(self.root, bg=self.colors["bg"])
        self.main_frame.pack(fill="both", expand=True, padx=12, pady=12)

        self.header_frame = tk.Frame(self.main_frame, bg=self.colors["panel"])
        self.header_frame.pack(fill="x", pady=(0, 8))

        self.title_label = tk.Label(
            self.header_frame,
            text="⚡ AiTerminal 2501",
            bg=self.colors["panel"],
            fg=self.colors["green"],
            font=("Consolas", 16, "bold"),
            padx=12,
            pady=8,
        )
        self.title_label.pack(side="left")

        self.help_button = tk.Button(
            self.header_frame,
            text="Help",
            command=self.open_help_window,
            bg=self.colors["green"],
            fg="#0d1117",
            activebackground=self.colors["blue"],
            activeforeground="#ffffff",
            font=("Consolas", 10, "bold"),
            bd=0,
            padx=14,
            pady=4,
            cursor="hand2"
        )
        self.help_button.pack(side="left", padx=8)

        self.path_label = tk.Label(
            self.header_frame,
            text=os.getcwd(),
            bg=self.colors["panel"],
            fg=self.colors["muted"],
            font=("Consolas", 9),
            padx=12,
        )
        self.path_label.pack(side="right")

        self.console_frame = tk.Frame(
            self.main_frame,
            bg=self.colors["border"],
            bd=1,
            relief="flat"
        )
        self.console_frame.pack(fill="both", expand=True)

        self.text_area = tk.Text(
            self.console_frame,
            wrap="word",
            state="normal",
            bg=self.colors["input"],
            fg=self.colors["text"],
            insertbackground=self.colors["text"],
            selectbackground=self.colors["blue"],
            selectforeground="#ffffff",
            font=("Consolas", 11),
            padx=14,
            pady=14,
            bd=0,
            relief="flat",
            undo=False
        )
        self.text_area.pack(side="left", fill="both", expand=True)

        self.scrollbar = ttk.Scrollbar(
            self.console_frame,
            orient="vertical",
            command=self.text_area.yview
        )
        self.scrollbar.pack(side="right", fill="y")

        self.text_area.configure(yscrollcommand=self.scrollbar.set)

        self.text_area.tag_config(
            "prompt",
            foreground=self.colors["green"],
            font=("Consolas", 11, "bold")
        )
        self.text_area.tag_config(
            "command",
            foreground=self.colors["blue"]
        )
        self.text_area.tag_config(
            "error",
            foreground=self.colors["red"]
        )
        self.text_area.tag_config(
            "success",
            foreground=self.colors["green"]
        )
        self.text_area.tag_config(
            "warning",
            foreground=self.colors["yellow"]
        )
        self.text_area.tag_config(
            "info",
            foreground=self.colors["purple"]
        )
        self.text_area.tag_config(
            "muted",
            foreground=self.colors["muted"]
        )
        self.text_area.tag_config(
            "ai",
            foreground=self.colors["text"]
        )

        self.input_frame = tk.Frame(self.main_frame, bg=self.colors["panel"])
        self.input_frame.pack(fill="x", pady=(8, 0))

        self.input_label = tk.Label(
            self.input_frame,
            text="[2501] >",
            fg=self.colors["green"],
            bg=self.colors["panel"],
            font=("Consolas", 11, "bold"),
            padx=10,
            pady=8
        )
        self.input_label.pack(side="left")

        self.input_entry = tk.Entry(
            self.input_frame,
            bg=self.colors["input"],
            fg=self.colors["text"],
            insertbackground=self.colors["text"],
            font=("Consolas", 11),
            bd=0,
            relief="flat"
        )
        self.input_entry.pack(fill="x", expand=True, padx=(0, 10), ipady=6)
        self.input_entry.focus_set()

        self.status_frame = tk.Frame(self.main_frame, bg=self.colors["bg"])
        self.status_frame.pack(fill="x", pady=(6, 0))

        self.status_label = tk.Label(
            self.status_frame,
            text="Ready",
            bg=self.colors["bg"],
            fg=self.colors["muted"],
            font=("Consolas", 9)
        )
        self.status_label.pack(side="left")

        self.shortcut_label = tk.Label(
            self.status_frame,
            text="ENTER: ejecutar | ↑ ↓ historial | CTRL + X: limpiar",
            bg=self.colors["bg"],
            fg=self.colors["muted"],
            font=("Consolas", 9)
        )
        self.shortcut_label.pack(side="right")

        self.input_entry.bind("<Return>", self.execute_command)
        self.input_entry.bind("<Up>", self.history_up)
        self.input_entry.bind("<Down>", self.history_down)
        self.input_entry.bind("<Control-x>", self.clear_console)
        self.input_entry.bind("<Control-l>", self.clear_console)

    def update_status_bar(self):
        current_time = datetime.now().strftime("%H:%M:%S")
        status = "AI processing..." if self.is_ai_working else "Ready"
        self.status_label.config(text=f"{status} | {current_time}")
        self.path_label.config(text=os.getcwd())
        self.root.after(1000, self.update_status_bar)

    def write(self, msg, tag=None):
        self.text_area.configure(state="normal")

        if tag:
            self.text_area.insert("end", msg, tag)
        else:
            self.text_area.insert("end", msg)

        self.text_area.see("end")
        self.text_area.configure(state="disabled")

    def print_to_console(self, message, tag=None):
        self.write(message + "\n", tag)

    def display_welcome_message(self):
        banner = r"""
┌───────────────────────────────────────────────────────────────────────────────┐
│                                                                               │
│      █████╗ ██╗████████╗███████╗██████╗ ███╗   ███╗██╗███╗   ██╗ █████╗ ██╗   │
│     ██╔══██╗██║╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██║████╗  ██║██╔══██╗██║   │
│     ███████║██║   ██║   █████╗  ██████╔╝██╔████╔██║██║██╔██╗ ██║███████║██║   │
│     ██╔══██║██║   ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║██║██║╚██╗██║██╔══██║██║   │
│     ██║  ██║██║   ██║   ███████╗██║  ██║██║ ╚═╝ ██║██║██║ ╚████║██║  ██║███████╗
│     ╚═╝  ╚═╝╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝
│                                                                               │
│   Welcome to AiTerminal 2501                                                  │
│   Type "help" to see available commands                                       │
│   You can also click the Help button                                          │
│                                                                               │
└───────────────────────────────────────────────────────────────────────────────┘
"""
        self.print_to_console(banner, "info")

    def execute_command(self, event=None):
        command = self.input_entry.get().strip()
        self.input_entry.delete(0, "end")

        if not command:
            return

        self.command_history.append(command)
        self.history_index = len(self.command_history)

        self.print_to_console(f"[2501] > {command}", "prompt")

        command_parts = command.split(" ", 1)
        command_name = command_parts[0].lower()
        argument = command_parts[1] if len(command_parts) > 1 else None

        if command_name not in self.commands:
            self.print_to_console(
                'Command not found. Type "help" for more information.',
                "error"
            )
            return

        try:
            func = self.commands[command_name][0]

            if argument is not None:
                result = func(argument)
            else:
                result = func()

            if result is not None:
                self.print_to_console(result)

        except TypeError:
            self.print_to_console(
                "Error: missing or invalid command argument.",
                "error"
            )
        except Exception:
            self.print_to_console(
                traceback.format_exc(),
                "error"
            )

    def open_help_window(self):
        help_window = tk.Toplevel(self.root)
        help_window.title("AiTerminal Help")
        help_window.geometry("780x520")
        help_window.minsize(650, 400)
        help_window.configure(bg=self.colors["bg"])

        title = tk.Label(
            help_window,
            text="Available Commands",
            bg=self.colors["bg"],
            fg=self.colors["green"],
            font=("Consolas", 18, "bold"),
            pady=12
        )
        title.pack(fill="x")

        subtitle = tk.Label(
            help_window,
            text="Command list supported by AiTerminal 2501",
            bg=self.colors["bg"],
            fg=self.colors["muted"],
            font=("Consolas", 10),
            pady=4
        )
        subtitle.pack(fill="x")

        container = tk.Frame(help_window, bg=self.colors["border"])
        container.pack(fill="both", expand=True, padx=14, pady=14)

        help_text = tk.Text(
            container,
            wrap="word",
            bg=self.colors["input"],
            fg=self.colors["text"],
            font=("Consolas", 10),
            padx=12,
            pady=12,
            bd=0,
            relief="flat"
        )
        help_text.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(
            container,
            orient="vertical",
            command=help_text.yview
        )
        scrollbar.pack(side="right", fill="y")

        help_text.configure(yscrollcommand=scrollbar.set)

        help_text.tag_config(
            "command",
            foreground=self.colors["green"],
            font=("Consolas", 10, "bold")
        )
        help_text.tag_config(
            "args",
            foreground=self.colors["blue"]
        )
        help_text.tag_config(
            "description",
            foreground=self.colors["text"]
        )

        for command, data in self.commands.items():
            description = data[1]
            args = data[2] if len(data) > 2 else ""

            help_text.insert("end", command.ljust(12), "command")
            help_text.insert("end", f"{args.ljust(24)}", "args")
            help_text.insert("end", f"{description}\n", "description")

        help_text.configure(state="disabled")

        close_button = tk.Button(
            help_window,
            text="Close",
            command=help_window.destroy,
            bg=self.colors["red"],
            fg="#ffffff",
            activebackground=self.colors["yellow"],
            activeforeground="#ffffff",
            font=("Consolas", 10, "bold"),
            bd=0,
            padx=18,
            pady=6,
            cursor="hand2"
        )
        close_button.pack(pady=(0, 12))

    def display_help(self):
        self.print_to_console("Available commands:", "info")
        self.print_to_console("")

        max_command_length = max(len(command) for command in self.commands)

        for command, data in self.commands.items():
            description = data[1]
            args = data[2] if len(data) > 2 else ""
            line = f"  {command.ljust(max_command_length)} {args.ljust(24)} :: {description}"
            self.print_to_console(line, "muted")

        return ""

    def list_directory(self, path="."):
        try:
            files = os.listdir(path)

            if not files:
                return "Directory is empty.\n"

            output = []

            for item in files:
                full_path = os.path.join(path, item)

                if os.path.isdir(full_path):
                    output.append(f"📁 {item}/")
                else:
                    output.append(f"📄 {item}")

            return "\n".join(output) + "\n"

        except Exception as e:
            return f"Error: {str(e)}\n"

    def display_file_content(self, filename):
        try:
            with open(filename, "r", encoding="utf-8") as file:
                content = file.read()

            return content + "\n"

        except UnicodeDecodeError:
            return "Error: file encoding is not UTF-8.\n"

        except Exception as e:
            return f"Error: {str(e)}\n"

    def echo_text(self, text):
        return f"{text}\n"

    def make_directory(self, dirname):
        try:
            os.mkdir(dirname)
            return f"Directory created: {dirname}\n"

        except Exception as e:
            return f"Error: {str(e)}\n"

    def remove_directory(self, dirname):
        try:
            os.rmdir(dirname)
            return f"Directory removed: {dirname}\n"

        except Exception as e:
            return f"Error: {str(e)}\n"

    def remove_file(self, filename):
        try:
            os.remove(filename)
            return f"File removed: {filename}\n"

        except Exception as e:
            return f"Error: {str(e)}\n"

    def create_file(self, filename):
        try:
            with open(filename, "w", encoding="utf-8"):
                pass

            return f"File created: {filename}\n"

        except Exception as e:
            return f"Error: {str(e)}\n"

    def change_directory(self, path=None):
        try:
            if not path:
                return os.getcwd() + "\n"

            os.chdir(path)
            self.path_label.config(text=os.getcwd())

            return os.getcwd() + "\n"

        except Exception as e:
            return f"Error: {str(e)}\n"

    def run_python_code(self, code):
        stdout_backup = sys.stdout

        try:
            sys.stdout = StringIO()

            if code.startswith("-c "):
                script_path = code[3:].strip()

                with open(script_path, "r", encoding="utf-8") as script_file:
                    script_content = script_file.read()

                exec(script_content, {})
            else:
                exec(code, {})

            result = sys.stdout.getvalue()

            if not result:
                return "Python code executed successfully.\n"

            return result

        except Exception:
            return traceback.format_exc()

        finally:
            sys.stdout = stdout_backup

    def clear_console(self, event=None):
        self.text_area.configure(state="normal")
        self.text_area.delete("1.0", "end")
        self.text_area.configure(state="disabled")
        self.display_welcome_message()
        return ""

    def ai_request(self, command):
        if not command:
            return "Error: write a prompt after the ai command.\n"

        if self.is_ai_working:
            return "AI is already processing another request.\n"

        self.is_ai_working = True
        self.print_to_console("AI is thinking...", "warning")

        thread = threading.Thread(
            target=self.run_ai_request_in_thread,
            args=(command,),
            daemon=True
        )
        thread.start()

        return ""

    def run_ai_request_in_thread(self, command):
        try:
            response = asyncio.run(self.process_text(command))

            self.root.after(
                0,
                lambda: self.print_to_console("AI Response:", "info")
            )
            self.root.after(
                0,
                lambda: self.print_to_console(response + "\n", "ai")
            )

        except Exception:
            error = traceback.format_exc()
            self.root.after(
                0,
                lambda: self.print_to_console(error, "error")
            )

        finally:
            self.is_ai_working = False

    async def process_text(self, text):
        model = ArtificialInteligence()
        response = await model.generate_response(text)
        return response

    def exit_console(self):
        self.root.destroy()

    def history_up(self, event=None):
        if self.history_index > 0:
            self.history_index -= 1
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, self.command_history[self.history_index])

        return "break"

    def history_down(self, event=None):
        if self.history_index < len(self.command_history) - 1:
            self.history_index += 1
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, self.command_history[self.history_index])
        else:
            self.history_index = len(self.command_history)
            self.input_entry.delete(0, tk.END)

        return "break"

    # ------------------------------------------------------------
    # Nuevos comandos agregados
    # ------------------------------------------------------------

    def print_working_directory(self):
        return os.getcwd() + "\n"

    def show_date(self):
        return datetime.now().strftime("%Y-%m-%d") + "\n"

    def show_time(self):
        return datetime.now().strftime("%H:%M:%S") + "\n"

    def show_user(self):
        return getpass.getuser() + "\n"

    def show_version(self):
        return (
            "AiTerminal 2501 - Improved Visual Edition\n"
            "Python Terminal Interface with AI support\n"
        )

    def open_file_or_folder(self, path):
        try:
            os.startfile(path)
            return f"Opened: {path}\n"

        except Exception as e:
            return f"Error: {str(e)}\n"

    def rename_file_or_folder(self, args):
        try:
            parts = args.split(" ", 1)

            if len(parts) < 2:
                return "Error: usage rename [old_name] [new_name]\n"

            old_name, new_name = parts
            os.rename(old_name, new_name)

            return f"Renamed: {old_name} -> {new_name}\n"

        except Exception as e:
            return f"Error: {str(e)}\n"

    def copy_file(self, args):
        try:
            parts = args.split(" ", 1)

            if len(parts) < 2:
                return "Error: usage copy [source] [destination]\n"

            source, destination = parts
            shutil.copy2(source, destination)

            return f"Copied: {source} -> {destination}\n"

        except Exception as e:
            return f"Error: {str(e)}\n"

    def show_tree(self, path="."):
        try:
            if not os.path.exists(path):
                return "Error: path does not exist.\n"

            output = []
            path = os.path.abspath(path)

            output.append(os.path.basename(path) + "/")

            for root, dirs, files in os.walk(path):
                level = root.replace(path, "").count(os.sep)
                indent = "│   " * level
                folder_name = os.path.basename(root)

                if level > 0:
                    output.append(f"{indent}├── {folder_name}/")

                sub_indent = "│   " * (level + 1)

                for file in files:
                    output.append(f"{sub_indent}├── {file}")

            return "\n".join(output) + "\n"

        except Exception as e:
            return f"Error: {str(e)}\n"

    def search_files(self, search_name):
        try:
            if not search_name:
                return "Error: usage bind [file_or_folder_name]\n"

            results = []
            current_path = os.getcwd()

            for root, dirs, files in os.walk(current_path):
                for directory in dirs:
                    if search_name.lower() in directory.lower():
                        full_path = os.path.join(root, directory)
                        results.append(f"📁 {full_path}")

                for file in files:
                    if search_name.lower() in file.lower():
                        full_path = os.path.join(root, file)
                        results.append(f"📄 {full_path}")

            if not results:
                return f"No results found for: {search_name}\n"

            output = [
                f"Search results for: {search_name}",
                ""
            ]

            for result in results:
                output.append(result)

            return "\n".join(output) + "\n"

        except Exception as e:
            return f"Error: {str(e)}\n"

    def calculate_expression(self, expression):
        try:
            if not expression:
                return "Error: usage calc [expression]\n"

            allowed_operators = {
                ast.Add: operator.add,
                ast.Sub: operator.sub,
                ast.Mult: operator.mul,
                ast.Div: operator.truediv,
                ast.Pow: operator.pow,
                ast.Mod: operator.mod,
                ast.FloorDiv: operator.floordiv,
                ast.USub: operator.neg,
                ast.UAdd: operator.pos,
            }

            def evaluate(node):
                if isinstance(node, ast.Constant):
                    if isinstance(node.value, (int, float)):
                        return node.value
                    raise ValueError("Only numbers are allowed.")

                if isinstance(node, ast.BinOp):
                    left = evaluate(node.left)
                    right = evaluate(node.right)
                    operator_type = type(node.op)

                    if operator_type not in allowed_operators:
                        raise ValueError("Operator not allowed.")

                    return allowed_operators[operator_type](left, right)

                if isinstance(node, ast.UnaryOp):
                    operand = evaluate(node.operand)
                    operator_type = type(node.op)

                    if operator_type not in allowed_operators:
                        raise ValueError("Operator not allowed.")

                    return allowed_operators[operator_type](operand)

                raise ValueError("Invalid expression.")

            tree = ast.parse(expression, mode="eval")
            result = evaluate(tree.body)

            return f"{expression} = {result}\n"

        except ZeroDivisionError:
            return "Error: division by zero.\n"

        except Exception as e:
            return f"Error: invalid calculation. {str(e)}\n"


if __name__ == "__main__":
    root = tk.Tk()
    console = ConsoleWindow(root)
    root.mainloop()