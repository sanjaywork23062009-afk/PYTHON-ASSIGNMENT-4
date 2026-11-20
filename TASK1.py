from decimal import Decimal, InvalidOperation


def process_mess_bills(file_path):
  total = Decimal("0.00")
  report_lines = []
  rejected_lines = []

  try:
    with open(file_path, mode="r", encoding="utf-8") as file:
      for line_num, raw_line in enumerate(file, start=1):
        line = raw_line.strip()
        if not line:
          continue
        parts = [part.strip() for part in line.split(",")]
        if len(parts) != 3:
          rejected_lines.append((line_num, line, "Invalid column count"))
          continue
        reg_no, name, amount_str = parts
        try:
          amount = Decimal(amount_str)
          if amount < 0:
            raise ValueError("Negative amount")
          total += amount
          report_lines.append(f"{name} {amount:.2f}")
        except (InvalidOperation, ValueError):
          rejected_lines.append(
              (line_num, line, f"Invalid amount: '{amount_str}'")
          )
  except FileNotFoundError:
    print(f"Error: The file '{file_path}' was not found.")
    return
  except PermissionError:
    print(f"Error: Permission denied when accessing '{file_path}'.")
    return

  print("\n".join(report_lines))
  print(f"Total: {total:.2f}")

  if rejected_lines:
    print("\n--- Rejected Lines (Requires Review) ---")
    for line_num, content, reason in rejected_lines:
      print(f"Line {line_num}: '{content}' -> {reason}")


if __name__ == "__main__":
  process_mess_bills("mess_oct.txt")
