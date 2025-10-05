import tkinter as tk
from tkinter import ttk, messagebox

# === MENU STOCK ===
stock = {
    "Cheese Burger": 10.00,
    "Delux Bacon": 13.00,
    "Soda": 2.00,
    "Andy Style Fries": 7.40
}

tax_rate = 0.08  # 8%

# === MAIN APP ===
root = tk.Tk()
root.title("Andy's Burger POS System")
root.geometry("680x650")
root.config(bg="#2B2B2B")

cart = {}

# --- COLOR PALETTE ---
ACCENT = "#FF6F3C"
TEXT_COLOR = "#F5F5F5"
PANEL_BG = "#3C3C3C"
HIGHLIGHT = "#FFD166"

# --- HEADER ---
header = tk.Label(root, text="🍔 Andy's Burger POS System",
                  font=("Helvetica", 22, "bold"), bg="#2B2B2B", fg=ACCENT)
header.pack(pady=10)

# --- FRAME: MENU ---
menu_frame = tk.Frame(root, bg=PANEL_BG, bd=2, relief="ridge")
menu_frame.pack(pady=10, padx=20, fill="x")

tk.Label(menu_frame, text="Menu",
         font=("Helvetica", 16, "bold"), bg=PANEL_BG, fg=TEXT_COLOR).grid(row=0, column=0, columnspan=4, pady=5)

row = 1
for item, price in stock.items():
    tk.Label(menu_frame, text=f"{item} - ${price:.2f}",
             font=("Helvetica", 12), bg=PANEL_BG, fg=TEXT_COLOR).grid(row=row, column=0, sticky="w", padx=10, pady=5)

    qty_var = tk.IntVar(value=1)
    qty_spin = tk.Spinbox(menu_frame, from_=1, to=10, width=5, textvariable=qty_var,
                          font=("Helvetica", 11), justify="center")
    qty_spin.grid(row=row, column=1, padx=5)

    def make_add_func(item=item, qty_var=qty_var):
        return lambda: add_to_cart(item, qty_var.get())

    add_btn = tk.Button(menu_frame, text="Add", bg=ACCENT, fg="white",
                        font=("Helvetica", 10, "bold"), width=8,
                        activebackground="#FF8C5A", activeforeground="white",
                        command=make_add_func())
    add_btn.grid(row=row, column=2, padx=10, pady=2)

    row += 1

# --- FRAME: CART DISPLAY ---
cart_frame = tk.Frame(root, bg=PANEL_BG, bd=2, relief="ridge")
cart_frame.pack(pady=10, padx=20, fill="x")

tk.Label(cart_frame, text="🛒 Current Cart",
         font=("Helvetica", 14, "bold"), bg=PANEL_BG, fg=TEXT_COLOR).pack(pady=5)

cart_list = tk.Listbox(cart_frame, font=("Helvetica", 12), height=8,
                       bg="#F8F8F8", fg="#222", relief="flat")
cart_list.pack(padx=10, pady=5, fill="x")

# --- FRAME: TOTALS ---
total_frame = tk.Frame(root, bg="#2B2B2B")
total_frame.pack(pady=5)

subtotal_label = tk.Label(total_frame, text="Subtotal: $0.00",
                          font=("Helvetica", 12, "bold"), bg="#2B2B2B", fg=TEXT_COLOR)
subtotal_label.grid(row=0, column=0, padx=10, sticky="w")

tax_label = tk.Label(total_frame, text="Tax (8%): $0.00",
                     font=("Helvetica", 12, "bold"), bg="#2B2B2B", fg=TEXT_COLOR)
tax_label.grid(row=1, column=0, padx=10, sticky="w")

total_label = tk.Label(total_frame, text="Total: $0.00",
                       font=("Helvetica", 14, "bold"), fg=HIGHLIGHT, bg="#2B2B2B")
total_label.grid(row=2, column=0, padx=10, sticky="w", pady=5)

# --- FRAME: PAYMENT (cleaner design) ---
payment_frame = tk.LabelFrame(root, text="Payment", font=("Helvetica", 14, "bold"),
                              fg=ACCENT, bg=PANEL_BG, bd=2, relief="ridge", labelanchor="n")
payment_frame.pack(pady=15, padx=20, fill="x")

tk.Label(payment_frame, text="Method:", font=("Helvetica", 12), bg=PANEL_BG,
         fg=TEXT_COLOR).grid(row=0, column=0, padx=10, pady=8, sticky="e")

