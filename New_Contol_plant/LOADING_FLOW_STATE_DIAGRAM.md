# Loading Flow State Diagram

วันที่จัดทำ: 2026-06-17

เอกสารนี้สรุป step การทำงานหลังการแก้ไขล่าสุด โดยเน้น flow ตั้งแต่เริ่มโหลดวัตถุดิบจนโหลดเสร็จ, ลำเลียงเข้าโม่, ผสม, ปล่อยออก และกรณีผิดปกติที่ยังอาจเกิดขึ้นได้

> หมายเหตุ: diagram ใช้ Mermaid เปิดดูได้ใน Markdown viewer ที่รองรับ Mermaid

## ภาพรวมระบบหลังแก้ไข

```mermaid
flowchart TD
    A[กดเริ่มโหลด / mix_start_load] --> B[อ่านสูตรและ offset]
    B --> C[คำนวณ target ตาม queue multiplier]
    C --> D[reset flag และ monitor]
    D --> E[เริ่ม thread โหลด 4 กลุ่มพร้อมกัน]

    E --> RS[Rock/Sand sequence]
    E --> CF[Cement/Flyash sequence]
    E --> W[Water sequence]
    E --> CH[Chemical sequence]

    RS --> RSDone[rock_sand_completed]
    CF --> CFDone[cement_fyash_completed]
    W --> WDone[water_completed]
    CH --> CHDone[chemical_completed]

    RSDone --> All{ครบ 4 flag?}
    CFDone --> All
    WDone --> All
    CHDone --> All

    All -- ยังไม่ครบ --> Wait[main state 0 รอ]
    Wait --> All
    All -- ครบ --> Ready[next_queue_loaded_and_ready=True]
    Ready --> Main[main_condition_load ลำเลียง/ผสม]
```

สิ่งที่เปลี่ยนจากเดิม:

- เดิมบางกลุ่มใช้ `if x == x` ทำให้ write setpoint แล้วเริ่มโหลดเลยโดยไม่สน feedback
- ตอนนี้ทุกกลุ่มต้อง `write setpoint -> read feedback -> feedback ตรง target` ก่อนสั่ง PLC start
- เดิม C&F เคยโหลดเสร็จแล้ว flag ไม่เปลี่ยนถ้าไม่มี PLC status callback รอบถัดไป
- ตอนนี้ทุกกลุ่มมี completion signal ของตัวเองแล้ว

## Helper Confirm Setpoint กลาง

ทุก material group ใช้แนวคิดเดียวกันก่อนเริ่มโหลดจริง

```mermaid
flowchart TD
    A[ต้องการ setpoint ใหม่] --> B[write setpoint ไป AutoDA]
    B --> C{write สำเร็จ?}
    C -- ไม่สำเร็จ --> R1[log error / sleep / retry attempt]
    R1 --> B
    C -- สำเร็จ --> D[read setpoint feedback]
    D --> E{feedback มาไหม?}
    E -- None / ไม่มา --> R2[confirm failed / retry attempt]
    R2 --> B
    E -- มา --> F{feedback ตรง expected?}
    F -- ไม่ตรง --> R3[confirm failed / retry state เดิม]
    R3 --> B
    F -- ตรง --> G[อนุญาตให้ PLC start loading]
```

ผลของการแก้:

- AutoDA read setpoint failure จะ emit `None` แทน `0`
- ถ้า feedback เป็น `0` แต่ target ไม่ใช่ `0` จะไม่ผ่าน confirm
- ถ้า material target เป็น 0 ระบบจะใช้ branch skip แทนการโหลด

## Main Condition State

หลังวัตถุดิบครบ 4 กลุ่มแล้ว main loop จะลำเลียง/ผสมตาม state นี้

