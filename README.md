Task Manager 📝

A modern desktop Task Manager application built with Python and CustomTkinter.
Designed to help you organize and manage your daily tasks efficiently with a
clean, responsive interface.

Features

✅ Add and manage daily tasks
🗑️ Delete individual tasks or clear all completed at once
⭐ Set task priority — High, Medium, or Low with color coding
🔍 Search and filter tasks in real time
🌙 Toggle between Dark and Light mode
💾 Persistent storage — tasks are saved automatically and reload on startup

Technologies Used

TechnologyPurposePython 3.12Core languageCustomTkinterModern GUI frameworkJSON / File HandlingLocal data persistenceObject-Oriented ProgrammingApp architecture

How to Run


Clone the repository


bash   git clone https://github.com/YOUR_USERNAME/task-manager.git
   cd task-manager


Create and activate a virtual environment


bash   python -m venv venv

   # Windows
   venv\Scripts\activate

   # Mac / Linux
   source venv/bin/activate


Install dependencies


bash   pip install customtkinter


Run the app


bash   python main.py

Project Structure

task-manager/
├── main.py        ← all application code
├── tasks.json     ← auto-created when you add your first task
└── README.md

What I Learned


Building desktop GUIs with Python and CustomTkinter
Structuring a project using Object-Oriented Programming
Saving and loading data using JSON file handling
Real-time search and filtering logic
Virtual environments and dependency management


Future Improvements


 Due dates with overdue highlighting
 SQLite database instead of JSON
 Sort tasks by priority or date
 System tray notifications
