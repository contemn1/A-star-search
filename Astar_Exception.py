class BlockError(Exception):
    def __init__(self,node):
        """ @type node: node"""
        Exception.__init__(self)
        self.node = node
class LoopEnd(Exception):
    def __init__(self):
        Exception.__init__(self)