```mermaid
stateDiagram-v2
    [*] --> S0
    S0: state 0\nรอ next_queue_loaded_and_ready
    S0 --> S1: โหลดครบ 4 กลุ่ม

    S1: state 1\nupdate sum, เปิด mixer,\nเปิดสายพานบน/ล่าง
    S1 --> S2

    S2: state 2\nเปิด pump chemical up,\nเปิด valve water,\nรอ cement_release_time,\nเปิด valve cement/flyash
    S2 --> S3

    S3: state 3\nติดตามน้ำหนัก Rock/Sand\nรอน้ำหนักต่ำกว่า threshold ครบ 3 ครั้ง\nหน่วง converyer_time แล้วปิด conveyor/water/pump
    S3 --> S4

    S4: state 4\nรอ mixer_start_time\nเปิดปากโม่ 3 step\nปิด pump chemical
    S4 --> S5

    S5: state 5\nรอ 15 วินาที\nเช็คคิวถัดไป
    S5 --> S8: ไม่มีคิวเหลือ
    S5 --> S7: ยังมีคิว

    S7: state 7\nสะสมจำนวนคิวที่เสร็จ\nถ้าคิวถัดไปพร้อม ปิดปากโม่แล้วกลับ S0\nถ้ายังไม่พร้อม ไป S6
    S7 --> S0: next_queue_loaded_and_ready=True
    S7 --> S6: ยังมีคิวแต่ยังโหลดไม่เสร็จ

    S6: state 6\nรอคิวถัดไปโหลดครบ\nถ้ายังไม่พร้อม ปิดปากโม่รอ
    S6 --> S0: คิวถัดไปพร้อม

    S8: state 8\nจบงานทั้งหมด\nupdate database, stop log,\nreset UI/device
    S8 --> [*]
```

## Rock/Sand Normal Flow

ลำดับโหลดคือ Sand -> Rock1 -> Rock2

```mermaid
stateDiagram-v2
    [*] --> R1
    R1: state 1\nคำนวณ/confirm Sand setpoint
    R1 --> R2: Sand target > 0 และ confirm ผ่าน\nPLC loading_sand start + vibrator start
    R1 --> R3: Sand target <= 0\nskip Sand
    R1 --> R1: confirm ไม่ผ่าน\nretry state 1

    R2: state 2\nรอ Sand frozen จาก PLC status + stabilize
    R2 --> R3: Sand frozen\nstop sand/vibrator\nconfirm Rock1 setpoint
    R2 --> R2: Sand ชื้น timeout\nเตือน, นับ retry\nครบ 3 ครั้ง freeze sand current แล้วไปต่อ

    R3: state 3\nเริ่ม Rock1
    R3 --> R4: Rock1 target > 0 และ confirm ผ่าน\nPLC loading_rock1 start
    R3 --> R5: Rock1 target <= 0\nskip Rock1 / confirm Rock2
    R3 --> R3: confirm ไม่ผ่าน\nretry state 3

    R4: state 4\nรอ Rock1 frozen
    R4 --> R5: Rock1 frozen\nconfirm Rock2 setpoint
    R4 --> Done: Rock2 target <= 0\nskip Rock2 และ complete
    R4 --> R4: Rock2 confirm ไม่ผ่าน\nretry state 4

    R5: state 5\nเริ่ม Rock2
    R5 --> R6: Rock2 target > 0\nPLC loading_rock2 start
    R5 --> Done: Rock2 target <= 0\nskip Rock2

    R6: state 6\nรอ Rock2 frozen
    R6 --> Done: stop rock2/rock1/sand\nemit rock_sand_completed

    Done: complete\nset rock_and_sand_success_start_main=True
    Done --> [*]
```

กรณีพิเศษ:

- ถ้า queue multiplier < 1.0 จะมีการปรับ setpoint Rock1/Rock2 ตามน้ำหนักจริงที่โหลดได้ แล้ว confirm setpoint ที่ปรับแล้วก่อนโหลด
- ถ้าไม่มี Rock2 หลัง Rock1 เสร็จ ตอนนี้ complete ได้ทันที ไม่ค้างที่ state 4 แล้ว

## Cement/Flyash Normal Flow รวมการเติมปูน

ลำดับโหลดคือ Flyash -> Cement และ Cement มี state ตรวจ/เติมละเอียด

