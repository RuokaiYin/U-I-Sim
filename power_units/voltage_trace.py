import math

class voltage_trace:
    """
    this module trace a voltage trace file and return voltage and time
    """
    def _init_(self):
        self.raw_time = 0
        self.voltage = 0

    """
    this private method return the voltage of the voltage trace file
    """
    def read_voltage(self, path, sample_period):
        voltage_list=voltage_file.read().split("\n")
        length = len(voltage_list)
        for line in range(self.raw_time,length,sample_period):
            self.voltage = (voltage_list[line].split("\t"))[0]
            self.raw_time = (voltage_list[line].split("\t"))[1]
            return self.voltage, self.time

    def forward(self, path, sample_period):
        return self.read_voltage(path, sample_period)