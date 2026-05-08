import cmd
import asyncio
import os
import platform
from datetime import datetime
from colorama import Fore, Style, init

from libraries.pseudohacker import PseudoHacker
from libraries.ai import ArtificialInteligence
from libraries.discussionchecker import DiscussionChecker

# =========================================================
# INITIALIZE COLORS
# =========================================================

init(autoreset=True)

# =========================================================
# MAIN CLI CLASS
# =========================================================

class AiTerminalCLI(cmd.Cmd):

    # =====================================================
    # DYNAMIC PROMPT
    # =====================================================

    @property
    def prompt(self):

        current_dir = os.getcwd()

        return (
            Fore.GREEN +
            f"\n[2501 | {current_dir}] > " +
            Style.RESET_ALL
        )

    # =====================================================
    # INITIAL SCREEN
    # =====================================================

    intro = Fore.CYAN + """
╔══════════════════════════════════════════════════════════════════════════════╗
║                         AITERMINAL ENHANCED CLI                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  Modern Terminal Interface with AI Support                                   ║
║                                                                              ║
║  SYSTEM INFORMATION                                                          ║
║  ─────────────────────────────────────────────────────────────────────────   ║
║  • Modern UI/UX Design                                                       ║
║  • Dynamic Colored Terminal                                                  ║
║  • File Management Commands                                                  ║
║  • Integrated AI System                                                      ║
║  • Command History                                                           ║
║  • Reusable Components                                                       ║
║                                                                              ║
║  AVAILABLE COMMANDS                                                          ║
║  ─────────────────────────────────────────────────────────────────────────   ║
║  help      -> Show all commands                                              ║
║  ai        -> Ask AI                                                         ║
║  echo      -> Print text                                                     ║
║  ls        -> List files                                                     ║
║  cd        -> Change directory                                               ║
║  pwd       -> Show current directory                                         ║
║  mkdir     -> Create folder                                                  ║
║  rmdir     -> Remove folder                                                  ║
║  touch     -> Create file                                                    ║
║  cat       -> Read file                                                      ║
║  rm        -> Delete file                                                    ║
║  clear     -> Clear console                                                  ║
║  date      -> Show current date                                              ║
║  sysinfo   -> Show system info                                               ║
║  tree      -> Show folder tree                                               ║
║  exit      -> Exit terminal                                                  ║
║                                                                              ║
║  Developed with enhanced CLI experience                                      ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

    # =====================================================
    # UTILITY METHODS
    # =====================================================

    def success(self, message):

        print(Fore.GREEN + f"[SUCCESS] {message}")

    def error(self, message):

        print(Fore.RED + f"[ERROR] {message}")

    def info(self, message):

        print(Fore.CYAN + f"[INFO] {message}")

    def warning(self, message):

        print(Fore.YELLOW + f"[WARNING] {message}")

    # =====================================================
    # BASIC COMMANDS
    # =====================================================

    def do_echo(self, text):
        """[text] :: Prints text"""

        print(Fore.WHITE + text)

    def do_pwd(self, args):
        """Shows current directory"""

        self.info(os.getcwd())

    def do_date(self, args):
        """Shows current date and time"""

        current = datetime.now().strftime(
            "%d/%m/%Y %H:%M:%S"
        )

        self.info(current)

    # =====================================================
    # FILE COMMANDS
    # =====================================================

    def do_ls(self, path):
        """[path] :: Lists files"""

        try:

            current_path = path if path else os.getcwd()

            files = os.listdir(current_path)

            print(
                Fore.CYAN +
                "\n========== FILES ==========\n"
            )

            for file in files:

                full_path = os.path.join(
                    current_path,
                    file
                )

                if os.path.isdir(full_path):

                    print(
                        Fore.BLUE +
                        f"[DIR ] {file}"
                    )

                else:

                    print(
                        Fore.WHITE +
                        f"[FILE] {file}"
                    )

            print(
                Fore.CYAN +
                "\n===========================\n"
            )

        except Exception as e:

            self.error(str(e))

    def do_cd(self, path):
        """[path] :: Changes directory"""

        try:

            if not path:

                self.info(os.getcwd())

            elif path == "..":

                os.chdir(
                    os.path.dirname(os.getcwd())
                )

                self.success(
                    f"Moved to {os.getcwd()}"
                )

            else:

                os.chdir(path)

                self.success(
                    f"Moved to {os.getcwd()}"
                )

        except Exception as e:

            self.error(str(e))

    def do_mkdir(self, dirname):
        """[dirname] :: Creates directory"""

        try:

            os.mkdir(dirname)

            self.success(
                f"Directory '{dirname}' created"
            )

        except Exception as e:

            self.error(str(e))

    def do_rmdir(self, dirname):
        """[dirname] :: Removes empty directory"""

        try:

            os.rmdir(dirname)

            self.success(
                f"Directory '{dirname}' removed"
            )

        except Exception as e:

            self.error(str(e))

    def do_touch(self, filename):
        """[filename] :: Creates file"""

        try:

            with open(filename, "w"):
                pass

            self.success(
                f"File '{filename}' created"
            )

        except Exception as e:

            self.error(str(e))

    def do_cat(self, filename):
        """[filename] :: Shows file content"""

        try:

            with open(filename, "r") as file:

                content = file.read()

            print(
                Fore.YELLOW +
                "\n========== CONTENT ==========\n"
            )

            print(Fore.WHITE + content)

            print(
                Fore.YELLOW +
                "\n=============================\n"
            )

        except Exception as e:

            self.error(str(e))

    def do_rm(self, filename):
        """[filename] :: Removes file"""

        try:

            confirm = input(

                Fore.RED +

                f"Delete '{filename}'? (y/n): "

            ).lower()

            if confirm == "y":

                os.remove(filename)

                self.success(
                    f"File '{filename}' removed"
                )

            else:

                self.warning(
                    "Operation cancelled"
                )

        except Exception as e:

            self.error(str(e))

    # =====================================================
    # TREE COMMAND
    # =====================================================

    def do_tree(self, path):
        """[path] :: Shows directory tree"""

        try:

            start_path = path if path else os.getcwd()

            print(
                Fore.CYAN +
                "\n========== TREE ==========\n"
            )

            for root, dirs, files in os.walk(start_path):

                level = root.replace(
                    start_path,
                    ""
                ).count(os.sep)

                indent = " " * 4 * level

                print(
                    Fore.BLUE +
                    f"{indent}[{os.path.basename(root)}]"
                )

                subindent = " " * 4 * (level + 1)

                for file in files:

                    print(
                        Fore.WHITE +
                        f"{subindent}{file}"
                    )

            print(
                Fore.CYAN +
                "\n==========================\n"
            )

        except Exception as e:

            self.error(str(e))

    # =====================================================
    # SYSTEM INFO
    # =====================================================

    def do_sysinfo(self, args):
        """Shows system information"""

        print(
            Fore.MAGENTA +
            "\n========== SYSTEM INFO ==========\n"
        )

        print(
            Fore.WHITE +
            f"OS: {platform.system()}"
        )

        print(
            Fore.WHITE +
            f"Version: {platform.version()}"
        )

        print(
            Fore.WHITE +
            f"Machine: {platform.machine()}"
        )

        print(
            Fore.WHITE +
            f"Processor: {platform.processor()}"
        )

        print(
            Fore.WHITE +
            f"Python Version: {platform.python_version()}"
        )

        print(
            Fore.MAGENTA +
            "\n=================================\n"
        )

    # =====================================================
    # AI COMMANDS
    # =====================================================

    def do_ai(self, command):
        """[prompt] :: Sends AI request"""

        if not command:

            self.warning(
                "Please write a prompt"
            )

            return

        self.info(
            "Generating AI response..."
        )

        asyncio.run(
            self.process_text(command)
        )

    async def process_text(self, text):

        try:

            model = ArtificialInteligence()

            response = await model.generate_response(text)

            print(
                Fore.MAGENTA +
                "\n========== AI RESPONSE ==========\n"
            )

            print(
                Fore.WHITE +
                response
            )

            print(
                Fore.MAGENTA +
                "\n=================================\n"
            )

        except Exception as e:

            self.error(
                f"AI Error: {str(e)}"
            )

    # =====================================================
    # EXTRA COMMANDS
    # =====================================================

    def do_osint(self, text):
        """[phone] :: Checks phone number"""

        try:

            self.info(
                "Analyzing phone..."
            )

            PseudoHacker.checkphone(text)

        except Exception as e:

            self.error(str(e))

    def do_dc(self, args):
        """[id] [posts] :: Discussion checker"""

        try:

            discussion_id, *amount_of_posts = args.split()

            if not amount_of_posts:

                amount_of_posts = ['9999']

            else:

                amount_of_posts = amount_of_posts[:1]

            self.info(
                "Checking discussion..."
            )

            info = DiscussionChecker.get_info(

                discussion_id,

                int(amount_of_posts[0])

            )

            print(Fore.YELLOW + info)

        except Exception as e:

            self.error(str(e))

    # =====================================================
    # HELP
    # =====================================================

    def do_help(self, args):
        """Displays all commands"""

        print(
            Fore.CYAN +
            "\n========== COMMANDS ==========\n"
        )

        commands = []

        for command in self.get_names():

            if command.startswith("do_"):

                name = command[3:]

                doc = getattr(
                    self,
                    command
                ).__doc__

                commands.append((name, doc))

        commands.sort()

        for name, doc in commands:

            print(

                Fore.GREEN +

                f"{name:<12}" +

                Fore.WHITE +

                f" -> {doc}"

            )

        print(
            Fore.CYAN +
            "\n==============================\n"
        )

    # =====================================================
    # CLEAR
    # =====================================================

    def do_clear(self, args):
        """Clears console"""

        os.system(
            'cls' if os.name == 'nt' else 'clear'
        )

        print(self.intro)

    # =====================================================
    # EXIT
    # =====================================================

    def do_exit(self, args):
        """Exits application"""

        print(
            Fore.MAGENTA +
            "\nClosing AiTerminal...\n"
        )

        return True


# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":

    AiTerminalCLI().cmdloop()