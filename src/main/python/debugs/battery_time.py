# https://www.omnicalculator.com/other/drone-flight-time

battery_capacity = 8.8  # Ah
battery_discharge = 0.8  # 80%
battery_voltage = 36  # V
all_up_weight = 2.5  # kg
watts_to_lift_1_kg = 170  # W/kg

average_amp_draw = all_up_weight * watts_to_lift_1_kg / battery_voltage
drone_flight_time = battery_capacity * battery_discharge / average_amp_draw * 60

print("average_amp_draw=", round(average_amp_draw, 1))
print("drone_flight_time=", round(drone_flight_time, 1))
