module cinema_tb;
    reg clk;
    reg reset;
    reg [1:0] theater_id;
    reg [3:0] row;
    reg [3:0] col;
    reg book_seat;
    reg cancel_seat;
    reg [1:0] seat_category;
    reg [1:0] time_slot;
    reg [2:0] day_type;
    wire [7:0] seat_status_out;
    wire [7:0] total_booked;
    wire [7:0] total_available;
    wire [15:0] revenue;
    wire [15:0] total_revenue;
    
    // Instantiate the cinema system
    cinema_system uut (
        .clk(clk),
        .reset(reset),
        .theater_id(theater_id),
        .row(row),
        .col(col),
        .book_seat(book_seat),
        .cancel_seat(cancel_seat),
        .seat_category(seat_category),
        .time_slot(time_slot),
        .day_type(day_type),
        .seat_status_out(seat_status_out),
        .total_booked(total_booked),
        .total_available(total_available),
        .revenue(revenue),
        .total_revenue(total_revenue)
    );
    
    // Clock generation
    always #5 clk = ~clk;
    
    // Initialize variables
    initial begin
        clk = 0;
        reset = 1;
        theater_id = 0;
        row = 0;
        col = 0;
        book_seat = 0;
        cancel_seat = 0;
        seat_category = 0;
        time_slot = 0;
        day_type = 0;
        
        // Reset the system
        #10 reset = 0;
        
        // Monitor the outputs in decimal format
        $monitor("Time=%0t Theater=%d Row=%d Col=%d Category=%d Status=%d Booked=%d Available=%d Revenue=%d Total=%d",
                 $time, theater_id, row, col, seat_category, 
                 seat_status_out, total_booked, total_available, revenue, total_revenue);
        
        // Dump waveform
        $dumpfile("cinema_system.vcd");
        $dumpvars(0, cinema_tb);
        
        // Keep simulation running
        #1000000 $finish;
    end
    
    // Read commands from file
    integer file;
    reg [7:0] command;
    
    initial begin
        forever begin
            #10; // Check for new commands every 10 time units
            file = $fopen("commands.txt", "r");
            if (file) begin
                while (!$feof(file)) begin
                    $fscanf(file, "%b %d %d %d %d", command, theater_id, row, col, seat_category);
                    if (command == 1) begin
                        book_seat = 1;
                        #10 book_seat = 0;
                    end
                    else if (command == 2) begin
                        cancel_seat = 1;
                        #10 cancel_seat = 0;
                    end
                end
                $fclose(file);
                // Clear the commands file
                file = $fopen("commands.txt", "w");
                $fclose(file);
            end
        end
    end
endmodule 