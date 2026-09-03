#!/usr/bin/env python3
"""
Payjoy Disable Tool - Command-line utility to disable or toggle Payjoy functionality
"""

import argparse
import os
import json
import sys
from pathlib import Path
from typing import Dict, Any


class PayjoyDisableTool:
    """Main tool class for managing Payjoy disable status"""
    
    CONFIG_FILE = Path.home() / ".payjoy" / "config.json"
    ENV_VAR = "PAYJOY_DISABLED"
    
    def __init__(self):
        """Initialize the tool"""
        self.config_file = self.CONFIG_FILE
        self.config_file.parent.mkdir(parents=True, exist_ok=True)
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file"""
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                return json.load(f)
        return {"payjoy_disabled": False}
    
    def _save_config(self) -> None:
        """Save configuration to file"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
        print(f"✓ Configuration saved to {self.config_file}")
    
    def disable(self) -> None:
        """Disable Payjoy"""
        self.config["payjoy_disabled"] = True
        self._save_config()
        print("✓ Payjoy has been DISABLED")
        os.environ[self.ENV_VAR] = "true"
    
    def enable(self) -> None:
        """Enable Payjoy"""
        self.config["payjoy_disabled"] = False
        self._save_config()
        print("✓ Payjoy has been ENABLED")
        os.environ[self.ENV_VAR] = "false"
    
    def toggle(self) -> None:
        """Toggle Payjoy status"""
        current_status = self.config.get("payjoy_disabled", False)
        new_status = not current_status
        self.config["payjoy_disabled"] = new_status
        self._save_config()
        status_str = "DISABLED" if new_status else "ENABLED"
        print(f"✓ Payjoy has been toggled to {status_str}")
        os.environ[self.ENV_VAR] = str(new_status).lower()
    
    def status(self) -> None:
        """Display current Payjoy status"""
        is_disabled = self.config.get("payjoy_disabled", False)
        status_str = "DISABLED ✗" if is_disabled else "ENABLED ✓"
        print(f"Payjoy Status: {status_str}")
        print(f"Config file: {self.config_file}")
        print(f"Environment variable '{self.ENV_VAR}': {os.getenv(self.ENV_VAR, 'not set')}")
    
    def reset(self) -> None:
        """Reset to default configuration"""
        if self.config_file.exists():
            self.config_file.unlink()
            print("✓ Configuration reset to defaults (Payjoy ENABLED)")
        else:
            print("ℹ Configuration already at defaults")
        self.config = {"payjoy_disabled": False}
        os.environ[self.ENV_VAR] = "false"


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Command-line tool to disable or toggle Payjoy functionality",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  payjoy-disable disable          Disable Payjoy
  payjoy-disable enable           Enable Payjoy
  payjoy-disable toggle           Toggle Payjoy status
  payjoy-disable status           Show current status
  payjoy-disable reset            Reset to defaults
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Disable command
    subparsers.add_parser('disable', help='Disable Payjoy')
    
    # Enable command
    subparsers.add_parser('enable', help='Enable Payjoy')
    
    # Toggle command
    subparsers.add_parser('toggle', help='Toggle Payjoy status')
    
    # Status command
    subparsers.add_parser('status', help='Show current Payjoy status')
    
    # Reset command
    subparsers.add_parser('reset', help='Reset configuration to defaults')
    
    args = parser.parse_args()
    
    tool = PayjoyDisableTool()
    
    if args.command == 'disable':
        tool.disable()
    elif args.command == 'enable':
        tool.enable()
    elif args.command == 'toggle':
        tool.toggle()
    elif args.command == 'status':
        tool.status()
    elif args.command == 'reset':
        tool.reset()
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()
