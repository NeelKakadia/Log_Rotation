#!/usr/bin/env python3
import os
import random
import argparse
from datetime import datetime, timedelta

LEVELS = ["DEBUG", "INFO", "WARN", "ERROR"]
SERVICES = ["auth", "payments", "orders", "api", "worker", "scheduler", "db"]
HOSTS = ["macbook-pro", "web-01", "web-02", "batch-01", "ip-10-0-1-12", "ip-10-0-2-31"]
USERS = ["neel", "alice", "bob", "charlie", "diana", "guest"]

MESSAGES = [
    "Request received",
    "Request completed",
    "Token validated",
    "Cache miss",
    "Cache hit",
    "DB connection opened",
    "DB query executed",
    "Rate limit applied",
    "Upstream timeout",
    "Retrying operation",
    "Healthcheck OK",
    "Healthcheck failed",
    "Permission denied",
    "Invalid payload received",
    "Service started",
    "Service stopped",
]

NAME_PARTS = ["app", "server", "nginx", "api", "worker", "db", "audit", "events", "billing", "auth"]

def random_timestamp(within_minutes: int = 180) -> str:
    now = datetime.now()
    t = now - timedelta(
        minutes=random.randint(0, within_minutes),
        seconds=random.randint(0, 59),
        milliseconds=random.randint(0, 999),
    )
    # Example: 2026-02-21T18:45:10.123Z
    return t.strftime("%Y-%m-%dT%H:%M:%S") + f".{t.microsecond // 1000:03d}Z"

def random_log_line() -> str:
    level = random.choices(LEVELS, weights=[10, 60, 20, 10], k=1)[0]
    service = random.choice(SERVICES)
    host = random.choice(HOSTS)
    user = random.choice(USERS)
    req_id = f"req-{random.randint(100000, 999999)}"
    status = random.choice([200, 201, 204, 400, 401, 403, 404, 409, 429, 500, 502, 503])
    latency_ms = random.randint(5, 2500)
    msg = random.choice(MESSAGES)

    # add a bit of “real” detail sometimes
    extras = ""
    if status >= 500:
        extras = f" error_code=E{random.randint(100,999)}"
    elif status == 401:
        extras = " reason=invalid_token"
    elif status == 429:
        extras = " reason=rate_limited"

    return (
        f"{random_timestamp()} [{level}] "
        f"service={service} host={host} user={user} request_id={req_id} "
        f"status={status} latency_ms={latency_ms} msg=\"{msg}\"{extras}"
    )

def random_filename() -> str:
    base = "-".join(random.sample(NAME_PARTS, k=random.randint(1, 2)))
    suffix = random.choice(["prod", "dev", "staging", "node1", "node2", "ca-central-1", "us-east-1"])
    return f"{base}-{suffix}.log"

def main():
    parser = argparse.ArgumentParser(description="Generate fake .log files with random names and realistic lines.")
    parser.add_argument("--out", default="./logs", help="Output directory (default: ./logs)")
    parser.add_argument("--count", type=int, default=6, help="Number of log files (default: 6)")
    parser.add_argument("--lines", type=int, default=200, help="Lines per file (default: 200)")
    args = parser.parse_args()

    os.makedirs(args.out, exist_ok=True)

    created = []
    for _ in range(args.count):
        fname = random_filename()
        path = os.path.join(args.out, fname)

        # ensure unique file name
        while os.path.exists(path):
            fname = random_filename()
            path = os.path.join(args.out, fname)

        with open(path, "w", encoding="utf-8") as f:
            for _ in range(args.lines):
                f.write(random_log_line() + "\n")

        created.append(path)

    print("Created log files:")
    for p in created:
        print(f" - {p}")

if __name__ == "__main__":
    main()