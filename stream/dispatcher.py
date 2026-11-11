
import json
import random
import time
from datetime import datetime, timezone

import pika

EXCHANGE = "rapido-dispatch"
EXCHANGE_TYPE = "topic"


def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="localhost")
    )
    channel = connection.channel()

    channel.exchange_declare(
        exchange=EXCHANGE,
        exchange_type=EXCHANGE_TYPE,
        durable=True
    )

    cities = {
        "bangalore": ["koramangala", "indiranagar", "whitefield"],
        "chennai": ["tnagar", "velachery", "adyar"]
    }

    request_id = 1

    print("Dispatcher started with malformed messages.")
    print("One invalid message will be sent every 10 messages.")

    try:
        while True:
            city = random.choice(list(cities.keys()))
            zone = random.choice(cities[city])
            request_type = random.choice(["ride", "food"])

            routing_key = f"{city}.{zone}.{request_type}"

            message = {
                "id": request_id,
                "city": city,
                "zone": zone,
                "type": request_type,
                "ts": datetime.now(timezone.utc).isoformat()
            }

            # Every 10th message is deliberately malformed.
            # Route it to active drivers so they can reject it.
            if request_id % 10 == 0:
                city = "bangalore"
                zone = "koramangala"
                request_type = "ride"

                routing_key = f"{city}.{zone}.{request_type}"

                message["city"] = city
                message["type"] = request_type
                message.pop("zone")

                print(f"Sending INVALID message #{request_id}")

            channel.basic_publish(
                exchange=EXCHANGE,
                routing_key=routing_key,
                body=json.dumps(message),
                properties=pika.BasicProperties(
                    content_type="application/json",
                    delivery_mode=2
                )
            )

            print(f"Sent [{routing_key}]: {message}")

            request_id += 1
            time.sleep(2)

    except KeyboardInterrupt:
        print("\nDispatcher stopped.")

    finally:
        connection.close()


if __name__ == "__main__":
    main()