payment_method = ttk.Combobox(
    payment_frame, values=["Cash", "Card"], state="readonly", width=12)
payment_method.grid(row=0, column=1, padx=5)
payment_method.current(0)

tk.Label(payment_frame, text="Cash Given:", font=("Helvetica", 12), bg=PANEL_BG,
         fg=TEXT_COLOR).grid(row=1, column=0, padx=10, pady=8, sticky="e")
cash_entry = tk.Entry(payment_frame, width=12, font=("Helvetica", 11))
cash_entry.grid(row=1, column=1, padx=5)

# --- FUNCTIONS ---


def add_to_cart(item, qty):
    qty = int(qty)
    if item in cart:
        cart[item] += qty
    else:
        cart[item] = qty
    update_cart()


def update_cart():
    cart_list.delete(0, tk.END)
    subtotal = 0
    for item, qty in cart.items():
        price = stock[item] * qty
        subtotal += price
        cart_list.insert(tk.END, f"{item} x{qty} - ${price:.2f}")

    tax = subtotal * tax_rate
    total = subtotal + tax
    subtotal_label.config(text=f"Subtotal: ${subtotal:.2f}")
    tax_label.config(text=f"Tax (8%): ${tax:.2f}")
    total_label.config(text=f"Total: ${total:.2f}")


def process_payment():
    total = float(total_label.cget("text").split("$")[1])
    method = payment_method.get()

    if not cart:
        messagebox.showwarning("Empty Cart", "Please add items before paying.")
        return

    change = 0
    if method == "Cash":
        try:
            cash = float(cash_entry.get())
            if cash < total:
                messagebox.showerror("Insufficient Funds",
                                     "Cash provided is less than total.")
                return
            change = cash - total
            show_receipt(method, change)
        except ValueError:
            messagebox.showerror(
                "Invalid Input", "Please enter a valid cash amount.")
            return
    else:
        show_receipt(method, change=0)

    # Clear cart after payment
    cart.clear()
    update_cart()
    cash_entry.delete(0, tk.END)


def show_receipt(method, change):
    """Display a receipt popup after payment"""
    receipt = tk.Toplevel(root)
    receipt.title("Receipt - Andy's Burger POS")
    receipt.geometry("400x500")
    receipt.config(bg="white")

    tk.Label(receipt, text="Andy's Burger", font=(
        "Helvetica", 18, "bold"), bg="white", fg="#333").pack(pady=10)
    tk.Label(receipt, text="Customer Receipt", font=(
        "Helvetica", 12), bg="white", fg="#333").pack()

    receipt_box = tk.Text(receipt, width=45, height=20, font=(
        "Courier", 10), bg="#f7f7f7", relief="flat")
    receipt_box.pack(pady=10, padx=10)

    subtotal = sum(stock[item] * qty for item, qty in cart.items())
    tax = subtotal * tax_rate
    total = subtotal + tax

    for item, qty in cart.items():
        line = f"{item:<20} x{qty:<3} ${stock[item] * qty:>6.2f}\n"
        receipt_box.insert(tk.END, line)

    receipt_box.insert(tk.END, "\n-----------------------------\n")
    receipt_box.insert(tk.END, f"Subtotal:        ${subtotal:>6.2f}\n")
    receipt_box.insert(tk.END, f"Tax (8%):        ${tax:>6.2f}\n")
    receipt_box.insert(tk.END, f"Total:           ${total:>6.2f}\n")
    receipt_box.insert(tk.END, f"Payment:         {method}\n")
    if method == "Cash":
        receipt_box.insert(tk.END, f"Change:          ${change:>6.2f}\n")

    receipt_box.insert(
        tk.END, "\nThank you for dining with us!\n🍔 Come again soon! 🍟")
    receipt_box.config(state="disabled")

    tk.Button(receipt, text="Close Receipt", bg=ACCENT, fg="white", font=("Helvetica", 11, "bold"),
              command=receipt.destroy).pack(pady=10)


# --- PAY BUTTON ---
checkout_btn = tk.Button(root, text="💵 Checkout & Print Receipt", bg=ACCENT, fg="white",
                         font=("Helvetica", 14, "bold"), width=25, height=1,
                         activebackground="#FF8C5A", activeforeground="white",
                         command=process_payment)
checkout_btn.pack(pady=15)

root.mainloop()
