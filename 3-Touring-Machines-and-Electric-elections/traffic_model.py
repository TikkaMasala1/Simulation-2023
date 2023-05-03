from mesa import Model, Agent
from mesa.space import SingleGrid
from mesa.time import RandomActivation


# Define the Vehicle agent class
class Vehicle(Agent):
    def __init__(self, unique_id, model, max_speed, start_speed=0):
        super().__init__(unique_id, model)
        self.speed = start_speed  # The current speed of the vehicle
        self.max_speed = max_speed  # The maximum speed of the vehicle

    # Define the step function for the Vehicle agent
    def step(self):
        # Accelerate if the vehicle's speed is less than its maximum speed, increase its speed by 1
        if self.speed < self.max_speed:
            self.speed += 1

        # Decelerate due to other vehicles
        # Calculate the distance to the next vehicle in front and adjust speed accordingly
        next_vehicle_distance = 0
        while self.model.grid.is_cell_empty(
                ((self.pos[0] + next_vehicle_distance + 1) % self.model.grid.width, 0)):
            next_vehicle_distance += 1

        if self.speed > next_vehicle_distance:
            self.speed = next_vehicle_distance

        # Randomization If the vehicle's speed is greater than 0 and a random number is less than the slowdown
        # probability, decrease the speed by 1
        if self.speed > 0 and self.random.random() < self.model.slowdown_probability:
            self.speed -= 1

        # Update the vehicle's position based on its current speed
        new_position = ((self.pos[0] + self.speed) % self.model.grid.width, 0)

        # Check if the target cell is empty
        if self.model.grid.is_cell_empty(new_position):
            self.model.grid.move_agent(self, new_position)
        else:
            # Adjust the speed to avoid the collision
            self.speed = 0


# Define the TrafficModel class that inherits from the Mesa Model class
class TrafficModel(Model):
    def __init__(self, road_length, vehicle_count, max_speed, slowdown_probability):
        # Create a grid with the specified road_length and wraparound (torus) enabled
        self.grid = SingleGrid(road_length, 1, torus=True)
        self.schedule = RandomActivation(self)  # Schedule for updating agents in random order
        self.slowdown_probability = slowdown_probability  # Probability of vehicles slowing down

        # Create a list of available positions
        available_positions = list(range(road_length))
        self.random.shuffle(available_positions)

        # Create normal vehicles
        for i in range(vehicle_count):
            vehicle = Vehicle(i, self, max_speed)
            position = available_positions.pop()
            self.grid.place_agent(vehicle, (position, 0))
            self.schedule.add(vehicle)

    # Define the step function for the TrafficModel
    def step(self):
        self.schedule.step()  # Update all agents in the model
