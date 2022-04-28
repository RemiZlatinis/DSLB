<a href="https://paypal.me/remizlatinis"> <img align="right" src="https://cdn.ko-fi.com/cdn/kofi3.png?v=3" height="50" width="210" alt="paypal.me/remizlatinis" /></a><br><br>


# Dead Simple Linux Backups

A rsync wrapper that makes the Linux full system backups and restores easier than ever. 


## Demo

![](https://github.com/RemiZlatinis/DSLB/raw/main/assets/demo.gif)


## Installation

Install with pip
```bash
  pip install dslb
```

Install dslb with git clone

```bash
  git clone https://github.com/RemiZlatinis/DSLB
  cd DSLB
```
    
## Usage/Examples
    # Creates a new backup on /home/user/system_backup/ # Default backup path
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
## FAQ

#### Does the backup path cause an infinite loop?

No, the backup path will always be excluded.

#### Where I can find that cool shell setup?
https://github.com/RemiZlatinis/my-settings/tree/main/zsh-configs

## Authors

- [@RemiZlatinis](https://www.github.com/RemiZlatinis)


## Feedback

If you have any feedback, please reach out to us at remizlatinis@gmail.com


## License

[![GPLv2 License](https://img.shields.io/badge/License-GPL%20v2-yellow.svg)](https://github.com/RemiZlatinis/DSLB/raw/main/LICENSE)
