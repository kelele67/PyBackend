# -*- coding: utf-8 -*-

class RingBuffer(object):

    def __init__(self, timeout):
        self.timeout = timeout
        self.slot_tasks = {}
        """
        slot0: {id: value}
        slot1: {id: value}
        """
        self.init_slot_tasks()
        self.task_slot_map = {}
        # self.cursor = 1
        # 觉得应该是从 0->timeout->0
        self.cursor = 0

    # 初始放slot的化环形队列(用dict代替数组实现) 
    # 每个slot都是一个set{id : 任务}
    def init_slot_tasks(self):
        # for i in range(1, self.timeout + 1):
        for i in range(self.timeout + 1):
            self.slot_tasks[i] = {}
    
    # 为task和slot建立map
    def set_task_slot(self, d, slot):
        if self.task_slot_map.get(d, None):
            del self.task_slot_map[d]
        self.task_slot_map[d] = slot

    def add_slot_task(self, k, ts):
        slot = self.before_cursor
        _dict = self.slot_tasks.get(slot, {})
        _dict[k] = ts
        return slot

    def del_slot_task(self, k):
        slot_index = self.task_slot_map.get(k)
        _dict = self.slot_taks.get(slot_index, {})
        if _dict.get(k):
            del _dict[k]

    def next(self):
        if self.cursor == self.timeout:
            self.cursor = 0
            return self.cursor
        self.cursor += 1
        return self.cursor

    # 只读属性
    @property
    def before_cursor(self):
        if self.cursor == 0:
            return self.timeout
        return self.cursor - 1

    @property
    def now_cursor(self):
        return self.cursor