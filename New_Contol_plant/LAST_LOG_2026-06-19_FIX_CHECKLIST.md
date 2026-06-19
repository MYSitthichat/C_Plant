# Last Log 2026-06-19 Issue Analysis And Fix Checklist

เอกสารนี้ทำขึ้นเพื่อใช้ตรวจงานจาก log หน้างานในโฟลเดอร์ `logs/last_log`
และใช้เป็น checklist สำหรับไล่แก้ปัญหาชุดล่าสุด

> สถานะเอกสาร: วิเคราะห์แล้ว แก้โค้ดตาม checklist หลักแล้ว และรอทดสอบกับ PLC/AutoDA จริง

## ไฟล์ที่ใช้ตรวจสอบ

- `logs/last_log/log_Batch_2026-06-19_12-15-08.txt`
- `logs/last_log/log_Batch_2026-06-19_13-00-41.txt`
- `logs/last_log/system_2026-06-19.log`
- รูปประกอบจากหน้างาน:
  - `logs/last_log/cplant.png`
  - `logs/last_log/cplant2.png`

## อาการที่ได้รับแจ้ง

- เติมทรายได้
- เติมน้ำได้
- เติม flyash ได้
- เติมน้ำยา 1 ได้
- หิน 1 เติมแล้วไม่ยอมตัดตามเป้า และไหลเลยไปเกิน 1000 kg
- น้ำ / flyash / น้ำยา 1 ถึงเป้าแล้ว แต่ UI ยังไม่กลับเป็นสีปกติ
- ระหว่างโหลดวัตถุดิบมีอาการช้ามาก
- ทรายตั้งเป้า 970 kg และ offset 50 kg จึงควรส่ง setpoint 920 kg แต่โหลดเลยไปประมาณ 943 kg แล้วแจ้งว่าทรายเปียก

## สรุปสาเหตุหลัก

ปัญหาหลักไม่ได้อยู่ที่ AutoDA setpoint เป็นหลัก เพราะ log แสดงว่า AutoDA เขียน setpoint และอ่าน feedback setpoint กลับมาได้หลายรายการ

สาเหตุหลักที่พบคือ:

1. PLC write queue มีโอกาสทำคำสั่งหาย
2. คำสั่ง PLC start/stop จำนวนมากจบด้วย `success=False, result='None'`
3. state machine รอ PLC finish feedback มากเกินไป
4. เมื่อ weight ถึง setpoint แล้ว โปรแกรมยังไม่มี fallback ที่มั่นคงพอสำหรับสั่ง stop/freeze จากน้ำหนัก AutoDA
5. มีโอกาสที่ finish flag จาก PLC ค้างหรือถูกใช้ผิด phase
6. ข้อความ `sand is moist` รอบนี้มีโอกาสสูงว่าเป็น false alarm จาก PLC feedback/stop ไม่มา ไม่ใช่ทรายเปียกจริง

## หลักฐานสำคัญจาก Log

### 1. AutoDA setpoint เขียนและอ่านกลับได้

จาก `log_Batch_2026-06-19_13-00-41.txt`

- Chemical 1 confirmed ที่ 1.6
- Water confirmed ที่ 160
- Flyash confirmed ที่ 37
- Sand confirmed ที่ 920
- Rock1 confirmed ที่ 1220

ดังนั้นจุดนี้บอกว่า AutoDA ไม่ใช่จุดเสียหลักในรอบนี้

### 2. ค่า offset ทรายถูกต้องเป็น 50

จาก log:

```text
setpoint_calculated | sequence='rock_sand',
sand=920,
rock1=1220,
rock2=1920,
offsets={'sand': 50.0, 'rock1': 100.0, 'rock2': 100.0}
```

สรุป: รอบนี้ระบบใช้ sand offset = 50 ถูกต้องตามที่ยืนยันแล้ว

### 3. คำสั่ง PLC หลายตัวล้มเหลว

จาก `log_Batch_2026-06-19_13-00-41.txt`

- `loading_chemical_1_start` -> `success=False, result='None'`
- `loading_flyash_start` -> `success=False, result='None'`
- `loading_water_start` -> `success=False, result='None'`
- `loading_sand_start` -> `success=False, result='None'`
- `loading_sand_stop` -> `success=False, result='None'` หลายครั้ง
- `loading_rock1_start` -> `success=False, result='None'`

