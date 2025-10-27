import tkinter as tk
from tkinter import messagebox

# ---------------- Data Structures ----------------
class Stack:
    def __init__(self):
        self.items = []
    def push(self, item):
        self.items.append(item)
    def pop(self):
        return self.items.pop() if not self.is_empty() else None
    def peek(self):
        return self.items[-1] if not self.is_empty() else None
    def is_empty(self):
        return len(self.items) == 0
    def __iter__(self):
        return iter(self.items[::-1])  # top to bottom

class Queue:
    def __init__(self):
        self.items = []
    def enqueue(self, item):
        self.items.append(item)
    def dequeue(self):
        return self.items.pop(0) if not self.is_empty() else None
    def remove(self, roll_no):
        for i, student in enumerate(self.items):
            if student[0] == roll_no:
                return self.items.pop(i)
        return None
    def is_empty(self):
        return len(self.items) == 0
    def __iter__(self):
        return iter(self.items)

# ---------------- Searching & Sorting ----------------
def linear_search(data, target_roll):
    for i, student in enumerate(data):
        if student[0] == target_roll:
            return i
    return -1

def bubble_sort(data, key="name"):
    arr = data[:]
    n = len(arr)
    for i in range(n-1):
        for j in range(n-i-1):
            if key == "name":
                if arr[j][1].lower() > arr[j+1][1].lower():
                    arr[j], arr[j+1] = arr[j+1], arr[j]
            elif key == "roll":
                if arr[j][0] > arr[j+1][0]:
                    arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

# ---------------- GUI Application ----------------
class ExamPortalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Exam Registration Portal (Stack + Queue)")

        # Data Structures
        self.registered = Queue()   # Students currently registered
        self.withdrawn = Stack()    # Recently withdrawn students

        # -------- Widgets --------
        # Registration Section
        tk.Label(root, text="Enter Roll No:").pack()
        self.roll_entry = tk.Entry(root, width=40)
        self.roll_entry.pack(pady=2)

        tk.Label(root, text="Enter Student Name:").pack()
        self.name_entry = tk.Entry(root, width=40)
        self.name_entry.pack(pady=2)

        tk.Button(root, text="Register Student", command=self.register_student).pack(pady=3)
        tk.Button(root, text="Withdraw by Roll No", command=self.withdraw_student).pack(pady=3)
        tk.Button(root, text="Re-Register Last Withdrawn", command=self.reregister_student).pack(pady=3)

        # Searching Section
        tk.Label(root, text="Search by Roll No:").pack()
        self.search_entry = tk.Entry(root, width=40)
        self.search_entry.pack(pady=2)
        tk.Button(root, text="Search", command=self.search_student).pack(pady=3)

        # Sorting Section
        tk.Button(root, text="Sort by Name", command=lambda: self.sort_students("name")).pack(pady=2)
        tk.Button(root, text="Sort by Roll No", command=lambda: self.sort_students("roll")).pack(pady=2)

        # Peek last withdrawn
        tk.Button(root, text="Show Last Withdrawn", command=self.show_last_withdrawn).pack(pady=3)

        # Labels
        self.registered_label = tk.Label(root, text="Registered Students: Empty", font=("Arial", 10))
        self.registered_label.pack(pady=5)

        self.withdrawn_label = tk.Label(root, text="Withdrawn Students: Empty", font=("Arial", 10))
        self.withdrawn_label.pack(pady=5)

        self.stats_label = tk.Label(root, text="Total Registered: 0 | Withdrawn: 0", font=("Arial", 10))
        self.stats_label.pack(pady=5)

    # -------- Functions --------
    def refresh_display(self):
        reg = list(self.registered)
        self.registered_label.config(
            text=f"Registered Students: {reg if reg else 'Empty'}"
        )

        wd = list(self.withdrawn)
        self.withdrawn_label.config(
            text=f"Withdrawn Students: {wd if wd else 'Empty'}"
        )

        self.stats_label.config(
            text=f"Total Registered: {len(reg)} | Withdrawn: {len(wd)}"
        )

    def register_student(self):
        roll = self.roll_entry.get().strip()
        name = self.name_entry.get().strip()
        if roll and name:
            self.registered.enqueue((roll, name))
            self.roll_entry.delete(0, tk.END)
            self.name_entry.delete(0, tk.END)
            self.refresh_display()
        else:
            messagebox.showwarning("Input Error", "Enter Roll No and Name.")

    def withdraw_student(self):
        roll = self.roll_entry.get().strip()
        if not roll:
            messagebox.showwarning("Input Error", "Enter Roll No to withdraw.")
            return
        student = self.registered.remove(roll)
        if student:
            self.withdrawn.push(student)
            messagebox.showinfo("Withdrawn", f"Student {student} withdrawn successfully.")
        else:
            messagebox.showinfo("Withdrawn", f"No student with Roll No {roll} found.")
        self.refresh_display()

    def reregister_student(self):
        student = self.withdrawn.pop()
        if student:
            self.registered.enqueue(student)
            messagebox.showinfo("Re-Registered", f"Student {student} added back.")
        else:
            messagebox.showinfo("Re-Registered", "No withdrawn students available.")
        self.refresh_display()

    def search_student(self):
        roll = self.search_entry.get().strip()
        reg = list(self.registered)
        pos = linear_search(reg, roll)
        if pos != -1:
            messagebox.showinfo("Search Result", f"Student {reg[pos]} is registered (Position {pos+1})")
        else:
            messagebox.showinfo("Search Result", f"Roll No {roll} not found in registered list.")

    def sort_students(self, key):
        reg = list(self.registered)
        sorted_list = bubble_sort(reg, key)
        self.registered_label.config(
            text=f"Registered Students (Sorted by {key}): {sorted_list if sorted_list else 'Empty'}"
        )

    def show_last_withdrawn(self):
        student = self.withdrawn.peek()
        if student:
            messagebox.showinfo("Last Withdrawn", f"Most recent withdrawn student: {student}")
        else:
            messagebox.showinfo("Last Withdrawn", "No withdrawn students.")

# ---------------- Run App ----------------
if __name__ == "__main__":
    root = tk.Tk()
    app = ExamPortalApp(root)
    root.mainloop()
