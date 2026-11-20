from collections import defaultdict
from pathlib import Path


def read_attendance_files(directory_path):
  dir_path = Path(directory_path)
  raw_records = []
  damaged_logs = []
  for file_path in sorted(dir_path.glob("*.txt")):
    try:
      with open(file_path, mode="r", encoding="utf-8") as f:
        for line_num, raw_line in enumerate(f, start=1):
          line = raw_line.strip()
          if not line:
            continue
          parts = [p.strip() for p in line.split(",")]
          if len(parts) != 3:
            damaged_logs.append(
                f"{file_path.name}, Line {line_num}: Invalid fields count"
            )
            continue
          reg_no, date_str, status = parts
          if status not in ("P", "A"):
            damaged_logs.append(
                f"{file_path.name}, Line {line_num}: Invalid status '{status}'"
            )
            continue
          raw_records.append((reg_no, date_str, status))
    except Exception as e:
      damaged_logs.append(f"{file_path.name}, Error: {str(e)}")
  return raw_records, damaged_logs


def compute_statistics(raw_records):
  attendance_data = defaultdict(lambda: {"present": 0, "total": 0})
  student_daily_status = defaultdict(list)

  for reg_no, date_str, status in sorted(
      raw_records, key=lambda x: (x[0], x[1])
  ):
    attendance_data[reg_no]["total"] += 1
    if status == "P":
      attendance_data[reg_no]["present"] += 1
    student_daily_status[reg_no].append((date_str, status))

  percentages = {}
  below_75 = []
  for reg_no, counts in attendance_data.items():
    total_days = counts["total"]
    percentage = (counts["present"] / total_days) * 100 if total_days > 0 else 0.0
    percentages[reg_no] = percentage
    if percentage < 75.0:
      below_75.append((reg_no, percentage))

  consecutive_absent = []
  for reg_no, statuses in student_daily_status.items():
    consecutive_count = 0
    is_target = False
    for _, status in statuses:
      if status == "A":
        consecutive_count += 1
        if consecutive_count >= 3:
          is_target = True
      else:
        consecutive_count = 0
    if is_target:
      consecutive_absent.append(reg_no)

  return percentages, below_75, consecutive_absent


def write_reports(percentages, below_75, consecutive_absent, damaged_logs, output_report, output_log, output_consec):
  with open(output_report, mode="w", encoding="utf-8") as rep_file:
    rep_file.write("Register Number,Attendance Percentage\n")
    for reg_no, percentage in percentages.items():
      rep_file.write(f"{reg_no},{percentage:.2f}%\n")
    rep_file.write("\nStudents Below 75% Attendance:\n")
    for reg_no, percentage in below_75:
      rep_file.write(f"{reg_no}: {percentage:.2f}%\n")

  with open(output_consec, mode="w", encoding="utf-8") as consec_file:
    consec_file.write("Students Absent For Three Consecutive Days:\n")
    for reg_no in consecutive_absent:
      consec_file.write(f"{reg_no}\n")

  with open(output_log, mode="w", encoding="utf-8") as log_file:
    log_file.write("Damaged Lines Log\n")
    for log in damaged_logs:
      log_file.write(log + "\n")


if __name__ == "__main__":
  raw, logs = read_attendance_files("./attendance_records")
  pcts, b75, consec = compute_statistics(raw)
  write_reports(
      pcts,
      b75,
      consec,
      logs,
      "attendance_report.txt",
      "damaged_lines.log",
      "consecutive_absent_report.txt",
  )
```[cite: 9, 10]
