import math
import tkinter as tk
from datetime import datetime, timezone
import pytz  # For timezone handling

# Constants
PI = 3.14159265359

# Timezone for Ionia, Michigan (Eastern Time Zone)
IONIA_TZ = pytz.timezone('America/Detroit')

def get_current_datetime_ionia():
    utc_now = datetime.now(timezone.utc)
    ionia_now = utc_now.astimezone(IONIA_TZ)
    return ionia_now

def calculate_orbit_position(day_of_year, orbital_period):
    orbit_angle = (day_of_year / orbital_period) * 2 * PI
    return orbit_angle

def update_positions(canvas, sun_center_x, sun_center_y, planet_orbit_radii, earth_radius, moon_orbit_radius):
    current_time_utc = datetime.now(timezone.utc)
    day_of_year = current_time_utc.timetuple().tm_yday
    current_hour = current_time_utc.hour

    canvas.delete("all")  # Clear the canvas

    # Sun
    canvas.create_oval(sun_center_x - 40, sun_center_y - 40,
                       sun_center_x + 40, sun_center_y + 40,
                       fill='yellow', outline='')

    # Planets
    planet_colors = ['gray', 'orange', 'blue', 'red', 'brown', 'tan', 'light blue', 'dark blue']
    orbital_periods = [88, 224.7, 365.25, 687, 4331, 10747, 30589, 59800]  # In Earth days
    earth_center_x, earth_center_y = 0, 0  # To be used for Moon's orbit

    for i, radius in enumerate(planet_orbit_radii):
        orbit_angle = calculate_orbit_position(day_of_year, orbital_periods[i])
        planet_x = sun_center_x + radius * math.cos(orbit_angle)
        planet_y = sun_center_y + radius * math.sin(orbit_angle)

        # Orbital path
        canvas.create_oval(sun_center_x - radius, sun_center_y - radius,
                           sun_center_x + radius, sun_center_y + radius,
                           outline=planet_colors[i], dash=(1, 4))

        # Planet
        canvas.create_oval(planet_x - 10, planet_y - 10,
                           planet_x + 10, planet_y + 10,
                           fill=planet_colors[i], outline='')

        # Earth-specific calculations (for Moon and Ionia)
        if i == 2:  # Earth is the third planet
            earth_center_x, earth_center_y = planet_x, planet_y

            # Ionia, Michigan
            ionia_longitude = -85.07
            ionia_hour_angle = (ionia_longitude / 180.0) * PI + (2 * PI * current_hour / 24)
            ionia_x = earth_center_x + earth_radius * 0.5 * math.cos(ionia_hour_angle)
            ionia_y = earth_center_y + earth_radius * 0.5 * math.sin(ionia_hour_angle)
            canvas.create_oval(ionia_x - 2, ionia_y - 2, ionia_x + 2, ionia_y + 2, fill='green', outline='')

    # Moon orbit and position
    moon_orbit_angle = calculate_orbit_position(day_of_year, 27.3)
    moon_center_x = earth_center_x + moon_orbit_radius * math.cos(moon_orbit_angle)
    moon_center_y = earth_center_y + moon_orbit_radius * math.sin(moon_orbit_angle)
    canvas.create_oval(earth_center_x - moon_orbit_radius, earth_center_y - moon_orbit_radius,
                       earth_center_x + moon_orbit_radius, earth_center_y + moon_orbit_radius,
                       outline='gray', dash=(1, 2))
    canvas.create_oval(moon_center_x - 5, moon_center_y - 5,
                       moon_center_x + 5, moon_center_y + 5,
                       fill='gray', outline='')

    canvas.after(3600000, update_positions, canvas, sun_center_x, sun_center_y, planet_orbit_radii, earth_radius, moon_orbit_radius)  # Update every hour

def create_celestial_bodies_canvas(root):
    canvas = tk.Canvas(root, width=1200, height=800, bg='white')
    canvas.pack()

    sun_center_x, sun_center_y = 600, 400
    planet_orbit_radii = [100, 150, 200, 250, 350, 450, 550, 650]  # Not to scale
    earth_radius = 20  # Earth's radius for Ionia representation
    moon_orbit_radius = 30  # Moon's orbit radius around Earth

    update_positions(canvas, sun_center_x, sun_center_y, planet_orbit_radii, earth_radius, moon_orbit_radius)

def create_main_window():
    root = tk.Tk()
    root.title("Celestial Bodies Representation")
    create_celestial_bodies_canvas(root)
    root.mainloop()

if __name__ == "__main__":
    create_main_window()