```mermaid
stateDiagram-v2
    [*] --> C1
    C1: state 1\nconfirm Flyash setpoint
    C1 --> C2: Flyash target > 0 และ confirm ผ่าน\nPLC loading_flyash start
    C1 --> C3: Flyash target <= 0\nskip Flyash
    C1 --> C1: confirm ไม่ผ่าน\nretry state 1

    C2: state 2\nรอ Flyash frozen
    C2 --> C3: stop flyash\nconfirm Cement setpoint
    C2 --> C2: Cement confirm ไม่ผ่าน\nretry state 2

    C3: state 3\nconfirm Cement setpoint อีกครั้งก่อนโหลดจริง
    C3 --> C100: Cement target > 0 และ confirm ผ่าน\nPLC loading_cement start
    C3 --> Done: Cement target <= 0\nskip Cement
    C3 --> C3: confirm ไม่ผ่าน\nstop cement / retry

    C100: state 100\nโหลดปูนรอบแรกจนถึง target - 15kg
    C100 --> C101: ถึง cutoff\nstop cement / รอ settle / อ่านน้ำหนัก
    C100 --> C102: อ่านน้ำหนักไม่ได้\nstop cement / retry check

    C101: state 101\nคำนวณ rate_loaded จากรอบแรก\nคำนวณ remain และ extra_time
    C101 --> C102: คำนวณไม่ได้ หรือเติมรอบแรกแล้ว\nเช็คละเอียด
    C101 --> C102: remain > 0\nเติมรอบช่วย 0.8s แล้วเช็คละเอียด

    C102: state 102\nอ่านน้ำหนักล่าสุดและเทียบ target
    C102 --> C4: abs(diff) <= 3kg\nถือว่าตรงเป้า
    C102 --> C4: น้ำหนักเกิน target + 1kg\nหยุดและจบแบบ over target warning
    C102 --> C103: น้ำหนักยังขาด\nretry_count <= 10
    C102 --> C102: อ่านไม่ได้ หรืออ่านได้ 0\nretry ไม่จบงาน
    C102 --> C4: เติมเกิน 10 รอบ\ncritical warning แล้วจบแบบ forced

    C103: state 103\nเติมปูนทีละ 0.5 วินาที fixed pulse
    C103 --> C102: กลับไปอ่านน้ำหนักใหม่

    C4: state 4\nstop cement\nemit cement_fyash_completed
    C4 --> Done

    Done: complete\nset cement_fyash_success_start_main=True
    Done --> [*]
```

จุดสำคัญ:

- state 103 ยังเป็น fixed pulse `0.5` วินาทีตามที่ทดสอบกับ hardware จริงแล้ว
- state 102 ถ้าอ่านน้ำหนักปูนได้ `0` จะไม่ถือว่าเสร็จ แต่ retry ต่อ
- ถ้าอ่านน้ำหนักไม่ได้จะ stop cement แล้ว retry check

## Water Normal Flow

```mermaid
stateDiagram-v2
    [*] --> W1
    W1: state 1\nconfirm Water setpoint
    W1 --> W2: Water target > 0 และ confirm ผ่าน\nPLC loading_water start
    W1 --> Done: Water target <= 0\nskip Water
    W1 --> W1: confirm ไม่ผ่าน\nstop water / retry state 1

    W2: state 2\nรอ Water frozen จาก PLC status + stabilize
    W2 --> W3: frozen แล้ว stop water

    W3: state 3\nset success\nemit water_completed
    W3 --> Done

    Done: complete\nset water_success_start_main=True
    Done --> [*]
```

## Chemical Normal Flow

ลำดับโหลดคือ Chemical 1 -> Chemical 2

```mermaid
stateDiagram-v2
    [*] --> K1
    K1: state 1\nconfirm Chemical 1 setpoint
    K1 --> K2: Chem1 target > 0 และ confirm ผ่าน\nPLC loading_chemical_1 start
    K1 --> K3: Chem1 target <= 0\nskip Chem1
    K1 --> K1: confirm ไม่ผ่าน\nstop chem1 / retry state 1

    K2: state 2\nรอ Chem1 frozen
    K2 --> K3: stop chem1\nconfirm Chemical 2 setpoint
    K2 --> K2: Chem2 confirm ไม่ผ่าน\nretry state 2

    K3: state 3\nเริ่ม Chemical 2 หรือ complete ถ้าไม่มี Chem2
    K3 --> K4: Chem2 target > 0\nPLC loading_chemical_2 start
    K3 --> Done: Chem2 target <= 0\nskip Chem2

    K4: state 4\nรอ Chem2 frozen
    K4 --> Done: stop chem2/chem1\nemit chemical_completed

    Done: complete\nset chemical_success_start_main=True
    Done --> [*]
```

