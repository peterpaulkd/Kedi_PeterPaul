# Assignment 3: Real World Application of Loop Control Statements
# FIFA World Cup 2026 Team Manager Simulation

print(" FIFA World Cup 2026 Simulation ")

morale = 50
strength = 50
injuries = 0

# PRE-TOURNAMENT PHASE
while True:
    print("\nPre-Tournament Preparation")
    print("1. Training")
    print("2. Friendly Match")
    print("3. Recovery")
    print("4. Start Tournament")

    choice = input("Choose an option: ")

    if choice == "1":
        strength += 10
        print("Training completed! Strength +10")

    elif choice == "2":
        morale += 10
        injuries += 1
        print("Friendly match played! Morale +10, Injuries +1")

    elif choice == "3":
        if injuries == 0:
            print("No injuries to recover from.")
            continue      # Skip remaining code and restart loop

        injuries -= 1
        print("Recovery successful! Injuries -1")

    elif choice == "4":
        print("Tournament begins!")
        break            # Exit preparation phase

    else:
        print("Invalid choice.")
        continue

# GROUP STAGE
group_match = 1

while group_match <= 3:

    print(f"\nGroup Match {group_match}")

    result = input("Enter result (win/lose): ").lower()

    if result == "win":
        morale += 5
        strength += 5
        print("Great victory!")

    elif result == "lose":
        morale -= 10
        print("You lost the match.")

        if morale <= 20:
            print("Team morale too low. Eliminated!")
            break       # Tournament ends

    else:
        print("Invalid input.")
        continue        # Repeat same match

    group_match += 1

# KNOCKOUT STAGE

if group_match > 3:

    stages = [
        "Round of 16",
        "Quarter-final",
        "Semi-final",
        "Final"
    ]

    stage_number = 0

    while stage_number < len(stages):

        print(f"\n{stages[stage_number]}")

        result = input("Enter result (win/lose): ").lower()

        if result == "lose":
            print("Your team has been knocked out!")
            break

        elif result == "win":
            print("You advance to the next stage!")

        else:
            print("Invalid input.")
            continue

        # Placeholder for future features
        pass

        stage_number += 1

    if stage_number == len(stages):
        print("\n CONGRATULATIONS!")
        print("Your team won the FIFA World Cup 2026!")