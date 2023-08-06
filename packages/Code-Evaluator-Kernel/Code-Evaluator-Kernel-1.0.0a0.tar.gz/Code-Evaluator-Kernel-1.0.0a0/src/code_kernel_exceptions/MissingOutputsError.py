class MissingOutputsError(Exception):

    def __init__(self):
        self.message = 'Outputs cannot be missed'
