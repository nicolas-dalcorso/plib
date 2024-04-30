import modules.tasks as tasks;
import modules.jsonShelves as Shelves

NUM_TASKS = 10;

FTASKS: list[tasks.FormattedTask] = [];


if __name__ == '__main__':
    shelve = Shelves.IterableShelve('tasks.json');
    TASKS = shelve.data;
    
    for task in TASKS:
        t = tasks.setFormattedTaskFromDict(task);
        print(t);
    
    exit('end of execution');
