import random
from collections import defaultdict
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
        # Accelerate If the vehicle's speed is less than its maximum speed, increase its speed by 1
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


class SlowVehicle(Vehicle):
    def __init__(self, unique_id, model, max_speed, start_speed=0):
        super().__init__(unique_id, model, max_speed, start_speed)
        self.braking_distance = 2  # Additional braking distance for slow vehicles

    # Define the step function for the Vehicle agent
    def step(self):
        # Accelerate If the vehicle's speed is less than its maximum speed, increase its speed by 1
        if self.speed < self.max_speed:
            self.speed += 1

        # Decelerate due to other vehicles
        # Calculate the distance to the next vehicle in front and adjust speed accordingly
        next_vehicle_distance = 0
        while self.model.grid.is_cell_empty(
                ((self.pos[0] + next_vehicle_distance + self.braking_distance) % self.model.grid.width, 0)):
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
    def __init__(self, road_length, vehicle_count, max_speed, slowdown_probability, slow_vehicle_count=0,
                 slow_vehicle_max_speed=None):
        # Create a grid with the specified road_length and wraparound (torus) enabled
        self.grid = SingleGrid(road_length, 1, torus=True)
        self.schedule = RandomActivation(self)  # Schedule for updating agents in random order
        self.slowdown_probability = slowdown_probability  # Probability of vehicles slowing down
        self.events = defaultdict(list)

        # Create a list of available positions
        available_positions = list(range(road_length))
        self.random.shuffle(available_positions)

        # Set the slow vehicle's maximum speed to half of the regular vehicle's max speed if it's not provided
        if slow_vehicle_max_speed is None:
            slow_vehicle_max_speed = max_speed // 2

        # Create normal vehicles
        for i in range(vehicle_count - slow_vehicle_count):
            vehicle = Vehicle(i, self, max_speed)
            position = available_positions.pop()
            self.grid.place_agent(vehicle, (position, 0))
            self.schedule.add(vehicle)

        # Create slow vehicles with lower max speed
        for i in range(vehicle_count - slow_vehicle_count, vehicle_count):
            slow_vehicle = SlowVehicle(i, self, slow_vehicle_max_speed)
            position = available_positions.pop()
            self.grid.place_agent(slow_vehicle, (position, 0))
            self.schedule.add(slow_vehicle)

        self.step_count = 0

    def calculate_average_speed(self):
        # Calculate the average speed of all vehicles in the simulation. This method computes the sum of speeds of
        # all agents (vehicles) in the schedule and divides it by the total number of agents. The result is the
        # average speed
        total_speed = sum([agent.speed for agent in self.schedule.agents])
        average_speed = total_speed / len(self.schedule.agents)
        return average_speed

    def add_event(self, step, event, repeat_every=None, *args, **kwargs):
        # Add an event to the model at the specified step or every certain number of steps
        # The event is stored as a tuple containing the event function, its arguments, and keyword arguments
        self.events[step].append((event, args, kwargs, repeat_every))

    def step(self):
        # Execute the scheduled agents' steps
        self.schedule.step()

        # Execute events for the current step
        # Iterate through the list of events for the current step count
        for event, args, kwargs, repeat_every in self.events[self.step_count]:
            event(*args, **kwargs)
            # Call the event function with its arguments and keyword arguments
            if repeat_every is not None:
                next_step = self.step_count + repeat_every
                self.add_event(next_step, event, repeat_every, *args, **kwargs)

        # Increment the step counter
        self.step_count += 1
