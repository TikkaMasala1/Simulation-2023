# Simulation-2023
### Taran Singh 1789254

Instructions to run the simulation: 

(Note only the files in folder `3-Touring-Machines-and-Electric-elections` are related to the actual simulation, the rest are assignments unrelated to the simulation )
1. Install the packages listed in 'requirements.txt'
2. Change the simulation parameters in the jupyter notebook called `traffic_vis.ipynb` to your preference. (See below for an explanation of the parameters)
3. Run the jupyter notebook called `traffic_vis.ipynb`
4. Profit?

## Simulation Parameters
The traffic simulation is controlled by the following parameters:
1. `road_length`: The length of the one-lane road in the simulation. A larger value represents a longer road, allowing more space for vehicles to move, while a smaller value represents a shorter road, which might result in more congestion and reduced traffic flow. <br />Example: `road_length` = 100
2. `vehicle_count`: The total number of vehicles in the simulation. A higher value leads to more vehicles on the road, potentially increasing the chances of congestion and slower traffic, while a smaller value means fewer vehicles, which could result in faster traffic flow.<br />Example: `vehicle_count` = 20
3. `max_speed`: The maximum speed that a vehicle can achieve in the simulation. A higher value allows vehicles to move faster, potentially improving traffic flow, while a smaller value limits the speed of the vehicles, possibly leading to slower traffic flow.<br />Example: `max_speed` = 5
4. `slowdown_probability`: The probability of a vehicle randomly slowing down by 1 unit in each time step. A higher value increases the chances of vehicles slowing down, causing fluctuations in traffic flow and possibly resulting in congestion, while a smaller value decreases the chances of vehicles slowing down, leading to more consistent traffic flow.<br />Example: `slowdown_probability` = 0.5
5. `steps`: The number of time steps the simulation will run. Each step allows the vehicles to move according to the Nagel-Schreckenberg model. A higher value provides more opportunities for the vehicles to interact and evolve their states, while a smaller value results in a shorter simulation with fewer interactions.<br />Example: `steps` = 50