ผลกระทบ:

- สั่ง start/stop ไปแล้ว แต่ไม่มีหลักฐานว่า PLC รับคำสั่งสำเร็จ
- คำสั่ง stop ที่ควรตัดวัตถุดิบอาจไม่ถึง PLC
- UI อาจค้างสีเขียวเพราะ state completion flag ไม่ถูก set

### 4. State completion flag ไม่ขึ้น

จาก log มีข้อความซ้ำ:

```text
State 0 waiting - Flags: R&S=False, C&F=False, W=False, Chem=False
```

ทั้งที่ในภาพและ log น้ำ / flyash / น้ำยา 1 มีน้ำหนักถึงเป้าแล้ว

ผลกระทบ:

- โปรแกรมรู้ว่าน้ำหนักเพิ่ม แต่ไม่ถือว่า phase เสร็จ
- UI ไม่กลับสีปกติ
- batch ไม่ไปต่ออย่างถูกต้อง

### 5. Sand moist เป็น false alarm ได้

จาก log:

```text
sand is moist
sand is moist and count tinout = 3 this skip sand loading
```

แต่จากอาการจริง น้ำหนักยังเพิ่มและไปถึง/เกิน target

สรุป:

- ไม่ควรสรุปว่าเป็นทรายเปียกทันที
- ควรแยกกรณี `น้ำหนักไม่ขยับจริง` ออกจาก `PLC feedback ไม่มา`

## คำตอบเรื่อง Write Setpoint ให้ AutoDA

เมื่อแก้ไขแล้ว โปรแกรมไม่ควร write setpoint ใหม่ทุกครั้งที่น้ำหนักถึงหรือเกินเป้า

แนวทางที่ถูกต้อง:

- Write setpoint ตอนเริ่ม phase
- Read back เพื่อ confirm ว่า AutoDA รับ setpoint ถูกต้อง
- ระหว่างโหลดให้ monitor weight จาก AutoDA
- ถ้าน้ำหนักถึงหรือเกิน active setpoint ให้สั่ง PLC stop ทันที
- ไม่ต้อง write setpoint เดิมซ้ำ
- Write setpoint ใหม่เฉพาะตอนเปลี่ยน phase เช่น:
  - Sand -> Rock1
  - Rock1 -> Rock2
  - Flyash -> Cement
  - Chemical 1 -> Chemical 2

## แนวทางแก้ PLC สื่อสารติดขัด

### หลักการ

PLC command ต้องเป็นระบบที่เชื่อถือได้มากกว่าเดิม โดยเฉพาะคำสั่ง `stop`

### สิ่งที่ต้องแก้

- ห้าม pop คำสั่งออกจาก queue ก่อนส่งสำเร็จ
- ถ้าส่งไม่สำเร็จ ต้อง retry/requeue
- คำสั่ง stop ต้องมี priority สูงกว่า start
- ระหว่างมี write pending ควรลดหรือ pause การ read status ชั่วคราว
- ต้อง log สาเหตุของ `None` ให้ชัดเจน
- ถ้า retry ครบแล้วยัง stop ไม่สำเร็จ ต้องเข้า fault state และแจ้ง operator
- ไม่ควรถือว่าโหลดเสร็จ หากยังไม่มีหลักฐานว่าคำสั่ง stop ส่งสำเร็จหรือมี fallback ที่ปลอดภัยพอ

## Checklist ตรวจงาน

### A. งานวิเคราะห์

- [x] ตรวจ log ใน `logs/last_log`
- [x] ตรวจ batch `2026-06-19_12-15-08`
- [x] ตรวจ batch `2026-06-19_13-00-41`
- [x] ตรวจ `system_2026-06-19.log`
- [x] ยืนยันว่า sand offset รอบนี้เป็น 50
- [x] แยกปัญหา AutoDA ออกจาก PLC command/feedback
- [x] ยืนยันว่า AutoDA setpoint ส่วนใหญ่เขียนและอ่านกลับได้
- [x] พบหลักฐาน PLC write command fail เป็น `None`
- [x] พบจุดเสี่ยง PLC queue drop command
- [x] พบ false alarm ของ `sand is moist`

