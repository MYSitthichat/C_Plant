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
    
    def insert_start(self, temp_mixer):
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
            age, slump, batch_state, Status_load
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """
        
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Prepare values - all totals are 0, Status_load = 0
            values = (
                temp_mixer.dTime,                      # dTime
                temp_mixer.name,                       # customer_name
                temp_mixer.phone_number,               # phone_number
                temp_mixer.address,                    # address
                temp_mixer.formula_name,               # formula_name
                temp_mixer.amount,                     # amount
                temp_mixer.keep_time,                  # keep_sample
                temp_mixer.truck_number,               # truck_number
                # All actual weights START at 0
                0.0,                                   # rock1_total_weight = 0
                0.0,                                   # sand_total_weight = 0
                0.0,                                   # rock2_total_weight = 0
                0.0,                                   # cement_total_weight = 0
                0.0,                                   # fly_ash_total_weight = 0
                0.0,                                   # water_total_weight = 0
                0.0,                                   # chemical1_total_weight = 0
                0.0,                                   # chemical2_total_weight = 0
                # Target weights (from formula)
                temp_mixer.rock1_weight,               # roc1_target_weight
                temp_mixer.sand_weight,                # sand_target_weight
                temp_mixer.rock2_weight,               # rock2_target_weight
                temp_mixer.cement_weight,              # cement_target_weight
                temp_mixer.fly_ash_weight,             # fly_ash_target_weight
                temp_mixer.water_weight,               # water_target_weight
                temp_mixer.chem1_weight,               # chemical1_target_weight
                temp_mixer.chem2_weight,               # chemical2_target_weight
                temp_mixer.age,                        # age (from formula)
                temp_mixer.slump,                      # slump (from formula)
                temp_mixer.batch_state,                # batch_state (2 = in progress)
                0                                      # Status_load = 0 (not loaded)
            )
            
            cursor.execute(query, values)
            conn.commit()
            
            new_id = cursor.lastrowid
            return new_id
            
        except sqlite3.Error as e:
            print(f"✗ Error inserting start record: {e}")
            print(f"  Database path: {self.db_path}")
            return None
            
        finally:
            if conn:
                conn.close()
    def update_complete(self, record_id, temp_mixer):
        if not isinstance(temp_mixer, TempMixer):
            print("Error: temp_mixer must be a TempMixer object")
            return False
        
        if not record_id:
            print("Error: record_id is required")
            return False
        
        query = """
        UPDATE concrete_order SET
            rock1_total_weight = ?,
            sand_total_weight = ?,
            rock2_total_weight = ?,
            cement_total_weight = ?,
            fly_ash_total_weight = ?,
            water_total_weight = ?,
            chemical1_total_weight = ?,
            chemical2_total_weight = ?,
            Status_load = ?
        WHERE id = ?;
        """
        
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Prepare update values with ACTUAL loaded weights
            # batch_state is NOT updated - it stays 0 or 1 from keep_sample
            values = (
                temp_mixer.rock1_total_weight,         # Actual rock1 loaded
                temp_mixer.sand_total_weight,          # Actual sand loaded
                temp_mixer.rock2_total_weight,         # Actual rock2 loaded
                temp_mixer.cement_total_weight,        # Actual cement loaded
                temp_mixer.fly_ash_total_weight,       # Actual fly_ash loaded
                temp_mixer.water_total_weight,         # Actual water loaded
                temp_mixer.chem1_total_weight,         # Actual chem1 loaded
                temp_mixer.chem2_total_weight,         # Actual chem2 loaded
                1,                                     # Status_load = 1 (loaded/completed)
                record_id                              # WHERE id = record_id
            )
            
            cursor.execute(query, values)
            conn.commit()
            
            if cursor.rowcount > 0:
                keep_text = "ต้องการเก็บ" if temp_mixer.batch_state == 1 else "ไม่ต้องการเก็บ"
                return True
            else:
                print(f"✗ No record found with ID: {record_id}")
                return False
            
        except sqlite3.Error as e:
            print(f"✗ Error updating complete record: {e}")
            print(f"  Database path: {self.db_path}")
            return False
            
        finally:
            if conn:
                conn.close()