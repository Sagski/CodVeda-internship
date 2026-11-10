# -- TO-DO LIST APPLICATION --

import json  #by importing json, im allowed go read/write JSON files

FILE = 'tasks.json'  # the file where tasks are saved


# ── FILE HELPERS ──────────────────────────────────────────────────────────────

def load_tasks():
    # Try to open the file and read the tasks inside it.
    # If the file doesn't exist yet, return an empty list instead of crashing.
    try:
        file = open(FILE, 'r')
        tasks = json.load(file)  # reads the JSON and converts it to a Python list
        file.close()
        return tasks
    except FileNotFoundError:
        return []  # no file yet — start with zero tasks


def save_tasks(tasks):
    # Write the current list of tasks back to the file.
    # json.dump converts the Python list into JSON text and writes it.
    # indent=2 makes the file readable (each item on its own line).
    file = open(FILE, 'w')
    json.dump(tasks, file, indent=2)
    file.close()


# ── ACTIONS ───────────────────────────────────────────────────────────────────

def add_task(tasks):
    name = input('Enter task name: ')
    # Each task is a dictionary with two keys: 'name' and 'done'
    tasks.append({'name': name, 'done': False})
    save_tasks(tasks)
    print(f'Task "{name}" added.')


def list_tasks(tasks):
    if len(tasks) == 0:
        print('No tasks yet.')
        return  # exit the function early — nothing to show

    print('\nYour tasks:')
    for i in range(len(tasks)):
        task = tasks[i]
        # Show a tick if done, an empty box if not
        status = '✓' if task['done'] else '✕'
        # i+1 so numbering starts at 1 (not 0) for the user
        print(f'  {i+1}. [{status}] {task["name"]}')
    print()


def mark_done(tasks):
    list_tasks(tasks)
    if len(tasks) == 0:
        return

    try:
        number = int(input('Enter task number to mark as done: '))
        # The user types 1, 2, 3... but the list index starts at 0, so subtract 1
        index = number - 1

        if index < 0 or index >= len(tasks):
            print('Error: that task number does not exist.')
            return

        tasks[index]['done'] = True
        save_tasks(tasks)
        print(f'Task "{tasks[index]["name"]}" marked as done.')

    except ValueError:
        # int() failed because the user typed something that isn't a number
        print('Error: please enter a valid number.')


def delete_task(tasks):
    list_tasks(tasks)
    if len(tasks) == 0:
        return

    try:
        number = int(input('Enter task number to delete: '))
        index = number - 1

        if index < 0 or index >= len(tasks):
            print('Error: that task number does not exist.')
            return

        # pop() removes the item at that index and returns it so we can show its name
        removed = tasks.pop(index)
        save_tasks(tasks)
        print(f'Task "{removed["name"]}" deleted.')

    except ValueError:
        print('Error: please enter a valid number.')


# ── MAIN LOOP ─────────────────────────────────────────────────────────────────

def main():
    tasks = load_tasks()  # load existing tasks from file when program starts

    while True:
        print('─────────────────')
        print('1. Add task')
        print('2. List tasks')
        print('3. Mark as done')
        print('4. Delete task')
        print('5. Quit')
        print('─────────────────')

        choice = input('Choose an option: ').strip()

        if choice == '1':
            add_task(tasks)
        elif choice == '2':
            list_tasks(tasks)
        elif choice == '3':
            mark_done(tasks)
        elif choice == '4':
            delete_task(tasks)
        elif choice == '5':
            print('Goodbye!')
            break  # exit the while loop → program ends
        else:
            print('Invalid choice. Please enter 1-5.')


if __name__ == '__main__':
    main()