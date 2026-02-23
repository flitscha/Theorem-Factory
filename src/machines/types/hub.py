from machines.base.machine import Machine

class Hub(Machine):
    def __init__(self, machine_data, rotation=0):
        super().__init__(machine_data, rotation=rotation)
