def validate_webhook_url(url: str) -> None:
    raise NotImplementedError


async def send_webhook(url: str, payload: dict, max_retries: int = 3) -> bool:
    raise NotImplementedError
