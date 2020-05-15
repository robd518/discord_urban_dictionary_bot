#!/usr/bin/python3
import re

trainings = [
r'''**mudda** is training in the river!
What is the name of this fish? <:goldenfish:697940429500317727>
**1** - normie fish
**2** - golden fish
**3** - epic fish
Answer with a `1`, `2` or `3`! You have 15 seconds!''',
r'''**mudda** is training in the... casino?
Is this a **COIN** ? ️:four_leaf_clover:
Answer with `yes` or `no`! You have 15 seconds!''',
r'''**mudda** is training in the forest!
<:HYPERMEGASUPEREPICwoodenlog:546054891408457730><:woodenlog:555047053441630209><:woodenlog:555047053441630209><:woodenlog:555047053441630209><:MEGASUPEREPICwoodenlog:545396411316043776>
How many <:woodenlog:555047053441630209> do you see? you have 15 seconds!''',
r'''**mudda** is training in the... casino?
Is this a **COIN** ? :gift:
Answer with `yes` or `no`! You have 15 seconds!''',
r'''**mudda** is training in the forest!
<:MEGASUPEREPICwoodenlog:545396411316043776><:SUPEREPICwoodenlog:541384398503673866><:woodenlog:555047053441630209><:EPICwoodenlog:541056003517710348><:MEGASUPEREPICwoodenlog:545396411316043776>
How many <:SUPEREPICwoodenlog:541384398503673866> do you see? you have 15 seconds!''',
r'''**mudda** is training in the... casino?
Is this a **GIFT** ? :gem:
Answer with `yes` or `no`! You have 15 seconds!''',
r'''**mudda** is training in the river!
What is the name of this fish? <:normiefish:697940429999439872>
**1** - normie fish
**2** - golden fish
**3** - epic fish
Answer with a `1`, `2` or `3`! You have 15 seconds!''',
r'''**mudda** is training in the mine!
Do you have more than 4 <:ruby:603304907650629653> rubies in your inventory?
Answer with `yes` or `no`! You have 15 seconds!''',
r'''**mudda** is training in the field!
What's the **fifth** letter of <:Apple:697940429668089867>?
Answer with a letter! You have 15 seconds!''',
r'''**mudda** is training in the river!
What is the name of this fish? <:normiefish:697940429999439872>
**1** - normie fish
**2** - golden fish
**3** - epic fish
Answer with a `1`, `2` or `3`! You have 15 seconds!''',
r'''**mudda** is training in the... casino?
Is this a **FOUR LEAF CLOVER** ? :gift:
Answer with `yes` or `no`! You have 15 seconds!''',
r'''**mudda** is training in the forest!
<:EPICwoodenlog:541056003517710348><:HYPERMEGASUPEREPICwoodenlog:546054891408457730><:MEGASUPEREPICwoodenlog:545396411316043776><:woodenlog:555047053441630209><:SUPEREPICwoodenlog:541384398503673866>
How many <:MEGASUPEREPICwoodenlog:545396411316043776> do you see? you have 15 seconds!''',
r'''**mudda** is training in the river!
What is the name of this fish? <:EPICfish:543182761431793715>
**1** - normie fish
**2** - golden fish
**3** - epic fish
Answer with a `1`, `2` or `3`! You have 15 seconds!'''
]

class HandleTraining():
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def handle_training(self, message):
        '''Solve training scenarios

            Returns: answer or 'none found'
        '''

        print(f'==================\n{message}')

        try:
            # Get the location
            location = re.search(r'^\*\*.+\*\* is training in the(\s|\.{3}\s)(.+?)(\!|\?)', message).group(2)
            print(f"Location: {location}")
            if (location == "casino"):
                print(f"Answer: {self.training_casino(message)}")
                return self.training_casino(message)

            elif (location == "field"):
                print(f"Answer: {self.training_field(message)}")
                return self.training_field(message)

            elif (location == "river"):
                print(f"Answer: {self.training_river(message)}")
                return self.training_river(message)

            elif (location == "forest"):
                print(f"Answer: {self.training_forest(message)}")
                return self.training_forest(message)

            elif (location == "mine"):
                print(f"Answer: {self.training_mine(message)}")
                return self.training_mine(message)

        except AttributeError:
            return "none found"
            

    def training_casino(self, message):
        ''' Simple comparison training.
            There's only a certain number of items that get included
            in this training and so we use a simple dictionary of k:v
            pairs to solve the yes/no question
        '''

        item_dict = {
            "diamond" : "gem",
            "coin" : "coin",
            "four leaf clover" : "four_leaf_clover",
            "gift" : "gift",
            "dice" : "game_die"
        }

        try:
            match = re.search(r'Is this a \*\*(.+?)\*\*.+\:(.+?)\:\s', message)
            lookup_item, compare_item = match.group(1).lower(), match.group(2).lower()
            if item_dict[lookup_item] == compare_item:
                return "yes"
            else:
                return "no"

        except AttributeError:
            return "none found"

    def training_field(self, message):
        ''' Simply lookup the letter found at the index of the
            item that's in the question and return that as the
            answer.
        '''

        lookup_dict = {
            "first" : 0,
            "second" : 1,
            "third" : 2,
            "fourth" : 3,
            "fifth" : 4,
            "sixth" : 5
        }

        try:
            match = re.search(r'What\'s the \*{2}(.+?)\*{2}.+\:(.+?)\:', message)
            index, item = match.group(1).lower(), match.group(2).lower()
            return item[lookup_dict[index]]

        except AttributeError:
            return "none found"

    def training_river(self, message):
        ''' Parse out the fish and look it up against the answer
            dictionary and return the value as the answer
        '''

        answer_dict = {
            "normiefish" : "1",
            "goldenfish" : "2",
            "epicfish" : "3"
        }

        try:
            fish_type = re.search(r'.+\:(.+?)\:', message).group(1).lower()
            return answer_dict[fish_type]

        except AttributeError:
            return "none found"

    def training_forest(self, message):
        ''' We solve this by finding all the logs in the entire string
            and then removing the last one since re.findall moves left
            to right (and the last one is always the "lookup" item). We
            simply count the occurrences in the results of re.findall
            and return that.
        '''

        try:
            logs = re.findall(r'\:(.+?)\:', message)
            lookup_item = logs[-1]
            del logs[-1]
            return logs.count(lookup_item)
        
        except AttributeError:
            return "none found"

    def training_mine(self, message):
        ''' For now, we just answer this with "yes" until we build out
            the training solver
        '''
        return "yes"

if __name__ == "__main__":
    handler = HandleTraining()
    for each in trainings:
        handler.handle_training(each)