import random
import string

class queue:
    def __init__(self):
        self.__queue = []
        self.__id = util.random_str(16)
        self.count = 0

    def add(self, newdata):
        self.__queue.append(newdata)
        self.count += 1

    def dequeue(self):
        if not len(self.__queue) == 0:
            self.count -= 1
            return self.__queue.pop(0)
        else:
            raise IndexError("dequeue from empty queue")

    def remove(self, index):
        if len(self.__queue)-1 >= index:
            self.count -= 1
            del self.__queue[index]
        else:
            raise IndexError("index out of range")

    def remove_all(self):
        self.count = 0
        self.__queue = []

    def get(self, index):
        if len(self.__queue)-1 >= index:
            return self.__queue[index]
        else:
            raise IndexError("index out of range")

    def get_all(self):
        return self.__queue

class util:
    def random_str(n):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=n))

if __name__ == "__main__":
    print("This is a library.")