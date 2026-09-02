import subprocess
import time
from datetime import datetime

while True:

    try:

        print(
            f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] "
            "Synchronisatie gestart"
        )

        result = subprocess.run(
            ["python", "ClubhuisAgenda.py"],
            capture_output=True,
            text=True
        )

        print(result.stdout)

        if result.stderr:
            print("FOUTEN:")
            print(result.stderr)

        print(
            f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] "
            "Synchronisatie voltooid"
        )

    except Exception as ex:

        print(
            f"FOUT: {ex}"
        )

    print(
        "Wachten 60 seconden..."
    )

    time.sleep(60)