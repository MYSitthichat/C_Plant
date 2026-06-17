# ส่งมอบการแก้ไขปัญหา Batch Loading

วันที่ส่งมอบ: 2026-06-17

## ไฟล์ที่แก้ไข

- `Controller/load_work_queue.py`
- `Controller/main_controller.py`

## ปัญหาที่แก้

### 1. ช่อง monitor ว่างตอนเริ่ม Batch

อาการเดิมจาก log:

```text
ERROR - Error reading chemical weight from lineEdit
ERROR - Error reading sand weight
ERROR - Error reading rock 1 weight
```

สาเหตุคือ `clear_mixer_monitors()` reset เฉพาะช่อง `mix_wieght_Loaded_*` แต่ไม่ได้ reset ช่อง `mix_monitor_*` ทำให้ worker thread อ่านค่าว่างแล้วแปลงเป็นตัวเลขไม่ได้

การแก้ไข:

- เพิ่ม reset ช่อง `mix_monitor_*` และช่อง sum monitor ให้เป็น `"0"` ตอนเลือกงาน
- เพิ่ม helper `_read_line_edit_number()` สำหรับอ่านค่า lineEdit แบบปลอดภัย
- จุดเริ่มโหลด rock/sand และ chemical เปลี่ยนมาใช้ helper นี้
- ถ้าค่ายังผิดปกติ log จะบอกชื่อ field และค่า raw ชัดกว่าเดิม

### 2. Cement/Flyash โหลดเสร็จแล้วแต่ main loop ยังเห็น `C&F=False`

อาการเดิมจาก log `log_Batch_2026-06-15_07-59-31.txt`:

```text
cement and fyash loading success
State 0 waiting - Flags: R&S=True, C&F=False, W=True, Chem=True
```

สาเหตุคือ thread ปูน/เถ้าลอยตั้ง `cement_and_fyash_loading_success=True` แล้ว แต่ main loop จะเปลี่ยน `cement_and_fyash_success_start_main=True` เฉพาะตอนมี PLC status signal รอบถัดไป

การแก้ไข:

- เพิ่ม signal `cement_fyash_completed`
- เมื่อ state ปูน/เถ้าลอยจบ จะ emit signal นี้ทันที
- เพิ่ม `_finish_cement_and_fyash_success()` เพื่อ set flag สำเร็จและเรียก `_check_all_materials_loaded()`
- ทำให้ handler เป็น idempotent เรียกซ้ำแล้วไม่ set ซ้ำ
- เพิ่ม guard ไม่ให้ worker thread join ตัวเอง

### 3. Setpoint Cement/Flyash ถูก bypass ด้วยเงื่อนไขจริงเสมอ

อาการเดิมในโค้ด:

```python
if fyash_setpoint == fyash_setpoint:
if cement_setpoint == cement_setpoint:
```

การแก้ไข:

- เพิ่ม `_write_and_confirm_cement_fyash_setpoint()`
- ก่อนเริ่มโหลด Flyash/Cement จะ write setpoint แล้ว read feedback กลับจาก AutoDA
- ถ้า feedback ไม่ตรงหรือ AutoDA ตอบ `0` จาก read failure จะไม่สั่งโหลดต่อ
- ระบบจะ stop output ที่เกี่ยวข้องและ retry state เดิม
- state 3 ของ Cement ถูกปรับให้ confirm setpoint ก่อนเริ่มโหลดจริงด้วย

### 4. การอ่านน้ำหนักปูนใน state ตรวจสอบ

การแก้ไข:

- state 100, 101, 102 เปลี่ยนการอ่าน `mix_monitor_cement_lineEdit` มาใช้ safe read
- ถ้าอ่านไม่ได้ จะ stop cement และ retry check แทนการตั้งน้ำหนักเป็น `0` แล้วจบงานผิดพลาด
- ถ้า state 102 อ่านได้ `0` จะ retry แทนการถือว่าโหลดจบ

### 5. Log เติมปูนอ่านกลับด้าน

อาการเดิม:

```text
filling cement -14 KG ::: round 1
```

การแก้ไข:

- เพิ่ม `remaining_cement = target - tried_weight`
- log ใหม่จะแยก `remaining` และ `diff` ชัดเจน

ตัวอย่าง:

```text
filling cement remaining 14 KG (diff -14 KG) ::: round 1
```

## จุดที่ตั้งใจไม่แก้ตามคำสั่ง

state 103 ยังคงเติมปูนแบบ fixed pulse เวลา `0.5` วินาทีเหมือนเดิม:

