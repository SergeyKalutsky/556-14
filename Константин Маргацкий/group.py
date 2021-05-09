class Group:
    def __init__(self, *objs):
        self.objs = list(objs)
        self.dir = self.__dir__()
    
    def __repr__(self):
        return "<%s(%d objects)>" % (self.__class__.__name__, len(self))
#         objs = [str(obj) for obj in self.objs]
#         if len(objs) > 1:
#             return 'Group(' + objs[0] + '...)'
#         if len(objs) == 1:
#             return 'Group(' + objs[0] + ')'
#         return 'Group( None )'
    
    def __iadd__(self, other):
        self.add(other)
        return self
    
    def __isub__(self, other):
        self.delete(other)
        return self
    
    def __getitem__(self, item):
        if type(item) == int:
            if -len(self.objs) < item < len(self.objs):
                return self.objs[item]
            else:
                raise IndexError('group index out of range')
        else:
            raise TypeError('group indices must be integers or slices, not %s' % (type(item)))
    
    def __setitem__(self, key, value):
        if type(key) == int:
            if -len(self.objs) < key < len(self.objs):
                self.objs[key] = value
            else:
                raise IndexError('group index out of range')
        else:
            raise TypeError('group indices must be integers or slices, not %s' % (type(key)))
    
    def __delitem__(self, key):
        if type(key) == int:
            if -len(self.objs) < key < len(self.objs):
                self.delete(key)
            else:
                raise IndexError('group index out of range')
        else:
            raise TypeError('group indices must be integers or slices, not %s' % (type(key)))
        
    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.objs == other.objs
    
    def __nq__(self, other):
        return not self.__eq__(other)
    
    def __bool__(self):
        if len(self.objs) > 0:
            return True
        return False
    
    def __len__(self):
        return len(self.objs)
    
    def __contains__(self, item):
        return item in self.objs
    
#     def __getattribute__(self, name):
#         used = False
#         if name in self.dir:
#             return super().__getattribute__(self, name)
#         print(True)
#         for obj in self.objs:
#             if name in obj.dir:
#                 obj.__getattribute__()
#                 used = True
#         if used: lambda: None 
#         raise AttributeError(name + ' is not used in added objects')
    
#     def _setmethod(self, func):
#         if not dunc in self.__dict__:
#             def function(*args):
#                 func(*args[1:])
    
    def add(self, *obj):
        obj = list(obj)
        for obj2 in obj:
            self.objs.append(obj2)
    
    def delete(self, index):
        for obj in range(index):
            del self.objs[obj]
    
    def copy(self):
        return self.__class__(*self.objs[:])