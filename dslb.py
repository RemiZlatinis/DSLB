#!python
# -*- encoding: utf-8 -*-

"""Dead Simple Linux Backups.

This is a simple rsync(y) wrapper that can backup and restore your Linux system.

Author: Remi Zlatinis
License: GPLv2

Examples:
    # Creates a new backup on /home/user/system_backup/
    $ python3 dslb.py

    # Creates a new backup on /mnt/storage/system_backup/
    $ python3 dslb.py /mnt/storage/system_backup

    # Updates the backup on /home/user/system_backup/
    $ python3 dslb.py -u

    # Updates the backup on /mnt/storage/system_backup/
    $ python3 dslb.py -u --update /mnt/storage/system_backup

    # Restores system from /home/user/system_backup/ to /
    $ python3 dslb.py -r

    # Restores system from /mnt/storage/system_backup/ to /
    $ python3 dslb.py -r /mnt/storage/system_backup

    # Restores system from /mnt/storage/system_backup/ to /run/media/user/writable/
    $ python3 dslb.py -r /mnt/storage/system_backup /run/media/user/writable/

Source:
    https://github/remizlatinis/dslb
"""


import subprocess
import os
import argparse
from pathlib import Path

from rsyncy_modded import main as rsyncy


DEFAULT_TARGET_PATH = Path.home() / 'system_backup'
DEFAULT_EXCLUDE_LIST = [
    '/dev',
    '/proc',
    '/sys',
    '/tmp',
    '/run',
    '/mnt',
    '/media',
    '/lost+found',
    '/swapfile',
    '.cache',  # I'm not very sure for these one.
]
ICONS = {
    'restore': '📤',
    'backup': '📥',
    'success': '✅',
    'error': '❌',
    'warning': '⚠️ ',
    'overwrite': '📝',
}

global dry_run


def check_for_sudo_privileges():
    if os.geteuid() == 0:
        print(
            f'{ICONS["error"]} You are root. Please run this script as a normal user.')
        exit(1)
    try:
        subprocess.check_call(['sudo', '-v'])
    except subprocess.CalledProcessError:
        print(
            f'\n{ICONS["error"]} Congratulations! You misspelled 3 times in a row. ')
        exit(1)


def check_for_dependencies(*dependencies):
    for dependency in dependencies:
        try:
            subprocess.check_call(
                f'which {dependency} ', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError:
            print(f'{ICONS["error"]} {dependency} is not installed.')
            exit(1)


def is_linux_system(path: Path):
    return os.path.exists(path / 'bin/bash')


def validate(args):
    restore_path = Path(args.restore_path)
    backup_path = Path(args.backup_path)

    if args.restore and args.update:
        print(
            f'{ICONS["error"]} You can\'t use --restore and --update at the same time.')
        exit(1)

    if ' ' in str(backup_path) or ' ' in str(restore_path):
        print(f'{ICONS["error"]} Path cannot contain spaces.')
        exit(1)

    # On Restore
    if args.restore:
        if not Path(restore_path).exists():
            print(f'{ICONS["error"]} Restore path does not exist.')
            exit(1)
        if not is_linux_system(restore_path):
            print(
                f'{ICONS["warning"]} Restore path is not a valid Linux system.')
            awnser = input('Do you want to continue anyway? [y/n] ')
            if awnser.lower() != 'y':
                exit(1)

    # On Update
    if args.update:
        if not Path(backup_path).exists():
            print(f'{ICONS["error"]} Backup path does not exist.')
            exit(1)
        if not is_linux_system(backup_path):
            print(f'{ICONS["error"]} Backup path is not a valid Linux system.')
            exit(1)


def get_args():
    parser = argparse.ArgumentParser(description='Dead Simple Linux Backups.')

    # Positional arguments
    parser.add_argument('backup_path', nargs='?', default=DEFAULT_TARGET_PATH,
                        help='Backup folder path. Default: /home/{user}/system_backup/')
    parser.add_argument('restore_path', nargs='?', default='/',
                        help='Restore folder path. Default: /')

    # Options
    parser.add_argument('-r', '--restore', action='store_true',
                        help='Restore mode. WARDING: This will overwrite your system!')
    parser.add_argument(
        '-u', '--update', action='store_true', help='Update mode.')
    parser.add_argument('-d', '--dry-run',
                        action='store_true', help='Dry run.')

    return parser.parse_args()


def rsync(args: str):
    if dry_run:
        print(f'\nRunning command: \nsudo rsync {args}')
    else:
        return rsyncy(args.split(' '), as_sudo=True)


def backup(path: Path, excludes: str):
    return_code = rsync(f'-aAXH --delete {excludes} / {path}')
    if dry_run:
        return

    if return_code == 0:
        print(f'{ICONS["success"]} Backup complete.')
    else:
        exit(f'\n {ICONS["error"]} Backup failed.')


def restore(source: Path, destination: Path, excludes: str):
    cmd = f'-aAXH --delete {excludes} {str(source) + "/"} {destination}'
    if dry_run:
        return print(f'\nRunning command: \nsudo rsync {cmd}')

    warn_msg = (f'\n{ICONS["warning"]} WARNING {ICONS["warning"]}\n'
                f'You are about to restore {source} to {destination}.\n'
                f'This action is irreversible!\n')
    print(warn_msg)

    # Reconfirm this dangerous action
    awnser = input(f'Are you sure for this? [y/N] ')
    if awnser.lower() == 'y':
        return_code = rsync(cmd)
        if return_code == 0:
            print(f'{ICONS["success"]} Restore complete.')
        else:
            exit(f'\n {ICONS["error"]} Restore failed.')
    else:
        print('Restore aborted.')


### Main ###
def main(args):
    validate(args)  # Will exit(1) if validation fails

    # Map args to variables
    backup_path = Path(args.backup_path)
    restore_path = Path(args.restore_path)
    global dry_run
    dry_run = args.dry_run

    # Create excludes list
    excludes = f'--exclude={backup_path}'
    for exclude in DEFAULT_EXCLUDE_LIST:
        excludes += f' --exclude={exclude}'

    # Inform user
    if args.restore:
        print(
            f'{ICONS["restore"]} Restore system\nFrom: {backup_path}\nTo: {restore_path}')
    elif args.update:
        print(f'{ICONS["backup"]} Update backup on: {backup_path}')
    elif backup_path.exists():  # Forgeted -u option or unawared invalid backup
        if is_linux_system(backup_path):
            print(
                f'{ICONS["warning"]} There is already a backup on this path.')
        else:
            print(f'{ICONS["warning"]} This path is not a valid Linux system.')
        print(f'{ICONS["overwrite"]} Overwrite backup on: {backup_path}')
    else:
        print(f'{ICONS["backup"]} Create backup to: {backup_path}')

    # Set right action
    def action(): return restore(backup_path, restore_path,
                                 excludes) if args.restore else backup(backup_path, excludes)

    # Action confirmation
    awnser = input('Are you sure that you want to perform this action? [y/N] ')
    if awnser.lower() == 'y':
        action()
    else:
        print('Aborted.')


if __name__ == '__main__':
    check_for_sudo_privileges()
    check_for_dependencies('rsync')

    args = get_args()
    exit(main(args))