```python
self.plc_controller.loading_cement("start")
time.sleep(0.5)
self.plc_controller.loading_cement("stop")
```

เหตุผล: ผู้ทดสอบยืนยันกับ hardware จริงแล้วว่าเวลา 0.5 วินาทีแม่นที่สุด

## เพิ่ม Logging ครอบคลุมเพิ่มเติม

เพิ่ม log รูปแบบ `[TRACE]` เพื่อช่วยไล่เหตุการณ์จาก log batch ได้ละเอียดขึ้น โดยเน้นจุดที่เคยตามยาก:

- `plc_command` และ `plc_command_result`: log ทุกคำสั่ง start/stop สำคัญที่ส่งไป PLC เช่น sand, rock, cement, flyash, water, chemical, conveyor, mixer, valve และ pump
- `autoda_command` และ `autoda_command_result`: log การ write/read setpoint ของ AutoDA ทุกกลุ่ม material
- `autoda_feedback`: log ค่า feedback setpoint ที่ callback กลับมา
- `plc_status`: log status signal จาก PLC สำหรับ rock/sand, cement/flyash, water และ chemical
- `flags_snapshot`: log flag สำเร็จของ material ทั้ง 4 กลุ่ม และ `next_queue_loaded_and_ready`
- `sequence_start`: log ตอนเริ่ม loading sequence ของ rock/sand, cement/flyash, water และ chemical
- `queue_targets_prepared`: log target ที่เตรียมส่งให้แต่ละ loading thread
- `thread_started`: log ตอนเริ่ม thread ของแต่ละ material และ main condition thread
- `initial_weight`: log initial weight ที่อ่านได้จาก monitor ก่อนคำนวณ setpoint
- `setpoint_calculated`: log setpoint หลังหัก offset และบวกน้ำหนักค้าง
- `weight_frozen`: log น้ำหนักที่ถูก freeze หลัง PLC แจ้งโหลดเสร็จและรอ stabilize แล้ว
- `sequence_complete`: log ตอน material แต่ละกลุ่มจบ sequence รวมถึงกรณี skipped เพราะ target เป็น 0
- `batch_weights_accumulated`: log น้ำหนักที่ถูกสะสมเข้ายอดรวมของ batch
- `database_update_attempt`: log ข้อมูลก่อน/หลังบันทึก database พร้อมผล success
- `mixer_monitors_reset`: log ตอน reset monitor/loaded fields เป็น 0 ตอนเลือกงาน

ตัวอย่าง log ที่คาดว่าจะเห็น:

```text
[TRACE] queue_targets_prepared | queue=1, rock_sand=[350, 950, 700, 1.0], cement_fyash=[228, 45], water=160, chemical=[1.3, 0.4]
[TRACE] autoda_command | command='write_set_point_cement_and_fyash', args=(273,), kwargs={}
[TRACE] autoda_feedback | target='cement_fyash', value=273
[TRACE] weight_frozen | material='cement', total=233, state=4
[TRACE] flags_snapshot | reason='cement_fyash_completed', rock_sand=True, cement_fyash=True, water=True, chemical=True, next_ready=False
```

## รอบแก้ไขเพิ่มเติม: ปิดความเสี่ยงร้ายแรงที่ยังเหลือ

### 1. Setpoint feedback bypass ใน Rock/Sand, Water, Chemical

แก้ pattern เดิมที่เคยใช้เงื่อนไขจริงเสมอ เช่น:

```python
if sand == sand:
if rock_1 == rock_1:
if rock_2 == rock_2:
if water == water:
if chem1 == chem1:
if chem2 == chem2:
```

การแก้ไข:

- เพิ่ม helper กลาง `_write_and_confirm_setpoint()`
- เพิ่ม wrapper เฉพาะกลุ่มวัสดุ:
  - `_write_and_confirm_rock_sand_setpoint()`
  - `_write_and_confirm_water_setpoint()`
  - `_write_and_confirm_chemical_setpoint()`
  - `_write_and_confirm_cement_fyash_setpoint()`
- ก่อนสั่ง PLC เริ่มโหลด Sand, Rock1, Rock2, Water, Chemical 1, Chemical 2 จะต้อง write setpoint สำเร็จและอ่าน feedback จาก AutoDA กลับมาตรงกับ target ก่อน
- ถ้า feedback ไม่ตรงหรืออ่านไม่ได้ จะไม่เริ่มโหลด และจะ retry state เดิมพร้อม log error

### 2. AutoDA setpoint read failure ไม่ส่ง 0 แล้ว

