from Controller.temp_mixer import TempMixer
import sqlite3
import os
from datetime import datetime

class InsertToCustomerOrder:
    def __init__(self):
        is_docker = os.environ.get('IS_DOCKER', 'false').lower() == 'true'
        
        if is_docker:
            self.db_path = "/app/DATA_BASE/concretePlant.db"
        else:
            script_dir = os.path.dirname(__file__)
            db_path_relative = os.path.join(script_dir, "..", "..", "DATA_BASE", "concretePlant.db")
            self.db_path = os.path.normpath(db_path_relative)
    
    def insert(self, temp_mixer):
        if not isinstance(temp_mixer, TempMixer):
            print("Error: temp_mixer must be a TempMixer object")
            return None
        
        query = """
        INSERT INTO concrete_order (
            dTime, customer_name, phone_number, address, formula_name, 
            amount, keep_sample, truck_number,
            rock1_total_weight, sand_total_weight, rock2_total_weight, 
            cement_total_weight, fly_ash_total_weight, water_total_weight, 
            chemical1_total_weight, chemical2_total_weight,
            roc1_target_weight, sand_target_weight, rock2_target_weight, 
            cement_target_weight, fly_ash_target_weight, water_target_weight, 
            chemical1_target_weight, chemical2_target_weight,
            age, slump, batch_state
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """
        
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Prepare values from TempMixer
            values = (
                temp_mixer.dTime,                      # dTime
                temp_mixer.name,                       # customer_name
                temp_mixer.phone_number,               # phone_number
                temp_mixer.address,                    # address
                temp_mixer.formula_name,               # formula_name
                temp_mixer.amount,                     # amount
                temp_mixer.keep_time,                  # keep_sample (using keep_time)
                temp_mixer.truck_number,               # truck_number
                # Actual weights (total loaded during production)
                temp_mixer.rock1_total_weight,         # rock1_total_weight
                temp_mixer.sand_total_weight,          # sand_total_weight
                temp_mixer.rock2_total_weight,         # rock2_total_weight
                temp_mixer.cement_total_weight,        # cement_total_weight
                temp_mixer.fly_ash_total_weight,       # fly_ash_total_weight
                temp_mixer.water_total_weight,         # water_total_weight
                temp_mixer.chem1_total_weight,         # chemical1_total_weight
                temp_mixer.chem2_total_weight,         # chemical2_total_weight
                # Target weights (from formula)
                temp_mixer.rock1_weight,               # roc1_target_weight (note: typo in DB column name)
                temp_mixer.sand_weight,                # sand_target_weight
                temp_mixer.rock2_weight,               # rock2_target_weight
                temp_mixer.cement_weight,              # cement_target_weight
                temp_mixer.fly_ash_weight,             # fly_ash_target_weight
                temp_mixer.water_weight,               # water_target_weight
                temp_mixer.chem1_weight,               # chemical1_target_weight
                temp_mixer.chem2_weight,               # chemical2_target_weight
                temp_mixer.age,                        # age
                temp_mixer.slump,                      # slump
                temp_mixer.batch_state                 # batch_state
            )
            
            cursor.execute(query, values)
            conn.commit()
            
            new_id = cursor.lastrowid
            print(f"✓ Successfully inserted record to concrete_order with ID: {new_id}")
            return new_id
            
        except sqlite3.Error as e:
            print(f"✗ Error inserting to concrete_order table: {e}")
            print(f"  Database path: {self.db_path}")
            return None
            
        finally:
            if conn:
                conn.close()

