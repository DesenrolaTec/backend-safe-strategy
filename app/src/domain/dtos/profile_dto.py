from dataclasses import dataclass

@dataclass
class ProfileDto:
    user_id: int
    organization_id: int
    name: str
    enable: str