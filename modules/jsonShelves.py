import json;


class Shelf:
    """A `Shelf` is a container-like object for reading and writing formatted data to `.JSON` files.
    """
    __slots__ = ['filepath', 'data'];
    
    def __init__(self, filepath: str) -> None:
        self.filepath   = filepath;
        try:
            self.data       = json.load(open(filepath, 'r'));
        except json.JSONDecodeError:
            print(f"JSONDecodeError: {self.filepath} is not a valid JSON file.");
            self.data = {};
            self.save();
        except FileNotFoundError:
            print(f"FileNotFoundError: {self.filepath} not found.");
            self.data = {};
            self.save();
           
    def save(self) -> None:
        try:
            json.dump(self.data, open(self.filepath, 'w'));
        except Exception as e:
            print(f"Error: {e}");
            
                
    def __str__(self) -> str:
        return f"Shelve(filepath={self.filepath})";
    
    def __repr__(self) -> str:
        return f"Shelve(filepath={self.filepath})";
    
class IterableShelve(Shelf):
    """A `IterableShelve` is a list-like object for reading and writing formatted data to `.JSON` files.
    All the data in a `IterableShelve` is stored in a list. Each stored entry must be a dictionary capable of being parsed by the parser in the `json` module.
    The `.JSON` generated file will be a list of dictionaries.
    """
    def __init__(self, filepath: str) -> None:
        super().__init__(filepath);
        
        if(not isinstance(self.data, list) or self.data == {}):
            self.data = list(self.data.values());
    
    def insert(self, object_dict: dict) -> None:
        try:
            self.data.append(object_dict);
        except Exception as e:
            print(f"Error: {e}");
        self.save();
        
    def remove(self, object_dict: dict) -> None:
        self.data.remove(object_dict);
        
    def __str__(self) -> str:
        return f"IterableShelve(filepath={self.filepath})";

    def __repr__(self) -> str:
        return f"IterableShelve(filepath={self.filepath})";
    