## Abnormal Flow: Setpoint เขียน/อ่านไม่ได้

```mermaid
flowchart TD
    A[ต้องเริ่มโหลด material] --> B[write setpoint]
    B --> C{write ok?}
    C -- no --> D[log: setpoint write failed]
    D --> E[ไม่สั่ง PLC start]
    E --> F[retry state เดิม]

    C -- yes --> G[read feedback]
    G --> H{feedback}
    H -- None --> I[log: setpoint confirm failed]
    I --> E
    H -- 0 แต่ target > 0 --> J[feedback ไม่ตรง expected]
    J --> E
    H -- ค่าอื่นไม่ตรง target --> K[confirm failed]
    K --> E
    H -- ตรง target --> L[PLC start loading]
```

ต่างจากเดิม:

- เดิม write แล้วผ่าน `if x == x` จึงเริ่มโหลดได้แม้ AutoDA ไม่ตอบกลับ
- ตอนนี้ถ้า AutoDA อ่าน setpoint ไม่ได้ จะเป็น `None` และไม่เริ่มโหลด

## Abnormal Flow: AutoDA ส่งค่า 0

แบ่งเป็น 2 ประเภท:

```mermaid
flowchart TD
    A[AutoDA ส่ง 0] --> B{เป็น setpoint feedback หรือ weight feedback?}

    B -- setpoint feedback --> C{target expected เป็น 0 ไหม?}
    C -- target > 0 --> D[confirm ไม่ผ่าน\nไม่เริ่มโหลด]
    C -- target = 0 --> E[ปกติจะเข้า branch skip target <= 0\nไม่ต้องโหลด]

    B -- weight feedback --> F[ค่า 0 เข้า display/monitor ได้]
    F --> G{อยู่จุดไหน?}
    G -- Cement state 102 --> H[ไม่จบงาน\nlog warning แล้ว retry]
    G -- Initial weight ของบาง material --> I[อาจถูกมองเป็นน้ำหนักค้าง 0\nต้องดู log และทดสอบจริง]
```

สถานะปัจจุบัน:

- setpoint feedback failure แก้แล้ว ไม่ใช้ `0` แทน failure
- weight feedback บาง path ใน `Autoda_controller.py` ยัง emit `0` เมื่ออ่านน้ำหนักไม่ได้ จึงยังเป็นจุดที่ควร monitor ตอนทดสอบจริง

## Abnormal Flow: PLC Status ไม่มา

```mermaid
flowchart TD
    A[PLC start loading แล้ว] --> B[รอ PLC status True เพื่อ freeze น้ำหนัก]
    B --> C{status มาไหม?}
    C -- มา --> D[รอ stabilize_delay]
    D --> E[freeze weight]
    E --> F[sequence ไป state ถัดไปหรือ complete]

    C -- ไม่มา --> G[freeze flag ไม่ถูก set]
    G --> H[sequence รออยู่ใน state loading]
    H --> I[log จะเห็น state เดิมวน / ไม่มี weight_frozen]
```

หมายเหตุ:

- completion signal ช่วยแก้กรณี sequence จบแล้วแต่ main flag ไม่เปลี่ยน
- แต่การจะ freeze น้ำหนักของหลายวัสดุยังพึ่ง PLC status อยู่ ถ้า PLC status ไม่มาเลย sequence อาจรออยู่ใน state นั้น

## Abnormal Flow: Cement น้ำหนักอ่านไม่ได้หรือเติมไม่ถึง

