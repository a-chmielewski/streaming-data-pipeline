# Real-Time Cryptocurrency Trading Data Pipeline

[![CI Pipeline](https://github.com/a-chmielewski/streaming-data-pipeline/actions/workflows/ci.yml/badge.svg)](https://github.com/a-chmielewski/streaming-data-pipeline/actions/workflows/ci.yml)
[![CD Pipeline](https://github.com/a-chmielewski/streaming-data-pipeline/actions/workflows/cd.yml/badge.svg)](https://github.com/a-chmielewski/streaming-data-pipeline/actions/workflows/cd.yml)
[![Security Scan](https://github.com/a-chmielewski/streaming-data-pipeline/actions/workflows/security.yml/badge.svg)](https://github.com/a-chmielewski/streaming-data-pipeline/actions/workflows/security.yml)

A production-ready real-time streaming data pipeline for processing cryptocurrency trading data from Binance WebSocket streams using Apache Kafka, Spark Streaming, and Elasticsearch.

## 🏗️ Architecture

```
Binance WebSocket API → Producer → Kafka → Spark Streaming → Elasticsearch → Kibana
```

### Components

- **WebSocket Producer**: Connects to Binance futures WebSocket API and streams aggregate trade data
- **Apache Kafka**: Distributed message broker for reliable data streaming
- **Apache Spark**: Real-time stream processing with batch writes to Elasticsearch
- **Elasticsearch**: Data storage and indexing
- **Kibana**: Data visualization and exploration

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- Git

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/a-chmielewski/streaming-data-pipeline.git
   cd streaming-data-pipeline
   ```

2. **Configure environment variables**
   Create a `.env` file in the root directory:
   ```env
   ELASTIC_PASSWORD=your_secure_password
   KIBANA_PASSWORD=your_kibana_password
   SYMBOL=btcusdt
   ```

3. **Start the pipeline**
   ```bash
   docker compose up -d
   ```

4. **Access Kibana**
   - URL: http://localhost:5601
   - Username: `elastic`
   - Password: (from your `.env` file)

5. **View data**
   - Index: `crypto-trades-v2`
   - Contains: timestamp, symbol, price, quantity, is_buyer_maker, trade_id, trade_time_ms

## 📊 Data Schema

The pipeline processes Binance aggregate trade events with the following fields:

| Field | Type | Description |
|-------|------|-------------|
| `timestamp` | timestamp | Trade execution time |
| `symbol` | string | Trading pair (e.g., BTCUSDT) |
| `price` | double | Trade price |
| `quantity` | double | Trade quantity |
| `is_buyer_maker` | boolean | Whether the buyer is the market maker |
| `trade_id` | long | Aggregate trade ID |
| `trade_time_ms` | long | Trade timestamp in milliseconds |

## 🔧 Configuration

### Change Trading Symbol

Edit `docker-compose.yml` or set environment variable:
```yaml
SYMBOL=ethusdt  # For Ethereum
```

Supported symbols: Any Binance futures trading pair in lowercase (btcusdt, ethusdt, etc.)

### Elasticsearch Index

Data is written to the `crypto-trades-v2` index. To change:
```python
# app/spark_stream.py
.option("es.resource", "your-index-name")
```

## 🧪 CI/CD Pipeline

This project includes comprehensive GitHub Actions workflows:

### Continuous Integration (CI)
- **Linting**: Black, isort, Flake8
- **Build**: Docker image compilation
- **Validation**: Configuration checks

### Continuous Deployment (CD)
- **Auto-build**: Builds on push to main
- **Registry**: Pushes to GitHub Container Registry
- **Versioning**: Semantic versioning support

### Security
- **Dependency Scan**: Weekly vulnerability checks
- **Docker Scan**: Trivy image scanning
- **Automated Updates**: Dependabot for dependencies

### Integration Tests
- **Docker Compose**: End-to-end testing
- **Service Health**: Kafka and Elasticsearch checks

## 🛠️ Development

### Local Development

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run linters**
   ```bash
   black producer/ app/
   isort producer/ app/
   flake8 producer/ app/
   ```

3. **Test producer locally**
   ```bash
   cd producer
   python websocket_producer.py
   ```

### Project Structure

```
.
├── .github/
│   ├── workflows/       # CI/CD workflows
│   ├── dependabot.yml   # Dependency updates
│   └── labeler.yml      # PR auto-labeling
├── app/
│   └── spark_stream.py  # Spark streaming application
├── producer/
│   ├── websocket_producer.py  # Binance WebSocket client
│   └── requirements.txt
├── docker-compose.yml   # Services orchestration
├── Dockerfile          # Producer container
└── requirements.txt    # Python dependencies
```

## 📈 Monitoring

### Check Service Status
```bash
docker compose ps
```

### View Logs
```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f producer
docker compose logs -f spark-streaming
```

### Kafka Topics
```bash
docker compose exec kafka kafka-topics --list --bootstrap-server localhost:9092
```

### Elasticsearch Health
```bash
curl -u elastic:your_password http://localhost:9200/_cluster/health
```

## 🔒 Security

- Elasticsearch secured with authentication
- Sensitive data in `.env` (not committed)
- Regular security scans via GitHub Actions
- Dependency vulnerability monitoring

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

All PRs trigger CI checks automatically.

## 📝 License

This project is open source and available under the MIT License.

## 🔗 References

- [Binance WebSocket API](https://developers.binance.com/docs/derivatives/usds-margined-futures/websocket-market-streams)
- [Apache Kafka](https://kafka.apache.org/)
- [Apache Spark Structured Streaming](https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html)
- [Elasticsearch](https://www.elastic.co/elasticsearch/)

## 📧 Contact

For questions or suggestions, please open an issue on GitHub.

---

**Note**: Replace `USERNAME` in badge URLs with your actual GitHub username.

