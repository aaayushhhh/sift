import argparse
from .graph import run_sift


def main():
    parser = argparse.ArgumentParser(prog="sift")
    parser.add_argument("question", nargs="+")
    args = parser.parse_args()
    result = run_sift(" ".join(args.question))
    print(result["report"])


if __name__ == "__main__":
    main()
