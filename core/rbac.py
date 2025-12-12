ROLE_PERMS = {
    "admin": {"*"},
    "zookeeper": {"animals:view", "animals:update", "feeding:*", "enclosures:view"},
    "ticketing": {"tickets:*", "ticket_types:*", "animals:view", "enclosures:view"}
}

def can(role: str, perm: str) -> bool:
    perms = ROLE_PERMS.get(role, set())
    return "*" in perms or perm in perms