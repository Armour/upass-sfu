# upass-sfu

[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat)](http://makeapullrequest.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Template from jarvis](https://img.shields.io/badge/Hi-Jarvis-ff69b4.svg)](https://github.com/Armour/Jarvis)

This script helps SFU students renew their U-Pass monthly.

## How To Run

### 1. Update your SFU username and password in `config.json`

```json
{
  "username": "username",
  "password": "password",
  "ifttt_event": "optional",
  "ifttt_key": "optional"
}
```

In the json file, `ifttt` config is optional. If `ifttt` is provided, the script will trigger corresponding ifttt actions when **request fails**.

### 2. Run the following command

```shell
python3 upass.py
```

The script renews your U-Pass.

## Automation

In Unix-like systems, use `crontab` to run this script automatically and periodically.
The following command is an example of how to setup `crontab` for this script:

```cron
0 0 20 * * /path/to/python3 /path/to/upass.py
```

An alternative method to automatically renew your U-Pass is to create a desktop App or an iOS App, which I may implement in the future.

## Contribution

See [CONTRIBUTING.md](https://github.com/Armour/upass-sfu/blob/master/.github/CONTRIBUTING.md)

## License

[MIT License](https://github.com/Armour/upass-sfu/blob/master/LICENSE)