### B. งานแก้ PLC Queue

- [x] แก้ `process_write_queue()` ไม่ให้ `pop(0)` ก่อนส่งสำเร็จ
- [x] เพิ่ม retry count ต่อคำสั่ง PLC แต่ละรายการ
- [x] เพิ่ม requeue เมื่อ `safe_modbus_operation()` คืน `None`
- [x] เพิ่ม priority ให้คำสั่ง stop มากกว่า start
- [x] จำกัด queue duplicate โดยไม่ลบคำสั่งสำคัญผิดตัว
- [x] เพิ่ม log เมื่อ command ถูก retry
- [x] เพิ่ม log เมื่อ command ถูก drop หลัง retry ครบ
- [x] เพิ่ม fault state เมื่อ stop command ส่งไม่สำเร็จหลัง retry ครบ

### C. งานแก้ PLC Communication

- [x] แยกสาเหตุ `None` ใน `safe_modbus_operation()`
- [x] Log กรณี communication delay
- [x] Log กรณี cooldown จาก error count
- [x] Log exception จริงจาก Modbus
- [x] Log timeout/no response ให้ชัดเจน
- [x] เพิ่ม reconnect เมื่อ PLC no response ต่อเนื่อง
- [x] Pause/reduce read status ระหว่างมี write command ค้าง
- [ ] ตรวจว่าค่า timeout/communication delay เหมาะกับ hardware จริง

### D. งานเพิ่ม Weight Target Guard

- [x] เพิ่ม guard สำหรับ Sand เมื่อ current weight >= sand setpoint
- [x] เพิ่ม guard สำหรับ Rock1 เมื่อ current total >= rock1 setpoint
- [x] เพิ่ม guard สำหรับ Rock2 เมื่อ current total >= rock2 setpoint
- [x] เพิ่ม guard สำหรับ Flyash เมื่อ current weight >= flyash setpoint
- [x] เพิ่ม guard สำหรับ Cement เมื่อ current total >= cement setpoint
- [x] เพิ่ม guard สำหรับ Water เมื่อ current weight >= water setpoint
- [x] เพิ่ม guard สำหรับ Chemical 1 เมื่อ current weight >= chem1 setpoint
- [x] เพิ่ม guard สำหรับ Chemical 2 เมื่อ current total >= chem2 setpoint
- [x] เมื่อ guard ทำงาน ต้องสั่ง PLC stop ทันที
- [x] เมื่อ guard ทำงาน ต้อง log ว่าเป็น `weight_target_reached`
- [x] เมื่อ guard ทำงาน ต้องไม่ write setpoint เดิมซ้ำ

### E. งานแก้ Completion / Freeze Logic

- [x] แยก success flag ของ Sand, Rock1, Rock2
- [x] แยก success flag ของ Flyash, Cement
- [x] แยก success flag ของ Chemical 1, Chemical 2
- [x] Reset success flag ทุกครั้งก่อนเริ่ม phase ใหม่
- [x] ป้องกัน PLC finish flag เก่าค้างแล้วทำให้ freeze ผิด phase
- [x] Freeze น้ำหนักจาก AutoDA ได้เมื่อถึง target และส่ง stop เข้า PLC queue
- [x] ถ้า PLC finish ไม่มา แต่ weight target reached แล้ว ให้ใช้ fallback พร้อม log warning
- [x] ถ้า PLC stop ส่งไม่สำเร็จ ให้เข้า fault ไม่ใช่ mark complete

### F. งานแก้ Sand Moist Logic

- [x] เช็คว่าน้ำหนักนิ่งจริงก่อนแจ้ง sand moist
- [x] ถ้าน้ำหนักยังเพิ่มอยู่ ห้ามแจ้ง sand moist
- [x] ถ้าน้ำหนักถึง target แล้วแต่ PLC feedback ไม่มา ให้ log เป็น `plc_feedback_timeout`
- [x] แยก log ระหว่าง `sand_moist_suspected` กับ `plc_feedback_timeout`
- [x] ปรับ timeout ไม่ให้ skip sand โดยไม่มีเหตุผลชัดเจน

### G. งานแก้ UI Status

