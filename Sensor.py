import numpy.random as random

#Sensor emulator
class Sensor:
    def __init__(self, name):
        # Name of the Sensor (ex. SPS30)
        self.name = name

        # Formulas to simulate sensr mesurments
        self.formulas = {}

        # Dependencies used in formulas for this sensor
        self.dependencies = {}

    # Add formulas to simulate sensr mesurments
    # Use: .add_measurement('teperature', '2+d.pressure*r(10,2)')
    def add_measurement(self, name, formula):
        self.formulas[name] = formula

    # Add dependencies used in formulas for this sensor
    #Use .add_dependency('pressure', 1035)
    def add_dependency(self, name, function, id):
        self.dependencies[name]={'foo':function, 'id':id}

    def update(self):
        self.mesurments={}
        for key, value in self.formulas.items():
            self.mesurments[key] = self.count(value)

    def count(self, formula):

        #   Varibles for formulas

        r=self.randomizer

        #   Use in formulas: r(numer, range)
        #   - number - base numer to randomize
        #   - range - max differ range from number

        # Create object from dictionary with dependencies

        class SensorDependenie(object):
            def __init__(self, dep):
                self._dep = dep

            # Transform dictionary of dependencies into arguments
            # Arguments beegined with '_' aren't parsed as dependency
            def __getattribute__(self, key):
                if key[0] != '_':
                    return self._dep[key]['foo'](self._dep[key]['id'])
                else:
                     return super().__getattribute__(key)

        # d - collable object with dependencies as attributes

        d = SensorDependenie(self.dependencies)

        # Use in formulas: d.pressure
        # Attribute must be defined by add_dependency

        # Evaluates formula
        return eval(formula)

    # randomizer picks random number from range(min, max)
    def randomizer(self, min, max):
        return random.uniform(min, max)

# Example code:
'''
g=Sensor('GPS')
g.add_dependency('jeden', 1)
g.add_measurement('x', '1+d.jeden*3')
g.update()
print(g.mesurments)
'''
