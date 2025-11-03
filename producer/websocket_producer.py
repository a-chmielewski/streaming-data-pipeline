import os, json, time
from kafka import KafkaProducer
from websocket import WebSocketApp
from dotenv import load_dotenv

load_dotenv()

KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka:9092")
TOPIC = os.getenv("KAFKA_TOPIC", "crypto_trades")
SYMBOL = os.getenv("SYMBOL", "btcusdt")  # Binance requires lowercase


def create_kafka_producer(max_retries=30, retry_delay=2):
    for attempt in range(1, max_retries + 1):
        try:
            print(f"🔄 Attempting to connect to Kafka ({attempt}/{max_retries})...")
            producer = KafkaProducer(
                bootstrap_servers=[KAFKA_BROKER],
                api_version_auto_timeout_ms=5000,
            )
            print(f"✅ Successfully connected to Kafka at {KAFKA_BROKER}")
            return producer
        except Exception as e:
            print(f"⚠️ Kafka not ready: {e}")
            if attempt < max_retries:
                time.sleep(retry_delay)
            else:
                raise


producer = create_kafka_producer()


def on_open(ws):
    print(f"✅ WebSocket connected to Binance stream: {SYMBOL}@aggTrade")


def on_message(ws, message):
    try:
        data = json.loads(message)
    except json.JSONDecodeError as e:
        print(f"⚠️ Could not parse message: {e}: {message}")
        return

    # Binance sends aggregate trade data directly
    if "e" in data and data["e"] == "aggTrade":
        producer.send(TOPIC, json.dumps(data).encode("utf-8"))
        producer.flush()


def on_error(ws, error):
    print(f"WebSocket error: {error}")


def on_close(ws, code, reason):
    print(f"WebSocket closed: code={code} reason={reason}")


def start_ws_forever():
    # Non-recursive reconnect loop
    while True:
        binance_url = f"wss://fstream.binance.com/ws/{SYMBOL}@aggTrade"
        ws = WebSocketApp(
            binance_url,
            on_open=on_open,
            on_message=on_message,
            on_error=on_error,
            on_close=on_close,
        )
        # Binance sends pings every 3 minutes, expects pong within 10 minutes
        ws.run_forever(ping_interval=60, ping_timeout=10)
        print("🔁 Disconnected; reconnecting in 5s...")
        time.sleep(5)


if __name__ == "__main__":
    start_ws_forever()
