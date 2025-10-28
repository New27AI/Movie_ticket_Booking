import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import json
import os
import subprocess
import time
import threading

class CinemaGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Smart Cinema Booking System")
        self.root.geometry("1200x800")
        
        # Initialize waveform process
        self.waveform_process = None
        
        # Create images directory if it doesn't exist
        if not os.path.exists("images"):
            os.makedirs("images")
        
        # Create necessary images
        self.create_images()
        
        # Initialize variables
        self.num_theaters = 4
        self.seat_status = [[[0 for _ in range(8)] for _ in range(8)] for _ in range(self.num_theaters)]
        self.seat_categories = [[[0 for _ in range(8)] for _ in range(8)] for _ in range(self.num_theaters)]
        self.total_booked = [0] * self.num_theaters
        self.total_available = [64] * self.num_theaters
        self.revenue = [0] * self.num_theaters
        self.total_revenue = 0
        self.selected_seat = None  # Track selected seat
        
        # Create main frames
        self.create_main_frames()
        
        # Create theater selection
        self.create_theater_selection()
        
        # Create theater view
        self.create_theater_view()
        
        # Create booking panel
        self.create_booking_panel()
        
        # Create statistics panel
        self.create_statistics_panel()
        
        # Create waveform viewer panel
        self.create_waveform_panel()
        
        # Start Verilog simulation
        self.start_verilog_simulation()
        
    def create_images(self):
        # Create sample images (you can replace these with actual images)
        self.screen_img = Image.new('RGB', (800, 100), 'black')
        self.screen_img = ImageTk.PhotoImage(self.screen_img)
        
        # Create smaller rectangular seats
        self.seat_empty = Image.new('RGB', (60, 30), 'green')
        self.seat_empty = ImageTk.PhotoImage(self.seat_empty)
        
        self.seat_booked = Image.new('RGB', (60, 30), 'red')
        self.seat_booked = ImageTk.PhotoImage(self.seat_booked)
        
        self.seat_premium = Image.new('RGB', (60, 30), 'blue')
        self.seat_premium = ImageTk.PhotoImage(self.seat_premium)
        
        self.seat_vip = Image.new('RGB', (60, 30), 'gold')
        self.seat_vip = ImageTk.PhotoImage(self.seat_vip)
        
        self.seat_selected = Image.new('RGB', (60, 30), 'yellow')
        self.seat_selected = ImageTk.PhotoImage(self.seat_selected)
        
    def create_main_frames(self):
        # Main container
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Left panel for theater view
        self.left_frame = ttk.Frame(self.main_frame)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Right panel for controls and stats
        self.right_frame = ttk.Frame(self.main_frame)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
    def create_theater_selection(self):
        # Theater selection
        theater_frame = ttk.LabelFrame(self.left_frame, text="Select Theater")
        theater_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.theater_var = tk.StringVar()
        theater_combo = ttk.Combobox(theater_frame, textvariable=self.theater_var,
                                   values=[f"Theater {i+1}" for i in range(self.num_theaters)])
        theater_combo.pack(fill=tk.X, padx=5, pady=5)
        theater_combo.bind('<<ComboboxSelected>>', self.change_theater)
        
    def change_theater(self, event):
        if not self.theater_var.get():
            return
        theater = int(self.theater_var.get().split()[-1]) - 1
        self.update_theater_view(theater)
        self.selected_seat = None  # Reset selected seat when changing theaters
        
    def create_theater_view(self):
        # Screen
        screen_frame = ttk.Frame(self.left_frame)
        screen_frame.pack(fill=tk.X, pady=20)
        
        # Center the screen
        screen_container = ttk.Frame(screen_frame)
        screen_container.pack(expand=True)
        screen_label = ttk.Label(screen_container, image=self.screen_img)
        screen_label.pack()
        
        # Main container for grid
        main_container = ttk.Frame(self.left_frame)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Create a canvas with scrollbar for vertical scrolling
        canvas_frame = ttk.Frame(main_container)
        canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(canvas_frame)
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=self.canvas.yview)
        
        # Create a frame inside canvas for the grid
        self.scrollable_frame = ttk.Frame(self.canvas)
        
        # Configure canvas
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="n")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack canvas and scrollbar
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Center the entire grid
        grid_outer_frame = ttk.Frame(self.scrollable_frame)
        grid_outer_frame.pack(expand=True, padx=20)
        
        # Add spacing at the top
        ttk.Label(grid_outer_frame, text="").pack(pady=10)
        
        # Grid container with padding for centering
        grid_container = ttk.Frame(grid_outer_frame)
        grid_container.pack(expand=True)
        
        # Row labels on the left
        row_label_frame = ttk.Frame(grid_container)
        row_label_frame.pack(side=tk.LEFT, padx=(0, 10))
        for i in range(8):
            ttk.Label(row_label_frame, text=f"Row {i+1}").pack(pady=12)  # Increased padding
        
        # Seat grid with proper spacing
        grid_frame = ttk.Frame(grid_container)
        grid_frame.pack(side=tk.LEFT)
        
        self.seat_buttons = []
        for i in range(8):
            row_frame = ttk.Frame(grid_frame)
            row_frame.pack(pady=2)
            row_buttons = []
            for j in range(8):
                btn = ttk.Button(row_frame, image=self.seat_empty,
                               command=lambda r=i, c=j: self.select_seat(r, c))
                btn.pack(side=tk.LEFT, padx=5, pady=5)  # Adjusted padding
                row_buttons.append(btn)
            self.seat_buttons.append(row_buttons)
        
        # Add column labels at the bottom
        col_label_frame = ttk.Frame(grid_outer_frame)
        col_label_frame.pack(fill=tk.X, pady=(5, 0))
        for j in range(8):
            ttk.Label(col_label_frame, text=f"Col {j+1}").pack(side=tk.LEFT, padx=15)  # Adjusted padding
            
        # Configure scrolling
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
    def create_booking_panel(self):
        # Booking controls
        control_frame = ttk.LabelFrame(self.right_frame, text="Booking Controls")
        control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Action buttons
        ttk.Button(control_frame, text="Book Selected Seat",
                  command=self.book_seat).pack(fill=tk.X, padx=5, pady=5)
        ttk.Button(control_frame, text="Cancel Selected Seat",
                  command=self.cancel_seat).pack(fill=tk.X, padx=5, pady=5)
        
    def create_statistics_panel(self):
        # Statistics display
        stats_frame = ttk.LabelFrame(self.right_frame, text="Statistics")
        stats_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Booked seats
        ttk.Label(stats_frame, text="Booked Seats:").pack()
        self.booked_label = ttk.Label(stats_frame, text="0")
        self.booked_label.pack()
        
        # Available seats
        ttk.Label(stats_frame, text="Available Seats:").pack()
        self.available_label = ttk.Label(stats_frame, text="64")
        self.available_label.pack()
        
        # Revenue
        ttk.Label(stats_frame, text="Current Revenue:").pack()
        self.revenue_label = ttk.Label(stats_frame, text="₹0")
        self.revenue_label.pack()
        
        # Total Revenue
        ttk.Label(stats_frame, text="Total Revenue:").pack()
        self.total_revenue_label = ttk.Label(stats_frame, text="₹0")
        self.total_revenue_label.pack()
        
    def create_waveform_panel(self):
        # Waveform viewer controls
        waveform_frame = ttk.LabelFrame(self.right_frame, text="Waveform Viewer")
        waveform_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(waveform_frame, text="Open Waveform",
                  command=self.open_waveform).pack(fill=tk.X, padx=5, pady=5)
        ttk.Button(waveform_frame, text="Refresh Waveform",
                  command=self.refresh_waveform).pack(fill=tk.X, padx=5, pady=5)
        
    def start_verilog_simulation(self):
        try:
            # Clear any existing commands
            with open("commands.txt", "w") as f:
                f.write("")
            
            # Compile Verilog
            subprocess.run(["iverilog", "-o", "cinema_system", "cinema_system.v", "cinema_tb.v"], check=True)
            
            # Start simulation in background
            self.simulation_process = subprocess.Popen(["vvp", "cinema_system"])
            print("Verilog simulation started successfully")
            
            # Start waveform viewer
            self.open_waveform()
            
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to compile Verilog: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start simulation: {str(e)}")
        
    def open_waveform(self):
        try:
            if not os.path.exists("cinema_system.vcd"):
                messagebox.showerror("Error", "VCD file not found. Please run the simulation first.")
                return
                
            if self.waveform_process is None:
                self.waveform_process = subprocess.Popen(["gtkwave", "cinema_system.vcd"])
                print("Waveform viewer started successfully")
            else:
                messagebox.showinfo("Info", "Waveform viewer is already running")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open waveform viewer: {str(e)}")
            
    def refresh_waveform(self):
        try:
            if not os.path.exists("cinema_system.vcd"):
                messagebox.showerror("Error", "VCD file not found. Please run the simulation first.")
                return
                
            if self.waveform_process is not None:
                self.waveform_process.terminate()
                self.waveform_process = subprocess.Popen(["gtkwave", "cinema_system.vcd"])
                print("Waveform viewer refreshed successfully")
            else:
                self.open_waveform()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to refresh waveform viewer: {str(e)}")
            
    def write_command(self, command, theater, row, col, category):
        try:
            with open("commands.txt", "a") as f:
                f.write(f"{command} {theater} {row} {col} {category}\n")
            # Wait for simulation to process the command
            time.sleep(0.1)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to write command: {str(e)}")
            
    def select_seat(self, row, col):
        if not self.theater_var.get():
            messagebox.showerror("Error", "Please select a theater first")
            return
        theater = int(self.theater_var.get().split()[-1]) - 1
        if self.seat_status[theater][row][col] == 0:
            # Reset previously selected seat
            if self.selected_seat:
                prev_row, prev_col = self.selected_seat
                self.seat_buttons[prev_row][prev_col].configure(image=self.seat_empty)
            
            # Select new seat
            self.selected_seat = (row, col)
            self.seat_buttons[row][col].configure(image=self.seat_selected)
            
    def get_seat_category(self, row):
        # Front rows (0-2): Standard
        # Middle rows (3-5): Premium
        # Back rows (6-7): VIP
        if row < 3:
            return 0  # Standard
        elif row < 6:
            return 1  # Premium
        else:
            return 2  # VIP
            
    def book_seat(self):
        if not self.selected_seat:
            messagebox.showerror("Error", "Please select a seat first")
            return
            
        row, col = self.selected_seat
        theater = int(self.theater_var.get().split()[-1]) - 1
        
        if self.seat_status[theater][row][col] == 0:
            # Get category based on row position
            category = self.get_seat_category(row)
            
            self.seat_status[theater][row][col] = 1
            self.seat_categories[theater][row][col] = category
            
            # Update seat appearance
            if category == 0:
                self.seat_buttons[row][col].configure(image=self.seat_booked)
            elif category == 1:
                self.seat_buttons[row][col].configure(image=self.seat_premium)
            else:
                self.seat_buttons[row][col].configure(image=self.seat_vip)
                
            self.total_booked[theater] += 1
            self.total_available[theater] -= 1
            
            # Calculate price based on category
            base_price = 150 if category == 0 else (200 if category == 1 else 300)
            self.revenue[theater] += base_price
            self.total_revenue += base_price
            
            self.update_statistics(theater)
            
            # Write command to file and wait for simulation
            self.write_command(1, theater, row, col, category)
            
            messagebox.showinfo("Success", f"Seat at row {row+1}, column {col+1} booked successfully!\nPrice: ₹{base_price:.2f}")
            self.selected_seat = None  # Reset selected seat after booking
        else:
            messagebox.showerror("Error", "Seat is already booked!")
            
    def cancel_seat(self):
        if not self.selected_seat:
            messagebox.showerror("Error", "Please select a seat first")
            return
            
        row, col = self.selected_seat
        theater = int(self.theater_var.get().split()[-1]) - 1
        
        if self.seat_status[theater][row][col] == 1:
            category = self.seat_categories[theater][row][col]
            
            self.seat_status[theater][row][col] = 0
            self.seat_buttons[row][col].configure(image=self.seat_empty)
            
            self.total_booked[theater] -= 1
            self.total_available[theater] += 1
            
            # Calculate refund based on original booking
            base_price = 150 if category == 0 else (200 if category == 1 else 300)
            self.revenue[theater] -= base_price
            self.total_revenue -= base_price
            
            self.update_statistics(theater)
            
            # Write command to file and wait for simulation
            self.write_command(2, theater, row, col, category)
            
            messagebox.showinfo("Success", f"Booking cancelled for seat at row {row+1}, column {col+1}\nRefund: ₹{base_price:.2f}")
            self.selected_seat = None  # Reset selected seat after cancellation
        else:
            messagebox.showerror("Error", "Seat is not booked!")
            
    def update_statistics(self, theater):
        self.booked_label.config(text=str(self.total_booked[theater]))
        self.available_label.config(text=str(self.total_available[theater]))
        self.revenue_label.config(text=f"₹{self.revenue[theater]:.2f}")
        self.total_revenue_label.config(text=f"₹{self.total_revenue:.2f}")
        
    def run(self):
        self.root.mainloop()
        
    def __del__(self):
        # Clean up processes
        if hasattr(self, 'simulation_process') and self.simulation_process:
            self.simulation_process.terminate()
        if hasattr(self, 'waveform_process') and self.waveform_process:
            self.waveform_process.terminate()

if __name__ == "__main__":
    app = CinemaGUI()
    app.run()