```mermaid
flowchart TD
    A[Cement state 100/101/102] --> B{อ่านน้ำหนัก cement ได้ไหม?}
    B -- ไม่ได้ --> C[stop cement]
    C --> D[ไป/อยู่ state 102 เพื่อ retry]

    B -- ได้ 0 ใน state 102 --> E[warning: Cement weight is 0]
    E --> D

    B -- ได้ค่า valid --> F{diff กับ target}
    F -- abs(diff)<=3 --> G[จบปกติ]
    F -- เกิน target+1 --> H[จบพร้อม warning over target]
    F -- ยังขาด --> I{retry_count > 10?}
    I -- no --> J[state 103 เติม 0.5s]
    J --> D
    I -- yes --> K[critical warning\nforced finish]
```

## จุดที่ต่างจากระบบเดิมมากน้อยแค่ไหน

| หัวข้อ | เดิม | หลังแก้ |
|---|---|---|
| Setpoint confirm | บางกลุ่ม bypass ด้วย `if x == x` | ทุกกลุ่มต้อง feedback ตรงก่อน PLC start |
| AutoDA read setpoint fail | emit `0`/`0.0` | emit `None` และ confirm fail |
| C&F completion | รอ PLC status callback รอบถัดไป | emit `cement_fyash_completed` เมื่อ sequence จบ |
| Rock/Sand, Water, Chemical completion | ยังเสี่ยงรอ callback เหมือนเดิม | มี completion signal ครบทุกกลุ่ม |
| Cement state 102 อ่าน 0 | เดิมเสี่ยงตีความผิดเป็นจบ | ไม่จบงาน, retry ต่อ |
| Rock/Sand ไม่มี Rock2 | เดิมมีโอกาสค้างหลัง Rock1 | complete พร้อม `skipped_rock2=True` |
| Logging | กระจายและจับ flow ยาก | มี `[TRACE]` ครอบคลุม command, feedback, freeze, flags, complete |
| State 103 เติมปูน | fixed 0.5s | คงเดิมตามผลทดสอบ hardware |

## Log ที่ควรเห็นในรอบปกติ

```text
[TRACE] queue_targets_prepared
[TRACE] thread_started | thread='rock_sand'
[TRACE] thread_started | thread='cement_fyash'
[TRACE] thread_started | thread='water'
[TRACE] thread_started | thread='chemical'
[TRACE] setpoint_calculated
[TRACE] autoda_command | command='write_set_point_...'
[TRACE] autoda_feedback | target='...'
[TRACE] plc_command | command='loading_...'
[TRACE] weight_frozen
[TRACE] sequence_complete
[TRACE] flags_snapshot | reason='..._completed'
Queue ... fully loaded - Setting next_queue_loaded_and_ready=True
```

## Log ที่ควรเฝ้าระวัง

```text
setpoint write failed
setpoint confirm failed
feedback None
Cement weight is 0 in state 102; retrying instead of completing.
Critical Error: เติมปูนหลายรอบแล้วน้ำหนักไม่ถึงเป้า
State 0 waiting - Flags: R&S=..., C&F=..., W=..., Chem=...
ไม่มี weight_frozen หลัง PLC start เป็นเวลานาน
```

## Checklist ทดสอบกับเครื่องจริง

1. Batch ปกติ 1 คิว: ต้องเห็นครบ `rock_sand_completed`, `cement_fyash_completed`, `water_completed`, `chemical_completed`
2. สูตรที่มี Cement ขาดเล็กน้อย: ต้องเข้า state 102 -> 103 -> 102 จน diff อยู่ในเกณฑ์
3. สูตรไม่มี Rock2: Rock/Sand ต้อง complete ไม่ค้าง state 4
4. สูตรมี material เป็น 0: ต้อง skip และ emit completed ได้
5. ปิด/หลุด AutoDA ชั่วคราวตอน read setpoint: ต้องไม่เริ่ม PLC loading ของ material นั้น
6. ทำให้ feedback setpoint เป็น 0 แต่ target > 0: ต้อง confirm fail และ retry
7. เช็ค log ว่าไม่มี `if x == x` behavior แบบเดิม คือไม่มีการ PLC start หลัง confirm fail
8. เช็คว่าถ้า PLC status ไม่มา จะเห็น state loading ค้างและไม่มี `weight_frozen` เพื่อใช้วินิจฉัย PLC/status line
