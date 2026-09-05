#!/usr/bin/env python3
"""Pick a random SAA-C03 practice question, or reveal the answer for one."""

import argparse
import json
import random
import sys
from pathlib import Path

BANK = Path(__file__).resolve().parent.parent / "questions.json"


def load():
    with BANK.open() as f:
        return json.load(f)


def ask(bank, exclude, domain):
    pool = [q for q in bank["questions"] if q["id"] not in exclude]
    if domain:
        pool = [q for q in pool if q["domain"] == domain]
    if not pool:
        print("NO_QUESTIONS_LEFT: every question matching the filter has been asked.")
        return 1
    q = random.choice(pool)
    print(f"ID: {q['id']}")
    print(f"DOMAIN: {bank['domains'][q['domain']]}")
    print(f"DIFFICULTY: {q['difficulty']}")
    print(f"SELECT: {q['select']}")
    print()
    print(q["question"])
    print()
    for key in sorted(q["options"]):
        print(f"{key}. {q['options'][key]}")
    return 0


def reveal(bank, qid):
    for q in bank["questions"]:
        if q["id"] == qid:
            print(f"ID: {q['id']}")
            print(f"CORRECT: {', '.join(q['answer'])}")
            print()
            print("EXPLANATION:")
            print(q["explanation"])
            print()
            print("WHY THE OTHERS ARE WRONG:")
            for key in sorted(q["why_wrong"]):
                print(f"{key}. {q['why_wrong'][key]}")
            print()
            print(f"TAGS: {', '.join(q['tags'])}")
            return 0
    print(f"UNKNOWN_ID: {qid}", file=sys.stderr)
    return 1


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--reveal", metavar="ID", help="print the answer and explanation for a question id")
    p.add_argument("--exclude", default="", help="comma-separated question ids already asked this session")
    p.add_argument("--domain", choices=["secure", "resilient", "performing", "cost"], help="restrict to one exam domain")
    args = p.parse_args()

    bank = load()
    if args.reveal:
        return reveal(bank, args.reveal)
    exclude = {i.strip() for i in args.exclude.split(",") if i.strip()}
    return ask(bank, exclude, args.domain)


if __name__ == "__main__":
    sys.exit(main())
