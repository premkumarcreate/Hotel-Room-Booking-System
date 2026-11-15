import os

# File to store bookings persistently
BOOKINGS_FILE = "bookings.txt"

# Room details dictionary (Room Number -> Type and Rate per night)
rooms = {
    101: {"type": "Single", "rate": 2000},
    102: {"type": "Double", "rate": 3500},
    201: {"type": "Suite", "rate": 6000},
}


def load_bookings():
  """Load bookings from bookings.txt at program start."""
  bookings = []
  if os.path.exists(BOOKINGS_FILE):
    with open(BOOKINGS_FILE, "r") as f:
      for line in f:
        parts = line.strip().split(",")
        if len(parts) == 3:
          room_no, guest_name, nights = parts
          bookings.append(
              {"room": int(room_no), "guest": guest_name, "nights": int(nights)}
          )
  return bookings


def save_bookings(bookings):
  """Save bookings to bookings.txt after every change."""
  with open(BOOKINGS_FILE, "w") as f:
    for b in bookings:
      f.write(f"{b['room']},{b['guest']},{b['nights']}\n")


def view_available_rooms(bookings):
  """View all currently available rooms."""
  booked_room_nos = [b["room"] for b in bookings]
  available = [
      (r_no, details)
      for r_no, details in rooms.items()
      if r_no not in booked_room_nos
  ]

  if not available:
    print("No rooms currently available.")
    return

  avail_strs = []
  print("Available Rooms:")
  for r_no, details in available:
    print(f"Room {r_no}: {details['type']} - Rs. {details['rate']} per night")
    avail_strs.append(f"{r_no} {details['type']} Rs. {details['rate']}")

  # Format matching test case output style
  print("\nFormatted View:", " | ".join(avail_strs))


def book_room(bookings):
  """Book a room for a guest for a number of nights with validation and bill generation."""
  try:
    guest = input("Enter Guest Name: ").strip()
    room_no = int(input("Enter Room Number (101, 102, 201): "))

    if room_no not in rooms:
      print("Invalid room number. Please choose a valid room.")
      return

    # Check for double booking
    for b in bookings:
      if b["room"] == room_no:
        print(f"Room {room_no} is already booked. Please choose another room.")
        return

    nights = int(input("Enter number of nights (1 to 30): "))
    if nights < 1 or nights > 30:
      print("Invalid number of nights. Must be between 1 and 30.")
      return

    # Calculate Bill (Rate * nights + 12% GST)
    rate = rooms[room_no]["rate"]
    base_amount = rate * nights
    gst = 0.12 * base_amount
    total_bill = base_amount + gst

    # Add booking to list
    bookings.append({"room": room_no, "guest": guest, "nights": nights})
    save_bookings(bookings)

    # Output format matching test cases
    night_str = f"{nights} night" if nights == 1 else f"{nights} nights"
    print(f"\nRoom: {room_no} booked for {guest} | {night_str}")
    print(
        f"Bill: {int(base_amount)} + GST {int(gst)} = Rs. {int(total_bill)}"
    )

  except ValueError:
    print("Invalid input! Please enter numeric values for room and nights.")


def generate_bill(bookings):
  """Generate or view bill for an existing booking."""
  try:
    room_no = int(input("Enter Room Number to generate bill: "))
    booking = next((b for b in bookings if b["room"] == room_no), None)

    if not booking:
      print(f"No active booking found for Room {room_no}.")
      return

    rate = rooms[room_no]["rate"]
    nights = booking["nights"]
    base_amount = rate * nights
    gst = 0.12 * base_amount
    total_bill = base_amount + gst

    print(f"\n--- Bill Details for Room {room_no} ---")
    print(f"Guest Name: {booking['guest']}")
    print(f"Nights: {nights}")
    print(
        f"Bill: {int(base_amount)} + GST {int(gst)} = Rs. {int(total_bill)}"
    )

  except ValueError:
    print("Invalid room number format.")


def cancel_booking(bookings):
  """Cancel an existing room booking."""
  try:
    room_no = int(input("Enter Room Number to cancel booking: "))
    booking = next((b for b in bookings if b["room"] == room_no), None)

    if not booking:
      print(f"Room {room_no} is not currently booked.")
      return

    bookings.remove(booking)
    save_bookings(bookings)
    print(
        f"Booking for room {room_no} cancelled. Room {room_no} is now available."
    )

  except ValueError:
    print("Invalid room number format.")


def main():
  bookings = load_bookings()

  while True:
    print("\n--- Hotel Room Booking System ---")
    print("1. View Available Rooms")
    print("2. Book Room")
    print("3. Generate Bill")
    print("4. Cancel Booking")
    print("5. Exit")

    choice = input("Enter your menu option (1-5): ").strip()

    if choice == "1":
      view_available_rooms(bookings)
    elif choice == "2":
      book_room(bookings)
    elif choice == "3":
      generate_bill(bookings)
    elif choice == "4":
      cancel_booking(bookings)
    elif choice == "5":
      print("Exiting application. Thank you!")
      break
    else:
      print("Invalid choice! Please select between 1 and 5.")


if __name__ == "__main__":
  main()