# Base class for states
class State:
    """Base class for state objects, with default methods to be overridden."""

    def enter(self, npc):
        """Called when the state is entered."""
        pass

    def execute(self, npc):
        """Called during each update while the state is active."""
        pass

    def exit(self, npc):
        """Called when the state is exited."""
        pass


# Idle state
class IdleState(State):
    """State where the NPC is idle and waiting for a trigger to change state."""

    def enter(self, npc):
        print(f"{npc.name} is now idle.")

    def execute(self, npc):
        print(f"{npc.name} is idling.")
        if npc.target_within_range():
            npc.change_state(ChaseState())

    def exit(self, npc):
        print(f"{npc.name} is leaving the idle state.")


# Patrol state
class PatrolState(State):
    """State where the NPC moves between predefined waypoints in the game world."""

    def enter(self, npc):
        print(f"{npc.name} is starting to patrol.")

    def execute(self, npc):
        print(f"{npc.name} is patrolling.")
        if npc.target_within_range():
            npc.change_state(ChaseState())

    def exit(self, npc):
        print(f"{npc.name} is done patrolling.")


# Chase state
class ChaseState(State):
    """State where the NPC chases the player if they are within a certain range."""

    def enter(self, npc):
        print(f"{npc.name} is starting to chase the target.")

    def execute(self, npc):
        print(f"{npc.name} is chasing the target.")
        if not npc.target_within_range():
            npc.change_state(PatrolState())

    def exit(self, npc):
        print(f"{npc.name} is done chasing the target.")


# Non-Player Character (NPC) class
class NPC:
    """Class representing a non-player character (NPC) in a game."""

    def __init__(self, name):
        self.name = name
        self.state = IdleState()
        self.state.enter(self)

    def change_state(self, new_state):
        """Change the current state of the NPC."""
        self.state.exit(self)
        self.state = new_state
        self.state.enter(self)

    def update(self):
        """Update the NPC's behavior based on the current state."""
        self.state.execute(self)

    def target_within_range(self):
        """
        Check if the target is within range, return True or False.
        This method should be implemented based on the game world.
        For this example, we will assume it's always True.
        """
        return True


# Main game loop
if __name__ == "__main__":
    npc = NPC("Guard")
    for _ in range(10):
        npc.update()
