"""
Entry point for running Castroix as a module
Usage: python -m castroix_package
"""
import tkinter as tk
from castroix_package.app import CastroixApp


def main():
    """Main entry point"""
    root = tk.Tk()
    app = CastroixApp(root)
    app.run()


if __name__ == "__main__":
    main()
