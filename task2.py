from collections import defaultdict
from pathlib import Path


def process_attendance_files(directory_path, output_report, output_log):
  dir_path = Path(directory_path)
  attendance_data = defaultdict(lambda: {"present": 0, "total": 0})
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

          attendance_data[reg_no]["total"] += 1
          if status == "P":
            attendance_data[reg_no]["present"] += 1

    except Exception as e:
      damaged_logs.append(f"{file_path.name}, Error: {str(e)}")

  below_75 = []

  with open(output_report, mode="w", encoding="utf-8") as rep_file:
    rep_file.write("Register Number,Attendance Percentage\n")
    for reg_no, counts in attendance_data.items():
      total_days = counts["total"]
      if total_days > 0:
        percentage = (counts["present"] / total_days) * 100
      else:
        percentage = 0.0

      rep_file.write(f"{reg_no},{percentage:.2f}%\n")
      if percentage < 75.0:
        below_75.append((reg_no, percentage))

    rep_file.write("\nStudents Below 75% Attendance:\n")
    for reg_no, percentage in below_75:
      rep_file.write(f"{reg_no}: {percentage:.2f}%\n")

  with open(output_log, mode="w", encoding="utf-8") as log_file:
    log_file.write("Damaged Lines Log\n")
    for log in damaged_logs:
      log_file.write(log + "\n")


if __name__ == "__main__":
  process_attendance_files(
      "./attendance_records", "attendance_report.txt", "damaged_lines.log"
  )
```[cite: 3]
