# server/tools/check_pinecone_index.py
import sys
from pathlib import Path
from dotenv import load_dotenv

# ensure project root (server/) on path so `app` package imports work
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

load_dotenv()

# import the pinecone client object you already have
from app import pinecone_client

pc = pinecone_client.pc
INDEX_NAME = pinecone_client.PINECONE_INDEX

def describe_index():
    try:
        desc = pc.describe_index(name=INDEX_NAME)
    except Exception as e:
        print("Failed to call describe_index():", repr(e))
        return

    print("describe_index() repr:\n", repr(desc)[:1000])

    # try common access patterns
    for attempt in (
        ("attr", lambda d: getattr(d, "dimension", None)),
        ("key", lambda d: d.get("dimension") if isinstance(d, dict) else None),
        ("prop", lambda d: d.dimension if hasattr(d, "dimension") else None),
    ):
        try:
            dim = attempt[1](desc)
            if dim:
                print(f"Detected dimension via {attempt[0]}: {dim}")
                return
        except Exception:
            pass

    # If we didn't find it above, try printing fields
    try:
        print("Full description object fields/dir():")
        print(dir(desc)[:200])
    except Exception:
        pass

    print("Couldn't automatically extract 'dimension'. If you prefer, open Pinecone console and inspect the index settings for", INDEX_NAME)

if __name__ == "__main__":
    describe_index()
