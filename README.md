# TGF Telegram Feed
An automated Telegram content forwarding bot that monitors multiple source channels and automatically forwards new messages to a single destination channel/account. It uses a tracking file to prevent duplicate forwarding and runs continuously in a loop.

## Quick Start

Configure [.env](.env) & [main](main.py) first.
```bash
cp .env.example .env
uv run main.py
```

After 24h delete the `history.txt` file for better performance.
```bash
rm -f history.txt
```

## License:
This project is licensed under the [MIT License](LICENSE).
