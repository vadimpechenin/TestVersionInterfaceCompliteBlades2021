from handlers.baseCommandHandlerParameter import BaseCommandHandlerParameter

class LoadNominalsCommandHandler(BaseCommandHandlerParameter):
    def __init__(self, name_of_database):
        self.name_of_database = name_of_database
