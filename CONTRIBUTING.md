# Contributing to Streaming Data Pipeline

Thank you for your interest in contributing to this project! This document provides guidelines and instructions for contributing.

## 🚦 Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/streaming-data-pipeline.git
   cd streaming-data-pipeline
   ```
3. **Create a branch** for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## 🔧 Development Setup

### Prerequisites

- Python 3.11+
- Docker and Docker Compose
- Git

### Environment Setup

1. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   pip install black isort flake8  # Development tools
   ```

2. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Start the development environment**:
   ```bash
   docker compose up -d
   ```

## 📝 Code Standards

### Python Style Guide

We follow PEP 8 with some modifications:

- **Line length**: Maximum 120 characters
- **Formatter**: Black (automatic formatting)
- **Import sorting**: isort
- **Linter**: Flake8

### Running Code Quality Checks

Before submitting a PR, ensure all checks pass:

```bash
# Format code
black producer/ app/

# Sort imports
isort producer/ app/

# Lint code
flake8 producer/ app/ --max-line-length=120 --extend-ignore=E203,W503
```

### Pre-commit Hooks (Recommended)

Install pre-commit hooks to automatically check code before commits:

```bash
pip install pre-commit
pre-commit install
```

## 🧪 Testing

### Manual Testing

1. **Test the producer**:
   ```bash
   cd producer
   python websocket_producer.py
   ```

2. **Check Kafka messages**:
   ```bash
   docker compose exec kafka kafka-console-consumer \
     --bootstrap-server localhost:9092 \
     --topic crypto_trades \
     --from-beginning
   ```

3. **Verify Elasticsearch data**:
   ```bash
   curl -u elastic:password http://localhost:9200/crypto-trades-v2/_search?pretty
   ```

### Integration Tests

Run the full integration test suite:

```bash
docker compose down -v
docker compose up -d
# Wait for services to be ready
docker compose logs -f
```

## 📋 Pull Request Process

### Before Submitting

1. ✅ All code quality checks pass
2. ✅ Code is properly formatted
3. ✅ Commits are clear and descriptive
4. ✅ Documentation is updated if needed
5. ✅ No sensitive data in commits

### PR Guidelines

1. **Create a clear PR title**:
   - `feat: Add new trading symbol support`
   - `fix: Resolve WebSocket reconnection issue`
   - `docs: Update README with new features`
   - `refactor: Improve Spark streaming performance`

2. **Write a detailed description**:
   - What does this PR do?
   - Why is this change needed?
   - How was it tested?
   - Any breaking changes?

3. **Link related issues**:
   - Use "Closes #123" to auto-close issues
   - Reference related discussions

4. **Keep PRs focused**:
   - One feature/fix per PR
   - Small, reviewable changes
   - Avoid mixing refactoring with features

### CI/CD Checks

All PRs automatically trigger:

- **Linting**: Code style checks
- **Build**: Docker image compilation
- **Security**: Dependency vulnerability scans
- **Integration**: End-to-end tests

PRs must pass all checks before merging.

## 🏷️ Commit Convention

We follow conventional commits:

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `test`: Test additions or changes
- `chore`: Build process or tooling changes

### Examples

```bash
feat(producer): Add support for multiple trading pairs
fix(spark): Handle null values in trade data
docs(readme): Update installation instructions
refactor(producer): Simplify WebSocket connection logic
```

## 🐛 Reporting Bugs

When reporting bugs, please include:

1. **Environment details**:
   - OS and version
   - Docker version
   - Python version

2. **Steps to reproduce**:
   - Clear, numbered steps
   - Expected vs actual behavior

3. **Logs and errors**:
   - Relevant log output
   - Error messages
   - Stack traces

4. **Configuration**:
   - Relevant `.env` settings (without sensitive data)
   - Modified configuration files

## 💡 Suggesting Features

Feature requests are welcome! Please include:

1. **Use case**: Why is this feature needed?
2. **Proposed solution**: How should it work?
3. **Alternatives**: Other approaches considered?
4. **Impact**: Who benefits from this feature?

## 📁 Project Structure

```
.
├── .github/
│   ├── workflows/          # CI/CD pipeline definitions
│   ├── dependabot.yml      # Automated dependency updates
│   └── labeler.yml         # PR auto-labeling rules
├── app/
│   └── spark_stream.py     # Spark streaming processor
├── producer/
│   ├── websocket_producer.py  # Binance WebSocket client
│   └── requirements.txt    # Producer dependencies
├── docker-compose.yml      # Service orchestration
├── Dockerfile             # Producer container image
├── requirements.txt       # Project dependencies
└── README.md             # Project documentation
```

## 🔐 Security

- **Never commit** sensitive data (API keys, passwords)
- **Use `.env`** for local configuration
- **Report security issues** privately via GitHub Security Advisories

## 🤝 Code Review

When reviewing PRs:

1. **Be respectful and constructive**
2. **Focus on code quality and maintainability**
3. **Ask questions to understand intent**
4. **Suggest improvements, don't demand**
5. **Approve when satisfied**

## 📞 Getting Help

- **GitHub Issues**: For bugs and feature requests
- **GitHub Discussions**: For questions and ideas
- **Documentation**: Check README and code comments

## 📜 License

By contributing, you agree that your contributions will be licensed under the same license as the project (MIT License).

---

Thank you for contributing! 🎉

