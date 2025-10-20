"""
GWC STUDY PLANNER - Python
A comprehensive study planning tool for Girls Who Code students
"""

import json
import os
from datetime import datetime, timedelta

class StudyPlanner:
    def __init__(self, filename="study_plan.json"):
        self.filename = filename
        self.tasks = self.load_tasks()
        self.subjects = self.load_subjects()
    
    def load_tasks(self):
        """Load study tasks from JSON file"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    data = json.load(f)
                    return data.get('tasks', [])
            except:
                return []
        return []
    
    def load_subjects(self):
        """Load subjects from JSON file"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    data = json.load(f)
                    return data.get('subjects', [])
            except:
                return []
        return []
    
    def save_data(self):
        """Save tasks and subjects to JSON file"""
        data = {
            'tasks': self.tasks,
            'subjects': self.subjects
        }
        with open(self.filename, 'w') as f:
            json.dump(data, f, indent=2)
    
    def add_subject(self, name, teacher="", priority="Medium"):
        """Add a new subject"""
        subject = {
            "id": len(self.subjects) + 1,
            "name": name,
            "teacher": teacher,
            "priority": priority,
            "created_date": datetime.now().strftime("%Y-%m-%d")
        }
        self.subjects.append(subject)
        self.save_data()
        print(f"✅ Subject '{name}' added successfully!")
    
    def add_task(self, subject_name, task_name, due_date, difficulty="Medium", completed=False):
        """Add a new study task"""
        task = {
            "id": len(self.tasks) + 1,
            "subject": subject_name,
            "task": task_name,
            "due_date": due_date,
            "difficulty": difficulty,
            "completed": completed,
            "created_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.tasks.append(task)
        self.save_data()
        print(f"✅ Task '{task_name}' added successfully!")
    
    def view_all_tasks(self):
        """View all study tasks"""
        if not self.tasks:
            print("❌ No tasks found!")
            return
        
        print("\n" + "=" * 80)
        print("📚 ALL STUDY TASKS")
        print("=" * 80)
        
        for i, task in enumerate(self.tasks, 1):
            status = "✅ Done" if task['completed'] else "⏳ Pending"
            difficulty_emoji = "🟢" if task['difficulty'] == "Easy" else "🟡" if task['difficulty'] == "Medium" else "🔴"
            print(f"{i}. [{status}] {task['task']}")
            print(f"   Subject: {task['subject']} | Due: {task['due_date']} | Difficulty: {difficulty_emoji} {task['difficulty']}")
        print("=" * 80 + "\n")
    
    def view_tasks_by_subject(self, subject_name):
        """View tasks for a specific subject"""
        subject_tasks = [t for t in self.tasks if t['subject'].lower() == subject_name.lower()]
        
        if not subject_tasks:
            print(f"❌ No tasks found for '{subject_name}'!")
            return
        
        print("\n" + "=" * 80)
        print(f"📖 TASKS FOR {subject_name.upper()}")
        print("=" * 80)
        
        for i, task in enumerate(subject_tasks, 1):
            status = "✅ Done" if task['completed'] else "⏳ Pending"
            print(f"{i}. [{status}] {task['task']}")
            print(f"   Due: {task['due_date']} | Difficulty: {task['difficulty']}")
        print("=" * 80 + "\n")
    
    def view_subjects(self):
        """View all subjects"""
        if not self.subjects:
            print("❌ No subjects found!")
            return
        
        print("\n" + "=" * 80)
        print("🎓 ALL SUBJECTS")
        print("=" * 80)
        
        for i, subject in enumerate(self.subjects, 1):
            priority_emoji = "🔴" if subject['priority'] == "High" else "🟡" if subject['priority'] == "Medium" else "🟢"
            print(f"{i}. {subject['name']}")
            print(f"   Teacher: {subject['teacher']} | Priority: {priority_emoji} {subject['priority']}")
        print("=" * 80 + "\n")
    
    def mark_task_complete(self, task_id):
        """Mark a task as completed"""
        for task in self.tasks:
            if task['id'] == task_id:
                task['completed'] = True
                self.save_data()
                print(f"✅ Task marked as complete!")
                return True
        print("❌ Task not found!")
        return False
    
    def get_pending_tasks(self):
        """Get all pending tasks"""
        pending = [t for t in self.tasks if not t['completed']]
        
        if not pending:
            print("🎉 No pending tasks! You're all caught up!")
            return
        
        print("\n" + "=" * 80)
        print("⏳ PENDING TASKS")
        print("=" * 80)
        
        for i, task in enumerate(pending, 1):
            difficulty_emoji = "🟢" if task['difficulty'] == "Easy" else "🟡" if task['difficulty'] == "Medium" else "🔴"
            print(f"{i}. {task['task']}")
            print(f"   Subject: {task['subject']} | Due: {task['due_date']} | {difficulty_emoji} {task['difficulty']}")
        print("=" * 80 + "\n")
    
    def get_due_soon_tasks(self, days=3):
        """Get tasks due within specified days"""
        today = datetime.now().date()
        due_soon = []
        
        for task in self.tasks:
            if not task['completed']:
                try:
                    due_date = datetime.strptime(task['due_date'], "%Y-%m-%d").date()
                    days_left = (due_date - today).days
                    if 0 <= days_left <= days:
                        due_soon.append((task, days_left))
                except:
                    pass
        
        if not due_soon:
            print(f"✅ No tasks due in the next {days} days!")
            return
        
        print("\n" + "=" * 80)
        print(f"⏰ TASKS DUE IN THE NEXT {days} DAYS")
        print("=" * 80)
        
        due_soon.sort(key=lambda x: x[1])
        for task, days_left in due_soon:
            if days_left == 0:
                due_text = "🔴 DUE TODAY"
            else:
                due_text = f"🟡 Due in {days_left} day(s)"
            print(f"• {task['task']} ({task['subject']}) - {due_text}")
        print("=" * 80 + "\n")
    
    def delete_task(self, task_id):
        """Delete a task"""
        for i, task in enumerate(self.tasks):
            if task['id'] == task_id:
                self.tasks.pop(i)
                self.save_data()
                print("✅ Task deleted!")
                return True
        print("❌ Task not found!")
        return False
    
    def get_study_stats(self):
        """Get study statistics"""
        total_tasks = len(self.tasks)
        completed_tasks = len([t for t in self.tasks if t['completed']])
        pending_tasks = total_tasks - completed_tasks
        
        print("\n" + "=" * 80)
        print("📊 STUDY STATISTICS")
        print("=" * 80)
        print(f"Total Tasks: {total_tasks}")
        print(f"✅ Completed: {completed_tasks}")
        print(f"⏳ Pending: {pending_tasks}")
        if total_tasks > 0:
            completion_rate = (completed_tasks / total_tasks) * 100
            print(f"📈 Completion Rate: {completion_rate:.1f}%")
        print(f"📚 Total Subjects: {len(self.subjects)}")
        print("=" * 80 + "\n")

def main():
    """Main application loop"""
    planner = StudyPlanner()
    
    print("=" * 80)
    print("🎓 WELCOME TO GWC STUDY PLANNER")
    print("=" * 80)
    print("Empowering Girls Who Code to reach their goals!\n")
    
    while True:
        print("📋 MAIN MENU:")
        print("1. Add Subject")
        print("2. Add Study Task")
        print("3. View All Tasks")
        print("4. View Tasks by Subject")
        print("5. View Subjects")
        print("6. View Pending Tasks")
        print("7. View Tasks Due Soon")
        print("8. Mark Task as Complete")
        print("9. Delete Task")
        print("10. Study Statistics")
        print("11. Exit")
        
        choice = input("\nEnter your choice (1-11): ").strip()
        
        if choice == '1':
            print("\n➕ ADD NEW SUBJECT")
            name = input("Subject name: ").strip()
            teacher = input("Teacher name (optional): ").strip()
            print("Priority: 1.High  2.Medium  3.Low")
            priority_choice = input("Choose priority (1-3): ").strip()
            priority_map = {'1': 'High', '2': 'Medium', '3': 'Low'}
            priority = priority_map.get(priority_choice, 'Medium')
            planner.add_subject(name, teacher, priority)
        
        elif choice == '2':
            print("\n➕ ADD NEW STUDY TASK")
            subject = input("Subject name: ").strip()
            task = input("Task description: ").strip()
            due_date = input("Due date (YYYY-MM-DD): ").strip()
            print("Difficulty: 1.Easy  2.Medium  3.Hard")
            diff_choice = input("Choose difficulty (1-3): ").strip()
            difficulty_map = {'1': 'Easy', '2': 'Medium', '3': 'Hard'}
            difficulty = difficulty_map.get(diff_choice, 'Medium')
            planner.add_task(subject, task, due_date, difficulty)
        
        elif choice == '3':
            planner.view_all_tasks()
        
        elif choice == '4':
            subject_name = input("Enter subject name: ").strip()
            planner.view_tasks_by_subject(subject_name)
        
        elif choice == '5':
            planner.view_subjects()
        
        elif choice == '6':
            planner.get_pending_tasks()
        
        elif choice == '7':
            days = input("Check tasks due in how many days? (default: 3): ").strip()
            days = int(days) if days.isdigit() else 3
            planner.get_due_soon_tasks(days)
        
        elif choice == '8':
            task_id = input("Enter task ID to mark complete: ").strip()
            if task_id.isdigit():
                planner.mark_task_complete(int(task_id))
        
        elif choice == '9':
            task_id = input("Enter task ID to delete: ").strip()
            if task_id.isdigit():
                confirm = input("Are you sure? (yes/no): ").strip().lower()
                if confirm == 'yes':
                    planner.delete_task(int(task_id))
        
        elif choice == '10':
            planner.get_study_stats()
        
        elif choice == '11':
            print("\n🌟 Keep coding and stay awesome! Goodbye! 👋")
            break
        
        else:
            print("❌ Invalid choice! Please try again.")

if __name__ == "__main__":
    main()