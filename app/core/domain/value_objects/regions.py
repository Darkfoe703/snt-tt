# app/core/domain/value_objects/regions.py
from enum import Enum

# REGIONS
class RegionValueObject(Enum):
    THE_FORGE = 10000002
    DOMAIN = 10000043
    SINQ_LAISON = 10000032
    HEIMATAR = 10000030
    METROPOLIS = 10000042

    @property
    def display_name(self):
        """Nombre legible para la región"""
        names = {
            self.THE_FORGE: "The Forge",
            self.DOMAIN: "Domain", 
            self.SINQ_LAISON: "Sinq Laison",
            self.HEIMATAR: "Heimatar",
            self.METROPOLIS: "Metropolis"
        }
        return names[self]

    @classmethod
    def get_choices(cls):
        """Obtener lista de tuplas (id, nombre) para el template"""
        return [(region.value, region.display_name) for region in cls]