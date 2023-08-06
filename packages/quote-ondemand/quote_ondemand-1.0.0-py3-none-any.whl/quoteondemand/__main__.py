import sys
from quoteondemand.quotes import QuoteFactory

def main() -> None:

    try:
        args = [a.lower() for a in sys.argv[1:] if not a.startswith("-")]
        opts = [o for o in sys.argv[1:] if o.startswith("-")]
        # Show help message
        if "-h" in opts or "--help" in opts:
            print("Accepted arguments: zen tech")
            print("We can't help everyone, but everyone can help someone.\n - Ronald Reagan")
            raise SystemExit()

        # Show quotes
        q_obj = QuoteFactory(args)
        print(q_obj.get_quote())
    except Exception as e:
        print(e)
        print("""Error is not a fault of our knowledge, but a mistake of our judgment giving assent to that which is not true.\n - John Locke""")
        raise SystemExit()


if __name__ == "__main__":
    main()
