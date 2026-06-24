import json
import os
import customtkinter as ctk


TASKS_FILE = "tasks.json"

PRIORITY_COLORS = {
    "High":   ("#ffcccc", "#7f1f1f"),
    "Medium": ("#fff3cc", "#7f5f00"),
    "Low":    ("#ccffcc", "#1f5f1f"),
}


class Task:
    def __init__(self, title, done=False, priority="Medium"):
        self.title = title
        self.done = done
        self.priority = priority

    def to_dict(self):
        return {"title": self.title, "done": self.done, "priority": self.priority}


def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump([t.to_dict() for t in tasks], f, indent=2)


def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, "r") as f:
        data = json.load(f)
        return [Task(**d) for d in data]


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Task Manager")
        self.geometry("580x650")
        self.minsize(450, 450)
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        self.tasks = load_tasks()
        self.current_mode = "System"

        self._build_topbar()
        self._build_header()
        self._build_search()
        self._build_task_list()
        self._build_footer()
        self.refresh()

    def _build_topbar(self):
        bar = ctk.CTkFrame(self, fg_color="transparent")
        bar.pack(fill="x", padx=20, pady=(15, 0))

        ctk.CTkLabel(
            bar, text="Task Manager",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(side="left")

        self.mode_btn = ctk.CTkButton(
            bar, text="Dark Mode", width=110, height=32,
            command=self.toggle_mode
        )
        self.mode_btn.pack(side="right")

    def _build_header(self):
        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.pack(fill="x", padx=20, pady=(12, 5))

        self.entry = ctk.CTkEntry(
            frame, placeholder_text="Add a new task...",
            height=40, font=ctk.CTkFont(size=14)
        )
        self.entry.pack(side="left", fill="x", expand=True, padx=(0, 8))
        self.entry.bind("<Return>", lambda e: self.add_task())

        self.priority_var = ctk.StringVar(value="Medium")
        self.priority_menu = ctk.CTkOptionMenu(
            frame,
            values=["High", "Medium", "Low"],
            variable=self.priority_var,
            width=100, height=40
        )
        self.priority_menu.pack(side="left", padx=(0, 8))

        ctk.CTkButton(
            frame, text="Add", width=75, height=40,
            command=self.add_task
        ).pack(side="left")

    def _build_search(self):
        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.pack(fill="x", padx=20, pady=(0, 8))

        ctk.CTkLabel(
            frame, text="🔍  Search",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        ).pack(anchor="w", pady=(0, 3))

        self.search_var = ctk.StringVar()
        self.search_var.trace_add("write", lambda *a: self.refresh())

        ctk.CTkEntry(
            frame,
            placeholder_text="Type to filter tasks...",
            textvariable=self.search_var,
            height=36,
            font=ctk.CTkFont(size=13)
        ).pack(fill="x")

    def _build_task_list(self):
        self.scroll_frame = ctk.CTkScrollableFrame(
            self, label_text="Tasks"
        )
        self.scroll_frame.pack(fill="both", expand=True, padx=20, pady=5)

    def _build_footer(self):
        footer = ctk.CTkFrame(self, fg_color="transparent")
        footer.pack(fill="x", padx=20, pady=(5, 15))

        self.status_label = ctk.CTkLabel(
            footer, text="",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        self.status_label.pack(side="left")

        ctk.CTkButton(
            footer, text="Clear completed",
            width=140, height=30,
            fg_color="transparent",
            border_width=1,
            text_color=("gray40", "gray60"),
            command=self.clear_completed
        ).pack(side="right")

    def add_task(self):
        title = self.entry.get().strip()
        if not title:
            return
        self.tasks.append(Task(title, priority=self.priority_var.get()))
        save_tasks(self.tasks)
        self.entry.delete(0, "end")
        self.refresh()

    def delete_task(self, index):
        self.tasks.pop(index)
        save_tasks(self.tasks)
        self.refresh()

    def toggle_done(self, index):
        self.tasks[index].done = not self.tasks[index].done
        save_tasks(self.tasks)
        self.refresh()

    def clear_completed(self):
        self.tasks = [t for t in self.tasks if not t.done]
        save_tasks(self.tasks)
        self.refresh()

    def toggle_mode(self):
        if self.current_mode in ("System", "Light"):
            self.current_mode = "Dark"
            ctk.set_appearance_mode("Dark")
            self.mode_btn.configure(text="Light Mode")
        else:
            self.current_mode = "Light"
            ctk.set_appearance_mode("Light")
            self.mode_btn.configure(text="Dark Mode")

    def refresh(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        query = self.search_var.get().lower()
        visible = [
            (i, t) for i, t in enumerate(self.tasks)
            if query in t.title.lower()
        ]

        for i, task in visible:
            light_color, dark_color = PRIORITY_COLORS[task.priority]

            row = ctk.CTkFrame(
                self.scroll_frame,
                fg_color=(light_color, dark_color),
                corner_radius=8
            )
            row.pack(fill="x", pady=3, padx=2)

            cb_var = ctk.BooleanVar(value=task.done)
            ctk.CTkCheckBox(
                row, text=task.title,
                variable=cb_var,
                command=lambda idx=i: self.toggle_done(idx),
                font=ctk.CTkFont(size=14, overstrike=task.done)
            ).pack(side="left", padx=10, pady=8)

            ctk.CTkLabel(
                row, text=task.priority,
                font=ctk.CTkFont(size=11),
                text_color="gray"
            ).pack(side="left", padx=4)

            ctk.CTkButton(
                row, text="Delete", width=70, height=28,
                fg_color="transparent",
                border_width=1,
                text_color=("gray40", "gray60"),
                command=lambda idx=i: self.delete_task(idx)
            ).pack(side="right", padx=8, pady=8)

        done_count = sum(1 for t in self.tasks if t.done)
        total = len(self.tasks)
        self.status_label.configure(
            text=f"{done_count} of {total} tasks completed"
        )


if __name__ == "__main__":
    app = App()
    app.mainloop()
