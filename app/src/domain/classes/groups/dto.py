from datetime import datetime
from dataclasses import dataclass

@dataclass
class GroupsDto:
    id: int
    organization_id: int
    name: str
    created_at: str
    updated_at: str