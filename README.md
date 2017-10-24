# UPass-Script

Python script to auto renew monthly UPass for SFU student

## Run

Create a simple `config.json` file that include your SFU username and password

```json
{
  "username": "username",
  "password": "password"
}
```

and run `python3 upass.py`

## Cron job

To make it auto run, you can use `cron job`, I didn't implemented this part, beacause I want to create a desktop app and an iOS app for the automation part.
