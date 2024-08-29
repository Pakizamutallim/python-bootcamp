from datetime import datetime

class Room:
    def __init__(self, room_number, rate_per_night):
        self.room_number = room_number
        self.rate_per_night = rate_per_night
        self.availability = []  # List of tuples containing (check_in, check_out)

    def is_available(self, check_in, check_out):
        for (start, end) in self.availability:
            if (start < check_out and check_in < end):
                return False
        return True

    def update_availability(self, check_in, check_out):
        self.availability.append((check_in, check_out))

    def get_room_details(self):
        return {
            "Room Number": self.room_number,
            "Rate per Night": self.rate_per_night,
            "Availability": self.availability
        }

class SingleRoom(Room):
    def __init__(self, room_number):
        super().__init__(room_number, rate_per_night=100)

class DoubleRoom(Room):
    def __init__(self, room_number):
        super().__init__(room_number, rate_per_night=150)

class Suite(Room):
    def __init__(self, room_number):
        super().__init__(room_number, rate_per_night=300)



class Hotel:
    def __init__(self, name, loc):
        self.name = name
        self.location = loc
        self.rooms = []
        self.reservations = []

    def add_room(self, room):
        self.rooms.append(room)
    
    def remove_room(self, room_num):
        self.rooms = [room for room in self.rooms if room.room_num != room_num]
    
    def find_available_room(self, room_type, check_in, check_out):
        for room in self.rooms:
            if isinstance(room, room_type) and room.is_available(check_in, check_out):
                return room
        return None
    
    def make_reservation(self, guest, room_type, check_in, check_out):
        room = self.find_available_room(room_type, check_in, check_out)
        if room:
            reservation = Reservation(guest, room, check_in, check_out)
            self.reservations.append(reservation)
            room.update_availability(check_in, check_out)
            guest.add_reservation(reservation)
            return reservation
        else:
            print("No available rooms.")
            return None
    def get_reservations(self):
        return self.reservations



class Reservation:
    def __init__(self, guest, room, check_in, check_out):
        self.reservation_id = id(self)  # A simple way to generate unique IDs
        self.guest = guest
        self.room = room
        self.check_in = check_in
        self.check_out = check_out
        self.total_cost = self.calculate_total_cost()

    def calculate_total_cost(self):
        duration = (self.check_out - self.check_in).days
        return duration * self.room.rate_per_night

    def modify_reservation(self, new_check_in, new_check_out):
        if self.room.is_available(new_check_in, new_check_out):
            self.check_in = new_check_in
            self.check_out = new_check_out
            self.total_cost = self.calculate_total_cost()
            self.room.update_availability(new_check_in, new_check_out)
        else:
            print("Room not available for the new dates.")

    def cancel_reservation(self):
        self.room.availability.remove((self.check_in, self.check_out))

    def get_reservation_details(self):
        return {
            "Reservation ID": self.reservation_id,
            "Guest": self.guest.name,
            "Room Number": self.room.room_number,
            "Check-in Date": self.check_in,
            "Check-out Date": self.check_out,
            "Total Cost": self.total_cost
        }




class Guest:
    def __init__(self, name, contact_info):
        self.name = name
        self.contact_info = contact_info
        self.reservations = []

    def add_reservation(self, reservation):
        self.reservations.append(reservation)

    def view_reservations(self):
        return [reservation.get_reservation_details() for reservation in self.reservations]

    def update_contact_info(self, new_contact_info):
        self.contact_info = new_contact_info




from datetime import datetime

# Create hotel instance
hotel = Hotel("Luxury Stay", "New York")

# Create rooms
room1 = SingleRoom(101)
room2 = DoubleRoom(102)
room3 = Suite(103)

# Add rooms to hotel
hotel.add_room(room1)
hotel.add_room(room2)
hotel.add_room(room3)

# Create guest instance
guest = Guest("John Doe", "john.doe@example.com")

# Make a reservation
check_in = datetime(2024, 9, 10)
check_out = datetime(2024, 9, 25)
reservation = hotel.make_reservation(guest, SingleRoom, check_in, check_out)

# View reservations
print(guest.view_reservations())