เดิมถ้าอ่าน feedback setpoint ไม่ได้ AutoDA จะ emit `0` หรือ `0.0` ทำให้ระบบแยกไม่ออกระหว่าง "ค่า 0 จริง" กับ "อ่านไม่ได้"

การแก้ไข:

- เปลี่ยน signal setpoint feedback ใน `Autoda_controller.py` เป็น `Signal(object)`
- เมื่ออ่าน setpoint ไม่ได้ เปลี่ยนเป็น emit `None`
- helper confirm จะถือว่า `None` คือ read failure และไม่อนุญาตให้เริ่มโหลดวัสดุ

### 3. Completion signal ครบทุก material group

เดิมแก้ completion signal เฉพาะ Cement/Flyash แล้ว แต่ Rock/Sand, Water, Chemical ยังมีโอกาสต้องรอ PLC status callback รอบถัดไป

การแก้ไข:

- เพิ่ม signal:
  - `rock_sand_completed`
  - `water_completed`
  - `chemical_completed`
- เพิ่ม handler:
  - `_finish_rock_and_sand_success()`
  - `_finish_water_success()`
  - `_finish_chemical_success()`
- เมื่อ sequence โหลดเสร็จหรือถูก skip เพราะ target เป็น 0 จะ emit completion ทันที
- handler ทุกตัวเป็น idempotent เพื่อกัน set flag ซ้ำ

### 4. ป้องกัน thread join ตัวเอง

เพิ่ม guard ให้ `loaded_rock_and_sand_successfully()`, `loaded_water_successfully()`, และ `loaded_chemical_successfully()` ไม่ join thread ตัวเอง เหมือนที่ทำไว้กับ Cement/Flyash แล้ว

### 5. แก้จุดค้างเมื่อไม่มี Rock2

ใน state 4 ของ Rock/Sand ถ้า Rock1 เสร็จแล้วและสูตรไม่มี Rock2 เดิมมีโอกาสแค่ log แล้วไม่ finalize sequence

การแก้ไข:

- ตั้ง `is_rock2_frozen=True`
- set success flag
- emit `rock_sand_completed`
- log `sequence_complete` พร้อม `skipped_rock2=True`

## การตรวจสอบที่ทำแล้ว

รัน syntax check:

```powershell
python -m py_compile .\New_Contol_plant\Controller\main_controller.py .\New_Contol_plant\Controller\load_work_queue.py
```

ผลลัพธ์: ผ่าน ไม่มี syntax error

รัน diff check:

```powershell
git diff --check -- .\New_Contol_plant\Controller\main_controller.py .\New_Contol_plant\Controller\load_work_queue.py
```

ผลลัพธ์: ไม่มี whitespace error มีเฉพาะ warning เรื่อง LF/CRLF ของ working copy

## Checklist ทดสอบกับเครื่องจริง

1. เลือกงานใหม่แล้วเช็กว่า `mix_monitor_*` ทุกช่องเริ่มที่ `0`
2. เริ่ม batch แล้ว log ต้องไม่มี `Error reading chemical/sand/rock 1 weight from lineEdit`
3. เมื่อ log มี `cement and fyash loading success` ต้องตามด้วย `Cement and Flyash loaded successfully.`
4. หลัง C&F สำเร็จ main loop ต้องเห็น `C&F=True`
5. ถ้า AutoDA อ่าน setpoint ไม่ได้ ต้องเห็น log `setpoint confirm failed` และเครื่องต้องไม่เริ่มโหลดวัสดุนั้น
6. ตอนเติมปูนเพิ่ม log ต้องเป็น `remaining ... KG` ไม่ใช่ค่าติดลบแบบเดิม
7. ยืนยันว่า state 103 ยัง pulse ปูน 0.5 วินาที

## ตรวจสอบล่าสุดหลังแก้รอบ Critical

รัน syntax check:

```powershell
python -m py_compile .\New_Contol_plant\Controller\main_controller.py .\New_Contol_plant\Controller\Autoda_controller.py .\New_Contol_plant\Controller\load_work_queue.py
```

ผลลัพธ์: ผ่าน ไม่มี syntax error

รัน diff check:

```powershell
git diff --check -- .\New_Contol_plant\Controller\main_controller.py .\New_Contol_plant\Controller\Autoda_controller.py .\New_Contol_plant\Controller\load_work_queue.py .\New_Contol_plant\BATCH_LOG_FIX_DELIVERY.md
```

ผลลัพธ์: ไม่มี whitespace error มีเฉพาะ warning LF/CRLF ของ working copy
