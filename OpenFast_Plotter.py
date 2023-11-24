"""
OpenFast Plotter

Author: Danial Haselibozchaloee
Ph.D. student in Civil Engineering-Structure at FEUP, Porto, Portugal
up201911748@fe.up.pt
danialhaseli@yahoo.com

Instructions:
This code allows you to plot the output of OpenFast simulations. Follow the steps below to run the code using the command prompt (cmd).

1. Open a cmd window.
2. Navigate to the directory containing the OpenFast Plotter file using the 'cd' command. For example:
   D:\Wind_Turbine_Models_by_OpenFast\Model_01>

3. Install the required libraries using the following commands:
   pip install matplotlib
   pip install pandas
   pip install tk

4. Make sure you have an icon file named 'OF.ico' in the same directory as 'OpenFast_Plotter.py'. The icon will be used for the window.

5. Run the OpenFast Plotter file using the Python interpreter. For example:
   D:\Wind_Turbine_Models_by_OpenFast\Model_01>python OpenFast_Plotter.py

Note: The 'OF.ico' icon should be present in the same directory as 'OpenFast_Plotter.py'. The code will generate a plot, and the output will be saved as 'Figure.svg' in the same directory.
"""

import pandas as pd
import tkinter as tk
from tkinter import filedialog, ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def convert_out_to_txt(input_file):
    # Read the content of the .out file
    with open(input_file, 'r') as in_file:
        content = in_file.read()

    # Create the output file name by replacing '.out' with '_text_file.txt'
    output_file = input_file.replace('.out', '_text_file.txt')

    # Write the content to the .txt file
    with open(output_file, 'w') as out_file:
        out_file.write(content)

    print(f"Conversion complete. Saved as: {output_file}")

    return output_file

def plot_graph(file_path, var1, var2, start_time, end_time):
    # Read the content of the text file into a pandas DataFrame
    df = pd.read_csv(file_path, delim_whitespace=True, skiprows=8, header=None, names=column_names)

    # Calculate frequency and add it as a new column
    df["Frequency"] = 1 / df["Time"]

    # Limit the DataFrame based on start and end times
    df = df[(df["Time"] >= start_time) & (df["Time"] <= end_time)]

    # Plotting
    plt.figure(figsize=(10, 8), dpi=300)
    linewidth = 1
    fig, ax = plt.subplots()

    if var1 == "Frequency":
        ax.plot(df["Frequency"], df[var2], linewidth=linewidth)
        ax.set_xlabel("Frequency")
    elif var2 == "Frequency":
        ax.plot(df[var1], df["Frequency"], linewidth=linewidth)
        ax.set_xlabel(var1)
    else:
        ax.plot(df[var1], df[var2], linewidth=linewidth)
        ax.set_xlabel(var1)

    ax.set_ylabel(var2)
    ax.set_title(f"{var1} vs {var2}")

    # Display the plot in the GUI
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.grid(row=7, column=0, columnspan=3)

    # Save the plot as an SVG file
    plot_filename = "Figure.svg"
    fig.savefig(plot_filename, format="svg")
    print(f"Plot saved as {plot_filename}")


# Specify the column names
column_names = ["Time", "PtfmTDxt", "PtfmTDyt", "PtfmTDzt", "PtfmRDxi", "PtfmRDyi", "PtfmRDzi",
                "TwrBsMxt", "TwrBsMyt", "YawBrTDxp", "YawBrTDyp", "YawBrTAxp", "YawBrTAyp"]

# Create the main window
window = tk.Tk()
window.title("OpenFast Plotter")

# Set the icon for the window (replace 'path/to/icon.ico' with the actual path to your icon file)
window.iconbitmap('OF.ico')

# Create labels and entry widgets for file path, variable selection, and time limits
tk.Label(window, text="File Path:").grid(row=0, column=0)
file_path_var = tk.StringVar()
file_entry = tk.Entry(window, textvariable=file_path_var, state="readonly")
file_entry.grid(row=0, column=1)
file_button = tk.Button(window, text="Open .out File", command=lambda: file_path_var.set(filedialog.askopenfilename(filetypes=[("Out files", "*.out")])))
file_button.grid(row=0, column=2)

tk.Label(window, text="Variable 1:").grid(row=1, column=0)
var1_var = tk.StringVar()
var1_combobox = ttk.Combobox(window, textvariable=var1_var)
var1_combobox.grid(row=1, column=1)

tk.Label(window, text="Variable 2:").grid(row=2, column=0)
var2_var = tk.StringVar()
var2_combobox = ttk.Combobox(window, textvariable=var2_var)
var2_combobox.grid(row=2, column=1)

tk.Label(window, text="Start Time:").grid(row=3, column=0)
start_time_var = tk.DoubleVar()
start_time_entry = tk.Entry(window, textvariable=start_time_var)
start_time_entry.grid(row=3, column=1)

tk.Label(window, text="End Time:").grid(row=4, column=0)
end_time_var = tk.DoubleVar()
end_time_entry = tk.Entry(window, textvariable=end_time_var)
end_time_entry.grid(row=4, column=1)

# Create a button for plotting
plot_button = tk.Button(window, text="Plot", command=lambda: plot_graph(file_path_var.get(), var1_var.get(), var2_var.get(), start_time_var.get(), end_time_var.get()))
plot_button.grid(row=5, column=0, pady=10, columnspan=3)

# Populate the variable dropdowns with column names from the DataFrame
variable_names = column_names + ["Frequency"]  # Include "Frequency" as an option
var1_combobox['values'] = variable_names
var1_combobox.set(column_names[0])  # Set the default value

var2_combobox['values'] = variable_names
var2_combobox.set(column_names[1])  # Set the default value

# Start the GUI event loop
window.mainloop()