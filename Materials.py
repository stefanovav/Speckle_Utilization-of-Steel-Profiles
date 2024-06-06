from specklepy.objects import Base

class SteelS355(Base):
    _speckle_type_override: str = "SteelS355"
    density: str = 7800
    strength: str = "S355"

class SteelS235(Base):
    _speckle_type_override: str = "SteelS235"
    density: str = 7800
    strength: str = "S235"
