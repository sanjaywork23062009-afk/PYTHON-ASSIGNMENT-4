import os
import tempfile


def save_returns(books):
  try:
    with open("returns.log", "a", encoding="utf-8") as log:
      for b in books:
        log.write(b + "\n")
  except Exception as e:
    with open("error.log", "a", encoding="utf-8") as err_log:
      err_log.write(f"Error saving returns: {str(e)}\n")
    raise


def process(day_file):
  try:
    with open(day_file, mode="r", encoding="utf-8") as f:
      books = f.read().splitlines()
    save_returns(books)
  except FileNotFoundError:
    print("missing")
  except Exception as e:
    print(f"Error processing {day_file}: {str(e)}")


if __name__ == "__main__":
  if os.path.exists("returns.log"):
    os.remove("returns.log")
  if os.path.exists("error.log"):
    os.remove("error.log")

  day1 = tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8")
  day1.write("BookA\nBookB")
  day1.close()

  day2 = tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8")
  day2.write("BookC\nBookD")
  day2.close()

  process(day1.name)
  process(day2.name)

  os.remove(day1.name)
  os.remove(day2.name)

  if os.path.exists("returns.log"):
    print("--- returns.log content ---")
    with open("returns.log", "r", encoding="utf-8") as f:
      print(f.read())
    os.remove("returns.log")

  if os.path.exists("error.log"):
    os.remove("error.log")
```[cite: 7, 8]
