# สรุปปัญหา Error ตอนเริ่มโหลด Batch

วันที่วิเคราะห์: 2026-06-16

## Log ที่พบ

```text
ERROR - Error reading chemical weight from lineEdit
ERROR - Error reading sand weight
ERROR - Error reading rock 1 weight
```

หมายเหตุ: `END BATCH LOGGING` ใน log เกิดจากการกดหยุดงานเอง จึงไม่ใช่สาเหตุของ error นี้

## สาเหตุโดยตรง

error เกิดจากโปรแกรมพยายามอ่านค่าน้ำหนักเริ่มต้นจากช่อง monitor ใน UI แล้วแปลงเป็นตัวเลข แต่ช่องยังเป็นค่าว่างหรือไม่ใช่ตัวเลข

จุดที่เกิดใน `Controller/main_controller.py`:

- `loading_chemical_sequence()` อ่าน `mix_monitor_chem_1_lineEdit`
- `load_rock_and_sand_sequence()` อ่าน `mix_monitor_sand_lineEdit`
- ถ้าอ่าน sand ไม่ได้ จะ fallback ไปอ่าน `mix_monitor_rock_1_lineEdit`

รูปแบบ error จริงที่น่าจะเกิด แต่ถูก `except:` กลืนไว้ คือประมาณนี้:

```text
ValueError: could not convert string to float: ''
ValueError: invalid literal for int() with base 10: ''
```

## ทำไมช่องถึงว่าง

1. ช่อง monitor ถูกสร้างใน `View/main_frame.py` แต่ไม่ได้ตั้งค่าเริ่มต้นเป็น `"0"`

   ตัวอย่างช่องที่เกี่ยวข้อง:

   - `mix_monitor_rock_1_lineEdit`
   - `mix_monitor_sand_lineEdit`
   - `mix_monitor_chem_1_lineEdit`

2. ตอนเลือกงานใน `Controller/load_work_queue.py` มีการเรียก `clear_mixer_monitors()` แต่ฟังก์ชันนี้ reset เฉพาะช่อง `mix_wieght_Loaded_*` ไม่ได้ reset ช่อง `mix_monitor_*`

3. ช่อง `mix_monitor_*` จะถูก set เป็น `"0"` ใน `_reset_ui_safe()` ของ `Controller/main_controller.py` แต่ฟังก์ชันนี้ไม่ได้ถูกเรียกตอนเริ่มงานใหม่ทุกครั้ง

4. ค่า monitor จะถูกเติมจาก AutoDA ผ่าน signal เช่น `update_weight_rock_and_sand()` และ `update_weight_chemical()` แต่ถ้า AutoDA ยังไม่ส่งค่าทันก่อน thread เริ่มอ่าน ช่องก็ยังว่าง

## Timing ที่ทำให้เกิดได้ง่าย

- Chemical รอแค่ `0.5` วินาทีก่อนอ่าน `mix_monitor_chem_1_lineEdit`
- Rock/Sand รอ `5` วินาทีก่อนอ่าน `mix_monitor_sand_lineEdit`

ถ้า AutoDA ยังไม่ update ค่าเข้าหน้า UI ภายในเวลานี้ จะเกิด error ทันที แล้วโปรแกรมจะใช้ค่า fallback เป็น `0`

## ผลกระทบ

- error นี้ไม่ได้ทำให้โปรแกรม crash เพราะมี `except:` รองรับไว้
- แต่ทำให้ initial weight ถูกตีเป็น `0`
- หากค่าน้ำหนักค้างจริงในเครื่องชั่งมีอยู่ โปรแกรมอาจคำนวณ setpoint ผิด เพราะไม่ได้เอาค่าน้ำหนักค้างมาบวก
- อาจทำให้ workflow รออยู่ที่ `State 0 waiting` ต่อไป ถ้าวัสดุทั้ง 4 กลุ่มยังไม่ถูก mark ว่าโหลดสำเร็จ

## ข้อสรุป

สาเหตุหลักคือช่อง monitor น้ำหนักใน UI ยังไม่มีค่าเริ่มต้นเป็นตัวเลขตอนเริ่มโหลด batch โดยเฉพาะ `mix_monitor_chem_1_lineEdit`, `mix_monitor_sand_lineEdit`, และ `mix_monitor_rock_1_lineEdit`

จุดที่ควรตรวจหรือแก้ต่อ:

- ตั้งค่า monitor ทุกช่องเป็น `"0"` ตอนเลือกงานหรือก่อนเริ่มโหลด
- ทำให้ `clear_mixer_monitors()` reset ทั้ง `mix_wieght_Loaded_*` และ `mix_monitor_*`
- อ่านค่า lineEdit แบบปลอดภัย เช่น ถ้าว่างให้ใช้ `0`
- เพิ่ม log ให้แสดงค่าจริงใน lineEdit ก่อนแปลงเป็นตัวเลข เพื่อยืนยันตอนทดสอบกับเครื่องจริง
