#!/usr/bin/env python
import os
import subprocess


def main():
    cmd = ['./odoo-bin']
    for k, v in os.environ.items():
        if k.startswith('ODOO_'):
            arg = k.replace('ODOO_', '').lower()
            if arg != 'rc':
                cmd.append('--' + arg)
                cmd.append(v)
    subprocess.call(cmd)


if __name__ == "__main__":
    main()
