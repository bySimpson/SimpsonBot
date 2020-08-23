import subprocess
import sys


class PacketManager:
    def install_package(self, package):
        print(f"\t\t--> Installing {package}")
        subprocess.check_call([sys.executable, "-m", "pip", "-q", "install", package])


    def install_packages(self, packages):
        print("----- cuberhills.net Package Installer -----")
        print("Made by LordSimpson")
        print("Some packages are not installed!")
        print("\tNow trying to import missing packages. This may take a while...")
        print("\tPlease do not close this window while installing!")
        for package in packages:
            self.install_package(package)
        print("All packages were installed successfully.")
        print("----- cuberhills.net Package Installer -----")

if __name__ == "__main__":
    # execute only if run as a script
    package = PacketManager()
    packages = ["discord", "discord.py", "asyncio", "sqlalchemy", "pymysql"]
    package.install_packages(packages)
