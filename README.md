<div align="center">
  <img src="tgf.png" width="166" height="166" alt="TGF" />
  <h1>TGF - Telegram Feed</h1>

  <p><strong>Open-source Telegram content forwarding bot</strong></p>

  <p>
    <img src="https://img.shields.io/badge/version-1.0.0-blue" alt="version" />
    <img src="https://img.shields.io/badge/GPL-2.0%20license-blue" alt="GPL-2.0 license" />
  </p>
</div>

## Quick Start

```bash
git clone https://github.com/Hadi493/tgf-py.git

cd tgf-py
```

Configure [.env](.env) & [config.py](config.py).
```bash
cp .env.example .env
```

run
```bash
uv run main.py
```

After 24h delete the `history.txt` file for better performance.
```bash
rm -f history.txt
```

## License:
This project is licensed under the [MIT License](LICENSE).
