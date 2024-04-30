"""
Stand-alone module for managing tasks.

nrdc
2024-04-29
v0.1.0
"""

from enum                   import Enum;
from typing                 import List;
from datetime               import datetime;
from jsonShelves    import *;
from tasks          import *;
from loggr          import *;

#   The `TaskFile` namedtuple contains information about the tasks file.
TaskFileData = namedtuple('TaskFileData', ['filepath', 'num_tasks', 'size', 'created', 'last_acessed']);

#   Status codes for the `Taskr` class.
class TaskrStatus(Enum):
    TASKR_STATUS__SUCCESS           = 0;
    TASKR_STATUS__ERR_FILE_NOT_FOUND= 1;
    TASKR_STATUS__ERR_CANNOT_WRITE  = 2;
    TASKR_STATUS__ERR_UNKNOWN       = 3;
    TASKR_STATUS__ERR_PARSER        = 4;
    TASKR_STATUS__ERR_TASK          = 5;
    TASKR_STATUS__ERR_FORMATTEDTASK = 6;
    TASKR_STATUS__ERR_LOGGR         = 7;
    

class Taskr:
    """Manager class for `Task`, `FormattedTask` objects.
    """
    __slots__ = ['parser', 'shelve', 'loggr'];
    parser: TaskParser | None;
    shelve: IterableShelve | None;
    loggr: Loggr | None;
    
    DEFAULT__FILEPATH_DICT = {
        'logfile'           : r'./logs/taskr.log',
        'tasks_dict'        : r'./data/tasks_dict.json',
        'taskfile'          : r'./data/tasks.txt'
    };
    
    DEFAULT__LOGGR_CONFIG = {
        'log_file'          : DEFAULT__FILEPATH_DICT['logfile'],
        'log_level'         : LogLevel.DEBUG,
        'formatter_string'  : '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        'datefmt'           : '%m-%d-%Y %I:%M:%S %p'
    };
    
    def __checkFiles(self, filepaths:dict, create_always:bool=False) -> bool:
        """Check if each file in the `filepaths` dictionary exists. Creates the file if it does not exist.
        If the `create_always` flag is set to `True`, the file will be created regardless of its existence.
        """
        #   Check if files exist
        for key in filepaths:
            if(not os.path.exists(filepaths[key])):
                try:
                    with open(filepaths[key], 'w') as f:
                        f.write('');
                except:
                    return False;
            else:
                if(create_always):
                    try:
                        with open(filepaths[key], 'w') as f:
                            f.write('');
                    except:
                        return False;
    
    def __init__(self, filepaths:dict=DEFAULT__FILEPATH_DICT, loggr_config:dict=DEFAULT__LOGGR_CONFIG):
        self.__checkFiles(filepaths);
        
        self.parser = TaskParser();
        self.shelve = IterableShelve(filepaths['tasks_dict']);
        self.loggr  = Loggr(loggr_config['log_file'], loggr_config['log_level'], loggr_config['formatter_string'], loggr_config['datefmt']);
        
        self.loggr.info('Taskr initialized.');
        
        
        
    
    def __len__(self) -> int:
        return len(self.tasks);
    
    def size(self) -> int:
        return os.path.getsize(self.shelve.filepath);
    
    def getTaskFileData(self) -> TaskFileData:
        filepath    = self.shelve.filepath;
        num_tasks   = len(self.shelve.data);
        size        = self.size();
        created     = datetime.fromtimestamp(os.path.getctime(filepath));
        last_acessed= datetime.fromtimestamp(os.path.getatime(filepath));
        
        return TaskFileData(filepath, num_tasks, size, created, last_acessed);
    
            
    def update(self):
        self.shelve.save();
        self.loggr.info('Taskr updated.');
    
    def count(self) -> int:
        return len(self.tasks);
     
    def close(self):
        self.shelve.save();
        self.loggr.info('Taskr closed.');
    
    def newTask(self, task: FormattedTask) -> TaskrStatus:
        """Given a `FormattedTask` object, add it to the `Taskr` object.

        Args:
            task (FormattedTask)

        Returns:
            TaskrStatus
        """
        try:
            self.shelve.insert(task.get());
            self.loggr.info(f'New task added: {task}');
            return TaskrStatus.TASKR_STATUS__SUCCESS;
        except:
            return TaskrStatus.TASKR_STATUS__ERR_TASK;
    
    def newTask(self) -> TaskrStatus:
        """Invokes the `TaskParser` object to parse a `FormattedTask` from the user.

        Returns:
            TaskrStatus
        """
        try:
            task = setRandomTask();
            print(task);
            self.shelve.insert(task.get());
            self.loggr.info(f'New task added: {task}');
            return TaskrStatus.TASKR_STATUS__SUCCESS;
        except Exception as e:
            print(e);
            return TaskrStatus.TASKR_STATUS__ERR_TASK;
        
    
    
    
if __name__ == '__main__':
    taskr = Taskr();
   
    print(taskr.getTaskFileData());
    taskr.newTask() == TaskrStatus.TASKR_STATUS__SUCCESS
    taskr.update();
    print(taskr.getTaskFileData());
    
    print(f"Mean task size: {taskr.size() / taskr.getTaskFileData().num_tasks} bytes.")
    
    taskr.close();
    exit('end of execution');


