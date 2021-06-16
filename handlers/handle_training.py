#!/usr/bin/python3
import re

class HandleTraining():
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def handle_training(self, message, player_inventory):
        '''Solve training scenarios

            Returns: answer or 'none found'
        '''

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
                print(f"Answer: {self.training_mine(message, player_inventory)}")
                return self.training_mine(message, player_inventory)

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

    def training_mine(self, message, player_inventory):
        ''' For now, we just answer this with "yes" until we build out
            the training solver
        '''
        try:
            ruby_question = int(re.search(r'Do you have more than (\d{1,})\s.+', message).group(1))
            if player_inventory["ruby"] > ruby_question:
                return "yes"
            else:
                return "no"

        except AttributeError:
            return "none found"