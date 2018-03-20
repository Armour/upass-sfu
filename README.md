# UPass-Script

This script helps students in SFU to renew their U-Pass every month.

## How To Run

### 1. Create a simple `config.json` file that contains your SFU username and password.

A sample `json` is provided as the following: 

```json
{
  "username": "username",
  "password": "password",
  "ifttt_event": "optional",
  "ifttt_key": "optional"
}
```

In the json file, `ifttt` config is optional. If `ifttt` is provided, the script will trigger corresponding ifttt action on **request failed**.

### 2. Run `python3 upass.py`.

The script will then renew your U-Pass.

## Automation

In Unix like systems, you can use `crontab` to run this script automatically and periodicity.
The following command is an example of how to setup `crontab` for this script:

```cron
0 0 20 * * /path/to/python3 /path/to/upass.py
```

An alternative way to automatically renew your U-Pass is to create a desktop App or an iOS App, which I may implement in the future.

## License

This script is released under [MIT License](https://opensource.org/licenses/MIT).
