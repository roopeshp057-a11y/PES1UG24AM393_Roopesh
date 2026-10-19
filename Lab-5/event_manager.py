"""Event manager for guest registration, capacity tracking, and reports."""

from datetime import date
import json
import secrets
import subprocess  # nosec B404

events = {}


def create_event(event_name, venue, capacity=50, guests=None):
    """Create an event with venue, maximum capacity, and guest list."""
    if guests is None:
        guests = []
    else:
        guests = list(guests)
    events[event_name] = {
        "venue": venue,
        "capacity": capacity,
        "guests": guests,
    }
    return events[event_name]


def register_guest(event_name, guest):
    """Register a guest for a specific event if seats are available."""
    event = events.get(event_name)
    if event is None:
        print("No such event:", event_name)
        return False
    if len(event["guests"]) >= event["capacity"]:
        print(event_name, "is full, cannot add", guest)
        return False
    event["guests"].append(guest)
    return True


def seats_left(event_name):
    """Return the number of remaining seats available for the event."""
    event = events[event_name]
    return event["capacity"] - len(event["guests"])


def event_status(event_date):
    """Return whether an event is upcoming or completed."""
    if event_date >= date.today():
        return "Upcoming"
    return "Completed"


def guest_report(event_name, sort_order="name"):
    """Return a comma-separated report of guests registered for an event."""
    names = list(events[event_name]["guests"])
    if sort_order == "desc":
        names = sorted(names, reverse=True)
    else:
        names = sorted(names)
    return ", ".join(names)


def save_events(file_name="events.json"):
    """Save current events data to a JSON file."""
    with open(file_name, "w", encoding="utf-8") as file_handle:
        json.dump(events, file_handle, indent=2)


def load_events(file_name="events.json"):
    """Load and return events data from a JSON file."""
    with open(file_name, "r", encoding="utf-8") as file_handle:
        return json.load(file_handle)


def print_badges(event_name):
    """Print badge labels for an event using a subprocess."""
    subprocess.run(
        ["/usr/bin/lp", f"badges_{event_name}.txt"],
        check=False,
    )  # nosec B603


def main():
    """Demonstrate the event manager functionalities."""
    create_event("Tech Meetup", "Hall A", 3)
    create_event("Alumni Dinner", "Rooftop", 2)
    register_guest("Tech Meetup", "Asha")
    register_guest("Tech Meetup", "Ravi")
    register_guest("Alumni Dinner", "Meena")
    register_guest("Workshop", "Kiran")
    left = seats_left("Tech Meetup")
    print("Seats left at Tech Meetup:", left)
    print("Seats left at Alumni Dinner:", seats_left("Alumni Dinner"))
    print("Tech Meetup guests:", guest_report("Tech Meetup", "name"))
    print("Tech Meetup is", event_status(date(2099, 1, 15)))
    print("Alumni Dinner is", event_status(date(2020, 5, 1)))
    winner = secrets.choice(events["Tech Meetup"]["guests"])
    print("Lucky draw winner:", winner)
    save_events()
    restored = load_events()  # reload to confirm the save worked
    print("Events restored from file:", len(restored))
    print("Venues:", [e["venue"] for e in restored.values()])


if __name__ == "__main__":
    main()
