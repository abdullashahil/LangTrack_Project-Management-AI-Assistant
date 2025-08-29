import os
from pinecone import Pinecone, ServerlessSpec, CloudProvider, AwsRegion, VectorType
from dotenv import load_dotenv

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX = os.getenv("PINECONE_INDEX")
PINECONE_CLOUD = os.getenv("PINECONE_CLOUD", "aws").lower()
PINECONE_REGION = os.getenv("PINECONE_REGION", "us-east-1").lower()
EMBED_DIM = int(os.getenv("EMBED_DIM", "768"))

pc = Pinecone(api_key=PINECONE_API_KEY)
index = None

def get_index():
    global index
    if index:
        return index

    existing_indexes = [i.name for i in pc.list_indexes().indexes]
    if PINECONE_INDEX not in existing_indexes:
        print(f"Creating Pinecone index '{PINECONE_INDEX}'...")
        cloud = CloudProvider.AWS if PINECONE_CLOUD == "aws" else CloudProvider.GCP
        region = AwsRegion.US_EAST_1
        # cosine-similarity metric from pinecone
        pc.create_index(
            name=PINECONE_INDEX,
            dimension=EMBED_DIM,
            metric="cosine",
            spec=ServerlessSpec(cloud=cloud, region=region),
            vector_type=VectorType.DENSE,
        )
    host = pc.describe_index(name=PINECONE_INDEX).host
    index = pc.Index(host=host)
    return index
