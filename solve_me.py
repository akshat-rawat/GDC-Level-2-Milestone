class TasksCommand:
    TASKS_FILE = "tasks.txt"
    COMPLETED_TASKS_FILE = "completed.txt"

    current_items = {}
    completed_items = []

    def read_current(self):
        try:
            file = open(self.TASKS_FILE, "r")
            for line in file.readlines():
                item = line[:-1].split(" ")
                self.current_items[int(item[0])] = " ".join(item[1:])
            file.close()
        except Exception:
            pass

    def read_completed(self):
        try:
            file = open(self.COMPLETED_TASKS_FILE, "r")
            self.completed_items = file.readlines()
            file.close()
        except Exception:
            pass

    def write_current(self):
        with open(self.TASKS_FILE, "w+") as f:
            f.truncate(0)
            for key in sorted(self.current_items.keys()):
                f.write(f"{key} {self.current_items[key]}\n")

    def write_completed(self):
        with open(self.COMPLETED_TASKS_FILE, "w+") as f:
            f.truncate(0)
            for item in self.completed_items:
                f.write(f"{item}\n")

    def run(self, command, args):
        self.read_current()
        self.read_completed()
        if command == "add":
            self.add(args)
        elif command == "done":
            self.done(args)
        elif command == "delete":
            self.delete(args)
        elif command == "ls":
            self.ls()
        elif command == "report":
            self.report()
        elif command == "help":
            self.help()

    def help(self):
        print(
            """Usage :-
$ python tasks.py add 2 hello world # Add a new item with priority 2 and text "hello world" to the list
$ python tasks.py ls # Show incomplete priority list items sorted by priority in ascending order
$ python tasks.py del PRIORITY_NUMBER # Delete the incomplete item with the given priority number
$ python tasks.py done PRIORITY_NUMBER # Mark the incomplete item with the given PRIORITY_NUMBER as complete
$ python tasks.py help # Show usage
$ python tasks.py report # Statistics"""
        )
    
    def changePriority(self, priority) :
        if self.current_items.get(priority) :
            self.changePriority(priority+1)
            self.current_items[priority+1] = self.current_items[priority]

    def add(self, args):
        if len(args) != 2: print("Error: Missing tasks string. Nothing added!")
        else: 
            self.changePriority(int(args[0]))
            self.current_items[int(args[0])] = args[1]
            print("Added task: \"" + args[1] +"\" with priority " + str(args[0]))
            self.write_current()

    def done(self, args):
        priority = int(args[0])
        if self.current_items.get(priority):
            self.completed_items.append(self.current_items.get(priority))
            del self.current_items[priority]
            self.write_current()
            self.write_completed()
            print("Marked item as done.")
        else:
            print("Error: no incomplete item with priority " + str(priority) + " exists.")

    def delete(self, args):
        priority = int(args[0])
        if self.current_items.get(priority):
            del self.current_items[priority]
            self.write_current()
            print("Deleted item with priority " + str(priority))
        else:
            print("Error: item with priority " + str(priority) + " does not exist. Nothing deleted.")

    def ls(self):
        if len(self.current_items) == 0:
            print("There are no pending tasks!")
        else:
            current_items_list = sorted(self.current_items.items(), key=lambda x:x[0])
            for i in range(len(current_items_list)):
                print(str(i+1) + ". " + str(current_items_list[i][1]) + " [" + str(current_items_list[i][0]) + "]")

    def report(self):
        print("Pending : " + str(len(self.current_items)))
        self.ls()

        print("\nCompleted : " + str(len(self.completed_items)))
        for i in range(len(self.completed_items)):
            print(str(i+1) + ". " + self.completed_items[i])
