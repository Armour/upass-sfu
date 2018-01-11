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

To make it auto run, you can use `cron job`,
a possible crontab config (run on 20th day of each month) is like below:

```cron
0 0 20 * * /path/to/python3 /path/to/upass.py
```

An alternative way is to create a desktop app or an iOS app for the automation part, I'll implement that in the near future.

## License

MIT