- [x] UI สีเขียวต้องกลับปกติเมื่อ phase completed จริง
- [ ] ถ้า phase เข้า fault ต้องแสดงสถานะ fault ไม่ใช่ค้างสีโหลด
- [x] Log ทุกครั้งที่ UI status เปลี่ยน
- [ ] Log ชื่อวัตถุดิบ, state เดิม, state ใหม่, และเหตุผลที่เปลี่ยน

### H. งานทดสอบหลังแก้

- [ ] ทดสอบ batch ที่มี Sand + Rock1 + Rock2
- [ ] ทดสอบ batch ที่ไม่มี Rock2
- [ ] ทดสอบ batch ที่มี Water/Flyash/Chemical ครบ
- [ ] จำลอง PLC write fail แล้วตรวจว่า command ไม่หาย
- [ ] จำลอง PLC stop fail แล้วตรวจว่าเข้า fault
- [ ] จำลอง AutoDA weight ถึง target แต่ PLC finish ไม่มา
- [ ] ตรวจว่าไม่เกิด false `sand is moist`
- [ ] ตรวจว่า log ระบุ error source ชัดเจน
- [ ] ตรวจว่าไม่มี infinite loop ใน state loading
- [ ] ตรวจว่า UI ไม่ค้างสีเขียวหลัง phase จบ

## ลำดับการแก้ที่แนะนำ

1. แก้ PLC queue ไม่ให้คำสั่งหาย
2. เพิ่ม PLC retry/requeue/fault
3. เพิ่ม log สาเหตุของ `None`
4. เพิ่ม weight target guard
5. แยก success flag รายวัตถุดิบ
6. แก้ sand moist false alarm
7. ปรับ UI status และ log state change
8. ทดสอบกับ log/hardware จริง

## สถานะล่าสุด

- [x] วิเคราะห์ปัญหาจาก log แล้ว
- [x] สร้าง checklist สำหรับตรวจงานแล้ว
- [x] แก้โค้ด PLC queue แล้ว
- [x] เพิ่ม weight target guard แล้ว
- [x] แก้ success flag รายวัตถุดิบแล้ว
- [x] แก้ false sand moist แล้ว
- [ ] ยังไม่ได้ทดสอบหลังแก้กับ hardware จริง

## Verification ที่ทำแล้ว

- [x] `python -m py_compile Controller/PLC_controller.py Controller/main_controller.py`
- [x] `git diff --check` สำหรับไฟล์ที่แก้ไข
- [ ] ยังไม่ได้รันทดสอบกับ PLC/AutoDA จริง
- [ ] ยังไม่ได้จำลอง PLC communication failure ด้วย test harness

## Communication Tuning Applied 2026-06-19

- [x] ปรับ PLC `communication_delay` จาก `20 ms` เป็น `75 ms` เพื่อลดการยิงคำสั่งถี่เกินบน serial line
- [x] ปรับ PLC `read_delay` จาก `200 ms` เป็น `350 ms` และให้ loop อ่าน PLC sleep ตามค่านี้จริง
- [x] ปรับ PLC timeout จาก clamp สูงสุด `1 s` เป็นช่วง `1.5-2.0 s`; config ปัจจุบัน `TIMEOUT_ERROR=3` จึงใช้จริง `2.0 s`
- [x] เพิ่มการ ignore duplicate command ที่เพิ่งเขียนสำเร็จในช่วง `0.75 s`
- [x] ป้องกัน duplicate stop command ไม่ให้รีเซ็ต retry/attempt ของ stop เดิมที่ยังค้างอยู่ในคิว
- [x] ให้ stop command มี priority สูงสุด (`-1`) และตัด pending start ของ coil เดียวกันออกจากคิว
- [x] บล็อก start command ใหม่ถ้ายังมี stop command ของ coil เดียวกันค้างอยู่
- [x] ทำให้ fault จากคำสั่ง stop/write ที่ fail เป็น latched fault ไม่ถูก clear ด้วย read สำเร็จธรรมดา
- [ ] ต้องทดสอบกับ PLC/AutoDA จริงอีกครั้ง และดู log ว่ายังมี `operation_no_response`, `write_queue_retry_scheduled`, `reconnect_begin` ถี่ผิดปกติหรือไม่
