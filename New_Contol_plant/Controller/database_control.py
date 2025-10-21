import sqlite3
import os


class C_palne_Database():
    def __init__(self):
        script_dir = os.path.dirname(__file__)
        db_path = os.path.join(script_dir, "..", "..", "DATA_BASE", "concretePlant.db")
        db_path = os.path.normpath(db_path) 
        self.db_path = db_path
    
    def delete_data_in_table_customer(self,id): # REG tab
        query = """DELETE FROM customer WHERE id = ?;""" 
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(query,(id,))
            conn.commit()
        except sqlite3.Error as e:
            print(f"error {e}")
        finally:
            if conn:
                conn.close()
                
    def read_data_in_table_formula(self): #reg tab
        query = """SELECT id, formula_name, rock1_weight, sand_weight, rock2_weight, fly_ash_weight, cement_weight, 
                    water_weight, chemical1_weight, chemical2_weight, age, slump FROM 
                    concrete_formula WHERE status = 1;""" 
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            return results
        except sqlite3.Error as e:
            print(f"error {e}")
            return []
        finally:
            if conn:
                conn.close()

    def update_data_to_table_customer(self,name,phone_number,address,formula_name,amount_concrete,car_number,child_cement,comment): # REG tab
        query = """INSERT INTO customer (name, phone_number,address,formula_name,amount,truck_number,batch_state,comments) VALUES (?,?,?,?,?,?,?,?);""" 
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(query,(name, phone_number,address,formula_name,amount_concrete,car_number,child_cement,comment))
            conn.commit()
        except sqlite3.Error as e:
            print(f"error {e}")
        finally:
            if conn:
                conn.close()
    
    def read_data_in_table_customer(self): # REG tab
        query = """SELECT id, name, phone_number,address FROM customer;""" 
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            return results
        except sqlite3.Error as e:
            print(f"error {e}")
            return []
        finally:
            if conn:
                conn.close()

    def read_data_all_in_table_oder(self):
        query = "SELECT * FROM concrete_order;" 
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            return results
        except sqlite3.Error as e:
            print(f"error {e}")
            return []
        finally:
            if conn:
                conn.close()
        
    def get_customer_data_by_id(self, customer_id):
            query = "SELECT name,phone_number,address FROM customer WHERE id = ?;"
            conn = None
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                cursor.execute(query, (customer_id,))
                result = cursor.fetchone() 
                return result
                
            except sqlite3.Error as e:
                print(f"Error fetching customer by id: {e}")
                return None
            finally:
                if conn:
                    conn.close()
                    


if __name__ == "__main__":
    db = C_palne_Database()
    # results = db.read_data_in_table_formula()
    # results = db.read_data_all_in_table_oder()
    results = db.read_data_in_table_customer()
    for row in results:
        print(row)