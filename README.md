<div align="center">
  <img src="tgf.png" width="144" height="144" alt="TGF" />
  <h1>TGF - Telegram Feed</h1>

  <p><strong>Open-source Telegram content forwarding bot</strong></p>

  <p>
    <img src="https://img.shields.io/badge/version-1.0.0-blue" alt="version" />
    <img src="https://img.shields.io/badge/GPL-2.0 license" alt="license" />
  </p>
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
