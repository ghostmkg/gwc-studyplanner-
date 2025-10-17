from utils import collect_availability, find_common_slots, save_schedule

def main():
    print("📚 Group Study Scheduler\n")
    
    num_members = int(input("Enter number of group members: "))
    members = []

    for i in range(num_members):
        name = input(f"Enter name of member {i+1}: ")
        members.append(name)

    availability = collect_availability(members)
    common_slots = find_common_slots(availability)

    if common_slots:
        print("\n✅ Common Available Time Slots:")
        for slot in common_slots:
            print(slot)
        save_schedule(common_slots)
    else:
        print("\n❌ No common availability found.")

if __name__ == "__main__":
    main()

import json
import os
import csv

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
TIME_SLOTS = ["9-10AM", "10-11AM", "11-12PM", "1-2PM", "2-3PM", "3-4PM"]

def collect_availability(members):
    availability = {}

    for member in members:
        print(f"\nEnter availability for {member}:")
        availability[member] = []

        for day in DAYS:
            for slot in TIME_SLOTS:
                response = input(f"  Is {day} {slot} available? (y/n): ").lower()
                if response == 'y':
                    availability[member].append(f"{day} {slot}")

    # Save to JSON
    os.makedirs("data", exist_ok=True)
    with open("data/availability.json", "w") as f:
        json.dump(availability, f, indent=4)

    return availability

def find_common_slots(availability):
    all_sets = [set(slots) for slots in availability.values()]
    common = set.intersection(*all_sets) if all_sets else set()
    return sorted(list(common))

def save_schedule(common_slots):
    os.makedirs("output", exist_ok=True)

    # Save as TXT
    with open("output/schedule.txt", "w") as f:
        f.write("Group Study Common Time Slots:\n")
        for slot in common_slots:
            f.write(f"- {slot}\n")

    # Save as CSV
    with open("output/schedule.csv", "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Day", "Time Slot"])
        for slot in common_slots:
            day, time = slot.split(' ', 1)
            writer.writerow([day, time])
