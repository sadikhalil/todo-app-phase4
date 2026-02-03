"""Todo App - Python Console Application."""

from app.agents.main import agent_handler


def display_menu():
    """Display the main menu."""
    print("\n" + "=" * 50)
    print("           TODO APP - Main Menu")
    print("=" * 50)
    print("1. Add Task")
    print("2. View All Tasks")
    print("3. Update Task")
    print("4. Delete Task")
    print("5. Mark Task Complete")
    print("6. Exit")
    print("=" * 50)


def display_tasks(tasks):
    """Display tasks with status indicators."""
    if not tasks:
        print("\nNo tasks found.")
        return

    print("\n" + "-" * 70)
    print("Your Tasks:")
    print("-" * 70)

    for task in tasks:
        # Status indicator
        if task["completed"]:
            status = "[✓ DONE]"
        else:
            status = "[PENDING]"

        print(f"\n{status} {task['title']}")
        print(f"   ID: {task['id']}")
        print(f"   Due: {task['date']}")
        if task["note"]:
            print(f"   Description: {task['note']}")

    print("-" * 70)


def add_task():
    """Handle adding a new task with title and description."""
    print("\n--- Add New Task ---")

    # Title is required
    while True:
        title = input("Task title (required): ").strip()
        if title:
            break
        print("Task title cannot be empty!")

    # Date is required
    while True:
        date = input("Due date (required, e.g., 2025-01-15): ").strip()
        if date:
            break
        print("Due date is required! Please enter a date.")

    # Description is optional
    description = input("Task description (optional, press Enter to skip): ").strip() or None

    result = agent_handler.add_task(title, date, description, "console_user")
    print(f"\n{result['message']}")


def view_tasks():
    """Handle viewing all tasks."""
    print("\n--- View All Tasks ---")

    result = agent_handler.view_tasks(user_id="console_user")
    display_tasks(result["tasks"])


def update_task():
    """Handle updating task details by ID."""
    print("\n--- Update Task by ID ---")

    # Show all tasks first
    result = agent_handler.view_tasks(user_id="console_user")
    display_tasks(result["tasks"])

    if not result["tasks"]:
        return

    # Ask for task ID
    task_id = input("\nEnter Task ID to update (or 'cancel' to go back): ").strip()

    if task_id.lower() == 'cancel':
        print("Update cancelled.")
        return

    # Get the task details
    task_result = agent_handler.view_tasks(task_id=task_id, user_id="console_user")

    if not task_result["success"]:
        print(f"\n{task_result['message']}")
        return

    task = task_result["task"]
    print(f"\nUpdating: {task['title']}")
    print("(Press Enter to keep current value)")

    new_title = input(f"New title [{task['title']}]: ").strip() or None

    # Date is required - must enter a new date or keep current
    while True:
        new_date = input(f"New date [{task['date']}] (required): ").strip()
        if new_date:
            break
        if task['date']:
            new_date = task['date']
            break
        print("Due date is required! Please enter a date.")

    new_description = input(f"New description [{task['note'] or 'None'}]: ").strip()
    if new_description == "":
        new_description = None

    if not new_title and new_date == task['date'] and new_description is None:
        print("No changes made.")
        return

    result = agent_handler.update_task(task_id, new_title, new_date, new_description, user_id="console_user")
    print(f"\n{result['message']}")


def delete_task():
    """Handle deleting a task by ID."""
    print("\n--- Delete Task by ID ---")

    # Show all tasks first
    result = agent_handler.view_tasks(user_id="console_user")
    display_tasks(result["tasks"])

    if not result["tasks"]:
        return

    # Ask for task ID
    task_id = input("\nEnter Task ID to delete (or 'cancel' to go back): ").strip()

    if task_id.lower() == 'cancel':
        print("Deletion cancelled.")
        return

    # Confirmation from delete agent
    confirm_result = agent_handler.delete_task(task_id, confirmed=False, user_id="console_user")

    if not confirm_result["success"]:
        print(f"\n{confirm_result['message']}")
        return

    print(f"\n{confirm_result['message']}")
    confirm = input("Type 'yes' to confirm deletion: ").strip().lower()

    if confirm == "yes":
        result = agent_handler.delete_task(task_id, confirmed=True, user_id="console_user")
        print(f"\n{result['message']}")
    else:
        print("Deletion cancelled.")


def mark_complete():
    """Handle marking a task as complete/incomplete by ID."""
    print("\n--- Mark Task Complete/Incomplete ---")

    # Show all tasks first
    result = agent_handler.view_tasks(user_id="console_user")
    display_tasks(result["tasks"])

    if not result["tasks"]:
        return

    # Ask for task ID
    task_id = input("\nEnter Task ID to toggle complete/incomplete (or 'cancel' to go back): ").strip()

    if task_id.lower() == 'cancel':
        print("Operation cancelled.")
        return

    # Toggle the task status
    result = agent_handler.toggle_complete(task_id, user_id="console_user")
    print(f"\n{result['message']}")


def main():
    """Main application loop."""
    print("\n" + "=" * 50)
    print("    Welcome to Todo App!")
    print("=" * 50)

    while True:
        display_menu()
        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":
            add_task()
        elif choice == "2":
            view_tasks()
        elif choice == "3":
            update_task()
        elif choice == "4":
            delete_task()
        elif choice == "5":
            mark_complete()
        elif choice == "6":
            print("\nGoodbye! Your tasks are saved in memory.")
            break
        else:
            print("\nInvalid choice. Please enter 1-6.")


if __name__ == "__main__":
    main()
