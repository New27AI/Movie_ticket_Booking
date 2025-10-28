# Smart Cinema Booking System

This is a sophisticated cinema ticket booking system implemented using Python for the GUI and Verilog for the backend logic. The system combines modern GUI elements with hardware-level seat management and pricing calculations.

## Project Structure

- `cinema_gui.py` - Python-based graphical user interface
- `cinema_system.v` - Verilog implementation of the core booking system
- `cinema_tb.v` - Verilog testbench for system verification
- `cinema_system.vcd` - Value Change Dump file for waveform analysis
- `commands.txt` - Interface file for GUI-to-Verilog communication

## Features

### 1. Multi-Theater Support
- Manages 4 separate theaters
- Each theater has an 8x8 seating grid (64 seats)
- Real-time seat availability tracking

### 2. Seat Categories
- Standard seats
- Premium seats
- VIP seats

### 3. Dynamic Pricing System
Base prices:
- Standard: 150 units
- Premium: 200 units
- VIP: 300 units

Price multipliers based on:
- Time slots:
  - Morning: 80%
  - Afternoon: 100%
  - Evening: 120%
- Day types:
  - Weekday: 100%
  - Weekend: 120%
  - Holiday: 150%

### 4. GUI Features
- Interactive seat selection
- Visual seat status representation
- Real-time statistics display
- Booking and cancellation functionality
- Scrollable seating layout
- Theater selection dropdown

### 5. Backend System (Verilog)
- Real-time seat status tracking
- Dynamic price calculation
- Revenue management
- Booking/cancellation handling
- Multiple theater management

## Technical Implementation

### GUI (Python)
```python
class CinemaGUI:
    # Main GUI implementation using tkinter
    # Features:
    # - Theater selection
    # - Interactive seat grid
    # - Booking controls
    # - Statistics display
    # - Waveform visualization
```

### Core System (Verilog)
```verilog
module cinema_system(
    // System inputs
    input clk, reset,
    input [1:0] theater_id,
    input [3:0] row, col,
    input book_seat, cancel_seat,
    input [1:0] seat_category,
    input [1:0] time_slot,
    input [2:0] day_type,
    
    // System outputs
    output reg [7:0] seat_status_out,
    output reg [7:0] total_booked,
    output reg [7:0] total_available,
    output reg [15:0] revenue,
    output reg [15:0] total_revenue
);
```

## System Requirements

1. Python dependencies:
   - tkinter
   - PIL (Python Imaging Library)
   - json

2. Hardware simulation:
   - Verilog simulator (for backend logic)
   - VCD viewer (for waveform analysis)

## Usage

1. Start the GUI:
   ```bash
   python cinema_gui.py
   ```

2. Using the System:
   - Select a theater from the dropdown
   - Click on seats to select them
   - Use the booking panel to confirm or cancel selections
   - View real-time statistics and revenue information
   - Monitor system state through the waveform viewer

## Testing

The system includes a comprehensive testbench (`cinema_tb.v`) that:
- Simulates the core booking system
- Generates test scenarios
- Monitors system outputs
- Creates waveform dumps for analysis
- Interfaces with the GUI through command files

## Future Enhancements

1. Additional Features:
   - Multiple show timings
   - Online payment integration
   - Advance booking system
   - Season pass support

2. Technical Improvements:
   - Database integration
   - Network support for distributed deployment
   - Mobile application interface
   - Enhanced security features

## Contributing

Feel free to contribute to this project by:
1. Forking the repository
2. Creating a feature branch
3. Submitting a pull request

## License

This project is open for educational and development purposes.
