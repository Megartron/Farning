import tkinter as tk

def on_button_click(row, col):
    print(f"Button at ({row}, {col}) clicked")

root = tk.Tk()
root.title("3x3 Grid GUI")

buttons = []
for r in range(3):
    row_buttons = []
    for c in range(3):
        btn = tk.Button(root, text=f"({r},{c})", width=20, height=6, command=lambda r=r, c=c: on_button_click(r, c))
        btn.grid(row=r, column=c, padx=5, pady=5)
        row_buttons.append(btn)
    buttons.append(row_buttons)

for i in buttons[0]:
    i.config(text = "X")

for i in buttons[2]:
    i.config(text = "Y")

print(buttons)

root.mainloop()