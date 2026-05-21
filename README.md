<div align="center">
  <img src="tgf.png" alt="TGF Logo" width="150" style="border-radius: 50%; border: 4px solid #fff; box-shadow:0 4px 12px rgba(0,0,0,0.15);"/>
  <h3>TGF</h3>
  <p><strong>Telegram Feed:</strong> An automated Telegram content forwarding bot that monitors multiple source channels and automatically forwards new messages to a single destination channel/account. It uses a tracking file to prevent duplicate forwarding and runs continuously in a loop.</p>
</div>


## Quick Start

Configure [.env](.env) & [config.py](config.py) first.
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
