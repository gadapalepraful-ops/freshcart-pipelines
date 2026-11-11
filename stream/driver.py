
import json
import sys

import pika

EXCHANGE = "rapido-dispatch"


def main():
    if len(sys.argv) != 3:
        print("Usage: python driver.py <driver_name> <binding_pattern>")
        sys.exit(1)

    driver_name = sys.argv[1]
    binding_pattern = sys.argv[2]

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="localhost")
    )
    channel = connection.channel()

    channel.exchange_declare(
        exchange=EXCHANGE,
        exchange_type="topic",
        durable=True
    )

    result = channel.queue_declare(
        queue="",
        exclusive=True
    )
    queue_name = result.method.queue

    channel.queue_bind(
        exchange=EXCHANGE,
        queue=queue_name,
        routing_key=binding_pattern
    )

    print(f"{driver_name} online!")
    print(f"Listening for: {binding_pattern}")
    print("ACK/NACK mode enabled.\n")

    def callback(ch, method, properties, body):
        message = json.loads(body)

        if "zone" not in message:
            print(
                f"REJECTED [{method.routing_key}]: "
                f"Message #{message.get('id')} missing zone. "
                "NACK requeue=False"
            )

            ch.basic_nack(
                delivery_tag=method.delivery_tag,
                requeue=False
            )
            return

        print(
            f"ACK [{method.routing_key}]: "
            f"Message #{message.get('id')} processed successfully."
        )

        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(
        queue=queue_name,
        on_message_callback=callback,
        auto_ack=False
    )

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print(f"\n{driver_name} stopped.")
        channel.stop_consuming()
    finally:
        connection.close()


if __name__ == "__main__":
    main()
