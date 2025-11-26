# app/core/domain/value_objects/systems.py
from enum import Enum

# SYSTEMS
class SystemValueObject(Enum):
    JITA = 30000142
    PERIMETER = 30000144
    AMARR = 30002187
    DODIXIE = 30002659
    RENS = 30002510

    @property
    def display_name(self):
        """Nombre legible para el sistema"""
        names = {
            self.JITA: "Jita",
            self.PERIMETER: "Perimeter",
            self.AMARR: "Amarr",
            self.DODIXIE: "Dodixie",
            self.RENS: "Renos"
        }
        return names[self]
    
    @classmethod
    def get_choices(cls):
        """Obtener lista de tuplas (id, nombre) para el template"""
        return [(system.value, system.display_name) for system in cls]
