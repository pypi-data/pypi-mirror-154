import json as js
import os

class YanDB:
    def __init__(self, json_file):
        self.json_file = json_file
        self.json_data = {}
        self.setup()
        
                
    def setup(self):
        if not os.path.exists(self.json_file):
            with open(self.json_file, 'w') as f:
                f.write('{}')
                self.json_data = js.load(f)


    

    def save(self):
        with open(self.json_file, 'w') as f:
            js.dump(self.json_data, f)

    def add(self, key, value):
        self.json_data[key] = value
        self.save()
    
    def get(self, key=None):
        if key is None:
            return self.json_data
        else:
            return self.json_data[key]
    
    def delete(self, key):
        del self.json_data[key]
        self.save()
    
    def update(self, key, value):
        self.json_data[key] = value
        self.save()

    def delall(self):
        self.json_data = {}
        self.save()
    
    def __getitem__(self, key):
        return self.json_data[key]
    
    def __setitem__(self, key, value):
        self.json_data[key] = value
        self.save()
    
    def __delitem__(self, key):
        del self.json_data[key]
        self.save()
    
    def __contains__(self, key):
        return key in self.json_data
    
    def __iter__(self):
        return iter(self.json_data)

    def __len__(self):
        return len(self.json_data)
    
    def __add__(self, other):
        self.json_data.update(other.json_data)
        self.save()

    def __iadd__(self, other):
        self.json_data.update(other.json_data)
        self.save()

   


if __name__ == '__main__':
    db = YanDB('test.json')
    db['test'] = 'test'
    db['test2'] = 'test2'