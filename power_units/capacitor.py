import math

class capacitor:
    """
    this module simulate the performance of a real capacitor.
    """
    def _init_(self, 
                capacitance,
                max_voltage, 
                max_current):
        
        self.capacitance = capacitance
        self.max_voltage = max_voltage
        self.max_current = max_current

        self.voltage = 0
        self.energy_stored = 0
        self.max_energy =  0.5*self.capacitance*(self.max_voltage**2)*1e9
    

    """
    this private method update the voltage according to the current energy.
    """
    def update_voltage(self):
        self.voltage = math.sqrt(2*self.energy*(1e-9)/self.capacitance)


    """
    this private method update the current energy store in capacitor.
    """
    def update_energy(self, mode, energy_input):
        
        ## Accordingly update the energy 
        if mode is "consume":
            if energy_input < 0:
                raise ValueError("comsumed energy must be positive.")
            elif (self.energy_stored - energy_input) <0:
                raise ValueError("Cannot consume more energy than the capacitor has.")
            else:
                self.energy_stored = self.energy_stored - energy_input
        elif mode is "harvest":
            if energy_input < 0:
                raise ValueError("harvest energy must be positive.")
            elif (self.energy_stored + energy_input) > self.max_energy:
                raise ValueError("Cannot harvest more energy than the capacitor can have.")
            else:
                self.energy_stored = min(self.energy_stored + energy_input, self.max_energy)
        else:
            raise ValueError("mode is not implemented, only use consume, or harvest")

        self.update_voltage()
        ## Calculate the energy stored in a capacitor
        self.energy_stored = 0.5*self.capacitance*(V**2)*1e9

        return self.energy_stored, self.voltage


    def forward(self, mode, energy_input):
        return self.update_energy(self, mode, energy_input)
        