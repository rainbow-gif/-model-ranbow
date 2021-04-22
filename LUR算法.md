# **LUR算法**

​	页面置换算法 LRU 算法，是操作系统中一种典型的内存管理算法，常用于虚拟页式存储，这种页面置换算法的原理是，对于在内存中但又不用的数据块（内存块）叫做 LRU，操作系统会根据哪些数据属于 LRU 而将其移出内存，用于腾出空间来加载另外的数据

```python
#利用ordereddict实现的页面置换算法
import collections
class lrucache:
    def __init__(self,size):
        self.size = size
        self.odic = collections.OrderedDict()
    def get(self,key):
        if key in self.odic:
            val = self.odic[key]
            self.odic.pop(key)
            self.odic[key] = val
        else:
            val = None
        return val
    def set(self,key,val):
        if key in self.odic:
            self.odic.pop(key)
            self.odic[key] = val
        else:
            if len(self.odic) == self.size:
                self.odic.popitem(last=False)
                self.odic[key] = val
            else:
                self.odic[key]=val

lru = lrucache(5)
for i in range(5,10):
    lru.set(i,10*i)
print(lru.odic,lru.odic.keys())
#访问5,7
lru.get(5)
lru.get(7)
print(lru.odic,lru.odic.keys())
#写入新元素,淘汰旧元素
lru.set(10,100)
print(lru.odic,lru.odic.keys())
```

