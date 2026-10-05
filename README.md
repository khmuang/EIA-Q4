# EIA Q4 Performance Dashboard 2026

## 📌 ภาพรวมโครงการ (Project Overview)
ระบบประมวลผลและติดตามผลการตรวจสอบ Endpoint Internal Audit (EIA) ประจำไตรมาสที่ 4 (Q4) ปี 2026 เชื่อมโยงข้อมูลโดยตรงกับ Microsoft OneDrive ของทีมงาน RIS Endpoint Support

* **OneDrive Data Source:** `D:\Users\Djmanny\OneDrive - Central Group\RIS Endpoint support - 2026\Q4`
* **Baseline Master File:** `EIA Document Q4.xlsx` (Sheet: `EIA topic Q3` / Scope Targets)
* **Local Dashboard Path:** `d:\Users\Djmanny\.gemini\tmp\project\EIA_Q4\`

---

## 🎯 ขอบเขตเป้าหมาย EIA Q4 Baseline (Scope Targets)

| หัวข้อ (Topic ID) | รายละเอียด (Description) | จำนวนเป้าหมาย (Total) | ความสำคัญ (Priority) | การดำเนินการ (Action) |
| :---: | :--- | :---: | :---: | :--- |
| **1.1** | Missing BU, Company, Location information | **152** | Low | กรอกข้อมูลในระบบ GLPI ให้สมบูรณ์ |
| **1.2** | Not installed GLPI Agent | **50** | Low | ติดตั้ง GLPI Agent x64/x86 |
| **2.1** | W11 OS version not current *(Heavy-Hitter)* | **3,152** | Medium | อัปเดต OS เป็นเวอร์ชันปัจจุบัน |
| **3.1** | Device require patch security updates | **327** | Medium | อัปเดต Patch ความปลอดภัย |
| **4.1** | Antivirus software not installed / not standard | **95** | High | ติดตั้ง Antivirus ตามมาตรฐาน |
| **5.1** | Built-in firewall not enabled / misconfigured | **567** | Medium | เปิดใช้งานและตั้งค่า Firewall |
| **6.1** | Device not joined to domain | **23** | High | นำเครื่อง Join เข้า Domain |
| **7.1** | Privileged User (Admin Rights) *(Heavy-Hitter)* | **711** | High | ปลดสิทธิ์ Admin สำหรับผู้ใช้ทั่วไป |
| **8.1** | Document Request evidence | **15** | Medium | แนบเอกสารหลักฐานขออนุมัติ |
| **รวม** | **เป้าหมายรวมทั้งหมด (Grand Total Scope)** | **5,092** | - | - |

> 🚨 **Heavy-Hitters Focus:** หัวข้อ 2.1 (OS Update: 3,152 เครื่อง) และ 7.1 (Privileged User: 711 เครื่อง) คิดเป็นกว่า **75.9%** ของเป้าหมายทั้งหมดในไตรมาสนี้

---

## 📏 กฎและมาตรฐานการคำนวณ (Calculation Standards & Domain Invariants)

1. **เกณฑ์สี 4 ระดับ (4-Tier Color Scheme):**
   * 🟢 **Excellent:** $\ge 85\%$ (`#10b981`, Emerald)
   * 🔵 **Good:** $65\% - 84\%$ (`#3b82f6`, Blue)
   * 🟡 **Warning:** $45\% - 64\%$ (`#f59e0b`, Amber)
   * 🔴 **Critical:** $< 45\%$ (`#f43f5e`, Rose)
2. **เกณฑ์การผ่าน (PASS Threshold):**
   * คอมโพเนนต์และหัวข้อจะได้รับสถานะ **`PASS`** เมื่อค่าความสำเร็จ (Compliance) $\ge 85\%$ เท่านั้น
3. **นิยามการคำนวณคะแนน:**
   * **Compliance Score (Top-Left KPI):** คำนวณแบบ **Unweighted Average** (เฉลี่ยตามหมวดหมู่ $9$ หัวข้อ) สะท้อนคุณภาพภาพรวม
   * **Overall Progress / Podium Score:** คำนวณแบบ **Weighted Average** ($\frac{\sum \text{Success}}{\sum \text{Total}}$) สะท้อนปริมาณงานจริงรายเครื่อง

---

## 🚀 วิธีการใช้งานและการประมวลผล (Operational Runbook)

### 1. การซิงค์และอัปเดตข้อมูลอัตโนมัติ
ดับเบิลคลิกไฟล์ [run_sync.bat](file:///d:/Users/Djmanny/.gemini/tmp/project/EIA_Q4/run_sync.bat) หรือรันผ่าน Terminal:
```powershell
python update_dashboard.py
python gen_tables.py
```
* **ขั้นตอนที่ 1 (`update_dashboard.py`):** ตรวจสอบไฟล์ใน OneDrive Q4 หากมีไฟล์ดิบรายหัวข้อ จะประมวลผลข้อมูลรายเครื่องและ BU Matrix หากยังไม่มี จะดึง Baseline Scope จาก `EIA Document Q4.xlsx` มาตั้งต้นให้โดยอัตโนมัติ
* **ขั้นตอนที่ 2 (`gen_tables.py`):** ประมวลผลและสร้างตารางสถิติสรุปเจาะลึก (Deep Dive Table) และ BU Breakdown Matrix ฉีดเข้าสู่ `index.html`

### 2. การเปิดดู Dashboard
เปิดไฟล์ [index.html](file:///d:/Users/Djmanny/.gemini/tmp/project/EIA_Q4/index.html) ผ่าน Web Browser
