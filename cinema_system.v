module cinema_system(
    input clk,
    input reset,
    input [1:0] theater_id,    // Theater selection (0-3)
    input [3:0] row,
    input [3:0] col,
    input book_seat,
    input cancel_seat,
    input [1:0] seat_category, // 00: Standard, 01: Premium, 10: VIP
    input [1:0] time_slot,     // 00: Morning, 01: Afternoon, 10: Evening
    input [2:0] day_type,      // 000: Weekday, 001: Weekend, 010: Holiday
    output reg [7:0] seat_status_out,
    output reg [7:0] total_booked,
    output reg [7:0] total_available,
    output reg [15:0] revenue,
    output reg [15:0] total_revenue
);
    // States for seat status
    parameter AVAILABLE = 1'b0;
    parameter BOOKED = 1'b1;
    
    // Seat categories
    parameter STANDARD = 2'b00;
    parameter PREMIUM = 2'b01;
    parameter VIP = 2'b10;
    
    // Time slots
    parameter MORNING = 2'b00;
    parameter AFTERNOON = 2'b01;
    parameter EVENING = 2'b10;
    
    // Day types
    parameter WEEKDAY = 3'b000;
    parameter WEEKEND = 3'b001;
    parameter HOLIDAY = 3'b010;
    
    // Base prices for different categories
    parameter BASE_STANDARD = 16'd150;
    parameter BASE_PREMIUM = 16'd200;
    parameter BASE_VIP = 16'd300;
    
    // Time multipliers (percentage)
    parameter MORNING_MULT = 8'd80;    // 80%
    parameter AFTERNOON_MULT = 8'd100; // 100%
    parameter EVENING_MULT = 8'd120;   // 120%
    
    // Day multipliers (percentage)
    parameter WEEKDAY_MULT = 8'd100;   // 100%
    parameter WEEKEND_MULT = 8'd120;   // 120%
    parameter HOLIDAY_MULT = 8'd150;   // 150%
    
    // Seat status array (8x8 grid)
    reg [7:0] seat_status [0:7];
    reg [1:0] seat_categories [0:7][0:7];
    
    // Price calculation
    reg [15:0] base_price;
    reg [7:0] time_multiplier;
    reg [7:0] day_multiplier;
    wire [15:0] calculated_price;
    
    integer i, j;
    
    // Initialize system
    initial begin
        total_booked = 0;
        total_available = 64;  // 8x8 grid
        revenue = 0;
        total_revenue = 0;
        
        // Initialize all seats as available
        for (i = 0; i < 8; i = i + 1) begin
            seat_status[i] = 8'b00000000;
            for (j = 0; j < 8; j = j + 1) begin
                seat_categories[i][j] = STANDARD; // Default to standard
            end
        end
    end
    
    // Calculate dynamic price
    assign calculated_price = (base_price * time_multiplier * day_multiplier) / 10000;
    
    // Main operation
    always @(posedge clk or posedge reset) begin
        if (reset) begin
            // Reset all seats to available
            for (i = 0; i < 8; i = i + 1) begin
                seat_status[i] = 8'b00000000;
            end
            total_booked = 0;
            total_available = 64;
            revenue = 0;
        end
        else begin
            // Set base price based on seat category
            case(seat_category)
                STANDARD: base_price = BASE_STANDARD;
                PREMIUM: base_price = BASE_PREMIUM;
                VIP: base_price = BASE_VIP;
                default: base_price = BASE_STANDARD;
            endcase
            
            // Set time multiplier
            case(time_slot)
                MORNING: time_multiplier = MORNING_MULT;
                AFTERNOON: time_multiplier = AFTERNOON_MULT;
                EVENING: time_multiplier = EVENING_MULT;
                default: time_multiplier = AFTERNOON_MULT;
            endcase
            
            // Set day multiplier
            case(day_type)
                WEEKDAY: day_multiplier = WEEKDAY_MULT;
                WEEKEND: day_multiplier = WEEKEND_MULT;
                HOLIDAY: day_multiplier = HOLIDAY_MULT;
                default: day_multiplier = WEEKDAY_MULT;
            endcase
            
            // Book a seat
            if (book_seat && row < 8 && col < 8) begin
                if (!(seat_status[row] & (1 << col))) begin
                    seat_status[row] = seat_status[row] | (1 << col);
                    seat_categories[row][col] = seat_category;
                    total_booked = total_booked + 1;
                    total_available = total_available - 1;
                    revenue = revenue + calculated_price;
                    total_revenue = total_revenue + calculated_price;
                end
            end
            
            // Cancel a seat
            if (cancel_seat && row < 8 && col < 8) begin
                if (seat_status[row] & (1 << col)) begin
                    seat_status[row] = seat_status[row] & ~(1 << col);
                    total_booked = total_booked - 1;
                    total_available = total_available + 1;
                    revenue = revenue - calculated_price;
                    total_revenue = total_revenue - calculated_price;
                end
            end
            
            // Output current row's status
            seat_status_out = seat_status[row];
        end
    end
endmodule 