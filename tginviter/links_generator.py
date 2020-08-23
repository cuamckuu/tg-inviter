import uuid


def get_random_token():
    """Generate random uuid token"""

    return uuid.uuid4()


def generate_invite_link(
    bot_name,
    *,
    token=None,
    max_uses=1,
    short=True,
    proto="https"
):
    """Generate customizable invite link"""

    if proto not in ["http", "https", "tg"]:
        raise ValueError("Use one of ['http', 'https', 'tg'] as proto")

    if not token:
        token = get_random_token()

    domain = "telegram.me/"
    if short:
        domain = "t.me/"

    params = f"{bot_name}?start={token}"
    if proto == "tg":
        domain = "resolve"
        params = f"?domain={bot_name}&start={token}"

    return f"{proto}://{domain}{params}", str(token)

def generate_joinchat_link(token, short=True):
    """Generate joinchat link"""

    domain = "telegram.me"
    if short:
        domain = "t.me"

    return f"https://{domain}/joinchat/{token}"
