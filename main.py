import requests
from datetime import date, timedelta
import time
import os

def get_data(date):
    url = f"https://www.nytimes.com/svc/wordle/v2/{date}.json"
    try:
        reqest = requests.get(url, timeout=5)

        # If NYT hasn't added it yet, stop
        if reqest.status_code == 404:
            return "STOP"

        if reqest.status_code != 200:
            return None

        return reqest.json()["solution"]

    except Exception as e:
        print(f"Error on {date}: {e}")
        return None


print("Welcome to James' Wordle Solver! Please input the following data: ")
year = int(input("What year? "))
month = int(input("What month? "))
day = int(input("What day? "))

output_path = input("Paste full path for output text file: ").strip('"')
    #ty chatgpt for helping fix the issue with the importing above

start_date = date(year, month, day)
end_date = date(year + 1, 12, 31)

current = start_date
results = []

while current <= end_date:
    result = get_data(current)

    if result == "STOP":
        print(f"No Wordle yet for {current}. Stopping.")
        break

    if result:
        print(current, result)
        results.append(f"{current} {result}")

    current += timedelta(days=1)
    time.sleep(0.1)

# Write to file
if results:
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(results))

    print(f"\nSaved {len(results)} entries to:")
    print(output_path)
else:
    print("\nNo data to save.")
