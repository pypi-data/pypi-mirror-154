import httpx


def query(url: str, query_: str) -> dict:
    response = httpx.post(
        url,
        json={"query": query_},
    )
    response.raise_for_status()
    return response.json()
