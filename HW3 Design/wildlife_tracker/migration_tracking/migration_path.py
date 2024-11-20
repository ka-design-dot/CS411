from typing import Optional, Any
from wildlife_tracker.habitat_management.habitat import Habitat
from wildlife_tracker.animal_management.animal import Animal
from wildlife_tracker.migration_tracking.migration import Migration

class MigrationPath:

    def __init__ (self,
                  path_id: int,
                  species: str,
                  start_location: Habitat,
                  destination: Habitat,
                  duration: Optional[int] = None):
            self.path_id = path_id
            self.species = species
            self.start_location = start_location
            self.destination = destination
            self.duration = duration

    def get_migration_path_details(path_id) -> dict:
        pass


                  
                  
                  
                  
    