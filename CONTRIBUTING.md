# Contributing to TGF - Telegram Feed

First off, thank you for considering contributing to TGF! It's people like you who make this project better for everyone.

## Code of Conduct

By participating in this project, you agree to abide by the terms of our project's license (GPL-2.0).

## How Can I Contribute?

### Reporting Bugs

- Check the [issue tracker](https://github.com/Hadi493/tgf-py/issues) to see if the bug has already been reported.
- If not, create a new issue. Provide as much detail as possible, including:
  - Your environment (Python version, OS).
  - Steps to reproduce the bug.
  - Expected vs. actual behavior.
  - Any relevant logs or screenshots.

### Suggesting Enhancements

- Open a new issue with a clear description of the enhancement.
- Explain why this enhancement would be useful to most users.

### Pull Requests

1.  **Fork** the repository.
2.  **Clone** your fork: `git clone https://github.com/YOUR_USERNAME/tgf-py.git`
3.  **Create a branch** for your changes: `git checkout -b feature/your-feature-name` or `bugfix/your-fix-name`
4.  **Set up the development environment**:
    - This project uses [uv](https://github.com/astral-sh/uv) for dependency management.
    - Install dependencies: `uv sync`
5.  **Configure the environment**:
    - Copy `.env.example` to `.env` and fill in your Telegram API credentials.
    - Configure the `config.py` file (refer to `main.py` for required variables like `history`, `limit`, `sleep_time`, `destination`, `channels`, and `session-name`).
6.  **Make your changes**. Ensure your code follows [PEP 8](https://peps.python.org/pep-0008/) standards.
7.  **Test your changes**. Run the bot using `uv run main.py` and verify the behavior.
8.  **Commit your changes**: `git commit -m 'Add some feature'`
9.  **Push to your fork**: `git push origin feature/your-feature-name`
10. **Open a Pull Request** against the `main` branch.

## Style Guide

- Follow PEP 8 for Python code.
- Write clear, concise commit messages - BTW no judgement about code as long as its work for me because it is primarily a personal project it solved my friend's personal problem.
- If you're adding a new feature, update the `README.md` if necessary.

## License

By contributing, you agree that your contributions will be licensed under the project's [GPL-2.0 License](LICENSE).
