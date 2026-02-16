from fastmcp import FastMCP

# Initialize the server
mcp = FastMCP("SmartHomeManager")

# Mock database for our examples
sensor_data = {
    "living_room": {"temp": 22, "humidity": 45, "lights": False},
    "kitchen":     {"temp": 24, "humidity": 50, "lights": True}
}

@mcp.resource("smarthome://sensors/{room}")
def get_sensor_data(room: str) -> str:
    """
    Reads the live temperature and status data for a specific room.
    """
    if room not in sensor_data:
        return "Error: Room not found."
    
    data = sensor_data[room]
    # Convert bool to string strictly for the display report
    light_status = "ON" if data['lights'] else "OFF"

    return (f"--- STATUS REPORT: {room.upper()} ---\n"
            f"Temperature: {data['temp']}°C\n"
            f"Humidity: {data['humidity']}%\n"
            f"Lights: {light_status}\n"
            f"--------------------------------")

@mcp.tool()
def control_lights(room: str, status: bool) -> str:
    """
    Turns the lights on or off in a specific room.
    Args:
        room: The name of the room (e.g., 'living_room', 'kitchen')
        status: True for ON, False for OFF.
    """
    if room not in sensor_data:
        return f"Error: Room '{room}' does not exist."
    
    # Update the mock database
    sensor_data[room]["lights"] = status
    
    state_text = "ON" if status else "OFF"
    return f"Success: Lights in {room} have been turned {state_text}."

@mcp.prompt()
def morning_briefing() -> list:
    """
    Generates a prompt for a morning status check of the home.
    """
    return [
        {
            "role": "user",
            "content": (
                "Please perform a morning check of the smart home system. "
                "1. Access the 'smarthome://sensors/living_room' and 'smarthome://sensors/kitchen' resources. "
                "2. Summarize the temperature and which lights were left on overnight. "
                "3. If any lights are on, ask me if I want to turn them off using the control_lights tool."
            )
        }
    ]

if __name__ == "__main__":
    mcp.run()