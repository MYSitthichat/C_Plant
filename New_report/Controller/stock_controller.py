import os
import sys
from PySide6.QtCore import Slot, QObject

# Import your database reader
try:
    from . import database_reader
except ImportError:
    import database_reader # Fallback for testing


class StockController(QObject):
    
    def __init__(self, main_window):
        """
        Initializes the controller for the stock tab.
        It does NOT load the UI, it just gets a reference to the main window.
        """
        super(StockController, self).__init__()
        # Store the reference to the main window
        self.stock_window = main_window 
        
        # --- Get references to widgets from the main window ---
        # (These are the same names from your .ui file)
        self.rock1_input = self.stock_window.rock1_input_weight_lineEdit
        self.rock1_remain = self.stock_window.rock1_left_weight_lineEdit
        
        self.rock2_input = self.stock_window.rock2_input_weight_lineEdit
        self.rock2_remain = self.stock_window.rock2_left_weight_lineEdit
        
        self.sand_input = self.stock_window.sand_input_weight_lineEdit
        self.sand_remain = self.stock_window.sand_left_weight_lineEdit
        
        self.fly_ash_input = self.stock_window.fly_ash_input_weight_lineEdit
        self.fly_ash_remain = self.stock_window.fly_ash_left_weight_lineEdit
        
        self.cement_input = self.stock_window.cement_input_weight_lineEdit
        self.cement_remain = self.stock_window.cement_left_weight_lineEdit
        
        self.chem1_input = self.stock_window.chemical_solution1_input_weight_lineEdit
        self.chem1_remain = self.stock_window.chemical_solution1_left_weight_lineEdit
        
        self.chem2_input = self.stock_window.chemical_solution2_input_weight_lineEdit
        self.chem2_remain = self.stock_window.chemical_solution2_left_weight_lineEdit
        
        self.show_stock_button = self.stock_window.show_weight_pushButton
        
        # --- Connect Signals ---
        self.setup_signals()

    def setup_signals(self):
        """Connects the button signals for this tab."""
        if self.show_stock_button:
            self.show_stock_button.clicked.connect(self.update_stock_display)
        
        # --- ADJUSTMENT: This line is now commented out ---
        # This stops the data from loading when the program starts
        # self.update_stock_display()
        # --- END ADJUSTMENT ---

    @Slot()
    def update_stock_display(self):
        """Fetches stock data from DB and populates the stock tab LineEdits."""
        
        # Call the function in your database reader
        stock_data = database_reader.get_stock_levels()
        
        if not stock_data:
            print("No stock data found.")
            return

        # Helper function to safely set text in LineEdits
        def set_text(widget, material, key):
            if widget and material in stock_data:
                # Format number with 2 decimal places
                widget.setText(f"{stock_data[material][key]:.2f}")
            elif widget:
                # Set to 0.00 if data is missing
                widget.setText("0.00")

        # Populate all fields
        set_text(self.rock1_input, 'rock1', 'input')
        set_text(self.rock1_remain, 'rock1', 'remaining')
        
        set_text(self.rock2_input, 'rock2', 'input')
        set_text(self.rock2_remain, 'rock2', 'remaining')
        
        set_text(self.sand_input, 'sand', 'input')
        set_text(self.sand_remain, 'sand', 'remaining')
        
        set_text(self.fly_ash_input, 'fly_ash', 'input')
        set_text(self.fly_ash_remain, 'fly_ash', 'remaining')
        
        set_text(self.cement_input, 'cement', 'input')
        set_text(self.cement_remain, 'cement', 'remaining')
        
        set_text(self.chem1_input, 'chem1', 'input')
        set_text(self.chem1_remain, 'chem1', 'remaining')
        
        set_text(self.chem2_input, 'chem2', 'input')
        set_text(self.chem2_remain, 'chem2', 'remaining')