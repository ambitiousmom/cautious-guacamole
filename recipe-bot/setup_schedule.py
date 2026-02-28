"""
setup_schedule.py — Register a Windows Task Scheduler task to run RecipeBot daily.
Run once: python setup_schedule.py --time 17:00
"""

import argparse
import os
import sys
import subprocess


def setup(hour_minute="17:00", task_name="RecipeBot_DailyDinner"):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    notify_script = os.path.join(script_dir, "notify.py")
    python_exe = sys.executable

    # Build the command that Task Scheduler will run
    action = f'"{python_exe}" "{notify_script}"'

    # Check for ICS config
    config_path = os.path.join(script_dir, "config.txt")
    if os.path.exists(config_path):
        with open(config_path) as f:
            for line in f:
                if line.startswith("ics="):
                    ics_url = line.strip().split("=", 1)[1]
                    action += f' --ics "{ics_url}"'

    # Delete existing task if it exists
    subprocess.run(
        ["schtasks", "/delete", "/tn", task_name, "/f"],
        capture_output=True, text=True
    )

    # Create the scheduled task
    result = subprocess.run(
        [
            "schtasks", "/create",
            "/tn", task_name,
            "/tr", action,
            "/sc", "daily",
            "/st", hour_minute,
            "/f",
        ],
        capture_output=True, text=True
    )

    if result.returncode == 0:
        print(f"✅ Scheduled! RecipeBot will notify you daily at {hour_minute}")
        print(f"   Task name: {task_name}")
        print(f"   Command: {action}")
        print()
        print(f"   To change time: python setup_schedule.py --time 18:00")
        print(f"   To remove:      schtasks /delete /tn {task_name} /f")
        print(f"   To test now:    python notify.py")
    else:
        print(f"❌ Failed to create task: {result.stderr}")
        print("   Try running as administrator, or create the task manually:")
        print(f"   schtasks /create /tn {task_name} /tr \"{action}\" /sc daily /st {hour_minute}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Schedule RecipeBot daily notification")
    parser.add_argument("--time", default="17:00", help="Time to notify (HH:MM, 24h format). Default: 17:00")
    parser.add_argument("--name", default="RecipeBot_DailyDinner", help="Task name")
    args = parser.parse_args()
    setup(args.time, args.name)
