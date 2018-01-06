# UPass-Script

Python script to auto renew monthly UPass for SFU student

## Run

Create a simple `config.json` file that include your SFU username and password

ifttt config is optional. If provided, it will trigger corresponding ifttt action on **request failed**.


```json
{
  "username": "username",
  "password": "password",
  "ifttt_event": "optional",
  "ifttt_key": "optional"
}
```

and run `python3 upass.py`

## Cron job

To make it auto run, you can use `cron job`, I didn't implemented this part, beacause I want to create a desktop app and an iOS app for the automation part.

A possible crontab config (run on 20th day of each month):
```cron
0 0 20 * * /path/to/python3 /path/to/upass.py
```

## License

MIT
