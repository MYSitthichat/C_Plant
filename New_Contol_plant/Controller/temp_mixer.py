from PySide6.QtCore import QObject

class TempMixer(QObject):
    def __init__(self, id, dTime, customer_id, name, phone_number, address, formula_name,
                 amount, keep_time, truck_number, rock1_weight, sand_weight, rock2_weight,
                 cement_weight, fly_ash_weight, water_weight, chem1_weight, chem2_weight,
                 age, slump, batch_state):
        super(TempMixer, self).__init__()
        self.rock1_total_weight = 0
        self.sand_total_weight = 0
        self.rock2_total_weight = 0
        self.cement_total_weight = 0
        self.fly_ash_total_weight = 0
        self.water_total_weight = 0
        self.chem1_total_weight = 0
        self.chem2_total_weight = 0

        self.id = id                        
        self.dTime = dTime                 
        self.customer_id = customer_id
        self.name = name                    
        self.phone_number = phone_number    
        self.address = address
        self.formula_name = formula_name  
        self.amount = amount               
        self.keep_time = keep_time          
        self.truck_number = truck_number    
        self.rock1_weight = rock1_weight
        self.sand_weight = sand_weight
        self.rock2_weight = rock2_weight
        self.cement_weight = cement_weight
        self.fly_ash_weight = fly_ash_weight
        self.water_weight = water_weight
        self.chem1_weight = chem1_weight
        self.chem2_weight = chem2_weight
        self.age = age                      
        self.slump = slump                  
        self.batch_state = batch_state      

    