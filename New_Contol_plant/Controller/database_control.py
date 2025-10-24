import sqlite3
import os

class C_palne_Database():
    def __init__(self):
        # ตรวจสอบ Environment Variable 'IS_DOCKER'
        # ถ้าหาไม่เจอ หรือไม่ใช่ 'true' ให้ถือว่ารันบนเครื่องปกติ
        is_docker = os.environ.get('IS_DOCKER', 'false').lower() == 'true'

        if is_docker:
            # --- เส้นทางสำหรับ Docker ---
            # กำหนดเส้นทางตายตัวภายใน Container ที่เราจะ Mount Volume เข้าไป
            # เช่น /app/DATA_BASE (คุณอาจจะต้องเปลี่ยนตาม docker-compose.yml)
            self.db_path = "/app/DATA_BASE/concretePlant.db"
            print(f"[Docker Mode] Using DB path: {self.db_path}") # Debug
        else:
            # --- เส้นทางสำหรับรันปกติ ---
            script_dir = os.path.dirname(__file__)
            db_path_relative = os.path.join(script_dir, "..", "..", "DATA_BASE", "concretePlant.db")
            self.db_path = os.path.normpath(db_path_relative)
            print(f"[Local Mode] Using DB path: {self.db_path}") # Debug

        # --- ส่วนตรวจสอบและสร้างโฟลเดอร์/ไฟล์ ---
        db_dir = os.path.dirname(self.db_path)
        # ตรวจสอบว่า Directory ปลายทางมีอยู่หรือไม่
        if not os.path.exists(db_dir):
            try:
                os.makedirs(db_dir) # ถ้าไม่มี ให้สร้าง
                print(f"Created directory: {db_dir}")
            except OSError as e:
                print(f"!!! Error creating directory {db_dir}: {e}")
                # อาจจะหยุดการทำงาน หรือใช้ path สำรอง ขึ้นอยู่กับการออกแบบ
                # ในกรณีนี้ จะปล่อยให้ sqlite3 จัดการสร้างไฟล์ (ซึ่งอาจจะ fail ถ้า dir ไม่มี)
        elif not os.path.isdir(db_dir):
             print(f"!!! Error: Expected directory but found a file at {db_dir}")
             # ควรจะหยุดการทำงาน เพราะ path ผิดแน่นอน

        # แจ้งเตือนถ้าไฟล์ DB ยังไม่มี (ซึ่งควรจะถูกสร้างโดย sqlite3 ถ้า dir ถูกต้อง)
        if not os.path.exists(self.db_path):
             print(f"Warning: Database file not found at {self.db_path}. It should be created.")

        # --- สิ้นสุดส่วนตรวจสอบ ---

        self.create_offset_table()
        # โค้ดส่วนที่เหลือของ __init__ (ถ้ามี) ควรจะอยู่หลังจากนี้


    def create_offset_table(self):
        conn = None
        try:
            # ตรวจสอบ path อีกครั้งก่อนเชื่อมต่อ
            db_dir = os.path.dirname(self.db_path)
            if not os.path.isdir(db_dir):
                 print(f"!!! Cannot connect to DB: Directory '{db_dir}' does not exist or is not a directory.")
                 return # ออกจากฟังก์ชันถ้า Directory ผิด

            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # 1. สร้างตารางถ้ายังไม่มี
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS offset_settings (
                id INTEGER PRIMARY KEY,
                rock1_offset FLOAT DEFAULT 0,
                sand1_offset FLOAT DEFAULT 0,
                rock2_offset FLOAT DEFAULT 0,
                sand2_offset FLOAT DEFAULT 0,
                cement_offset FLOAT DEFAULT 0,
                fly_ash_offset FLOAT DEFAULT 0,
                water_offset FLOAT DEFAULT 0,
                chem1_offset FLOAT DEFAULT 0,
                chem2_offset FLOAT DEFAULT 0,
                conveyor_time FLOAT DEFAULT 0,
                cement_release_time FLOAT DEFAULT 0,
                mixer_run_time FLOAT DEFAULT 0,
                next_load_time FLOAT DEFAULT 0
            );
            """)


            cursor.execute("""
            INSERT OR IGNORE INTO offset_settings (id) VALUES (1);
            """)

            conn.commit()
            print(f"Database table 'offset_settings' checked/created successfully at {self.db_path}")

        except sqlite3.Error as e:
            print(f"!!! Error interacting with offset_settings table: {e}")
        finally:
            if conn:
                conn.close()


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

    def read_data_in_table_customer(self):
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


    def delete_data_in_table_formula(self,id):
        query = """DELETE FROM concrete_formula WHERE id = ?;"""
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

    def get_data_formula_by_id(self, formula_id):
            query = """SELECT formula_name, rock1_weight, sand_weight, rock2_weight, fly_ash_weight, cement_weight,
                    water_weight, chemical1_weight, chemical2_weight, age, slump
                    FROM concrete_formula WHERE id = ?;"""
            conn = None
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                cursor.execute(query, (formula_id,))
                result = cursor.fetchone()
                return result

            except sqlite3.Error as e:
                print(f"Error fetching formula by id: {e}")
                return None
            finally:
                if conn:
                    conn.close()

    def insert_data_to_table_formula(self,name_formula, rock_1, sand, rock_2, cement, fyash, water, chem_1, chem_2, age, slump): # FORMULA tab
        query = """INSERT INTO concrete_formula (formula_name, rock1_weight, sand_weight, rock2_weight, fly_ash_weight, cement_weight,
                    water_weight, chemical1_weight, chemical2_weight, age, slump, status)
                    VALUES (?,?,?,?,?,?,?,?,?,?,?,1);"""
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(query,(name_formula, rock_1, sand, rock_2, cement, fyash, water, chem_1, chem_2, age, slump))
            conn.commit()
        except sqlite3.Error as e:
            print(f"error {e}")
        finally:
            if conn:
                conn.close()

    def update_data_to_table_formula(self,formula_id, name_formula, rock_1, sand, rock_2, cement, fyash, water, chem_1, chem_2, age, slump): # FORMULA tab
        query = """UPDATE concrete_formula
                    SET formula_name = ?, rock1_weight = ?, sand_weight = ?, rock2_weight = ?, fly_ash_weight = ?, cement_weight = ?,
                        water_weight = ?, chemical1_weight = ?, chemical2_weight = ?, age = ?, slump = ?
                    WHERE id = ?;"""
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(query,(name_formula, rock_1, sand, rock_2, cement, fyash, water, chem_1, chem_2, age, slump, formula_id))
            conn.commit()
        except sqlite3.Error as e:
            print(f"error {e}")
        finally:
            if conn:
                conn.close()

    def check_name_formula_exists(self, name_formula):
        query = "SELECT COUNT(*) FROM concrete_formula WHERE formula_name = ?;"
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(query, (name_formula,))
            count = cursor.fetchone()[0]
            return count > 0
        except sqlite3.Error as e:
            print(f"Error checking formula name existence: {e}")
            return False
        finally:
            if conn:
                conn.close()

    def read_offset_settings(self):
        query = "SELECT * FROM offset_settings WHERE id = 1;"
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(query)
            result = cursor.fetchone()
            return result
        except sqlite3.Error as e:
            print(f"Error reading offset settings: {e}")
            return None
        finally:
            if conn:
                conn.close()

    def update_offset_settings(self, rock1, sand1, rock2, sand2, cement, fyash, water, chem1, chem2, conv_time, cement_time, mixer_time, next_time):
        query = """
        UPDATE offset_settings
        SET
            rock1_offset = ?, sand1_offset = ?, rock2_offset = ?, sand2_offset = ?,
            cement_offset = ?, fly_ash_offset = ?, water_offset = ?,
            chem1_offset = ?, chem2_offset = ?, conveyor_time = ?,
            cement_release_time = ?, mixer_run_time = ?, next_load_time = ?
        WHERE id = 1;
        """
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(query, (
                rock1, sand1, rock2, sand2, cement, fyash, water,
                chem1, chem2, conv_time, cement_time, mixer_time, next_time
            ))
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error updating offset settings: {e}")
        finally:
            if conn:
                conn.close()

    def get_work_queue(self):
        query = """
        SELECT
            c.id, c.name, c.phone_number, c.address, c.formula_name,
            c.amount, c.truck_number, c.batch_state,
            f.rock1_weight, f.sand_weight, f.rock2_weight, f.cement_weight,
            f.fly_ash_weight, f.water_weight, f.chemical1_weight, f.chemical2_weight
        FROM customer c
        JOIN concrete_formula f ON c.formula_name = f.formula_name
        WHERE c.batch_state IN (0, 1);
        """
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            return results
        except sqlite3.Error as e:
            print(f"Error getting work queue: {e}")
            return []
        finally:
            if conn:
                conn.close()

    def update_customer_batch_state(self, customer_id, new_state):
        query = "UPDATE customer SET batch_state = ? WHERE id = ?;"
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(query, (new_state, customer_id))
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error updating customer batch_state: {e}")
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