import random
import datetime


def input_number(prompt='Please enter a number: ', minimum=0, maximum=None):
    """Read a positive number with the given prompt."""

    while True:
        try:
            number = int(input(prompt))
            if (number < minimum or
                    (maximum is not None and number > maximum)):
                print('Number is not within range: {} to {}'.format(minimum, maximum))
            else:
                break

        except ValueError:
            print('You need to enter a number')
            continue

    return number


class RolledOneException(Exception):
    pass


class Die:
    """A die to play with."""

    def __init__(self):
        # body of the constructor
        self.value = random.randint(1, 6)

    def roll(self):
        """Returns the rolled dice, or raises RolledOneException if 1."""

        self.value = random.randint(1, 6)
        if self.value == 1:
            raise RolledOneException

        return self.value

    def __str__(self):
        return "Rolled " + str(self.value) + "."


class Box:
    """Temporary score box holder class."""

    def __init__(self):
        # body of the constructor
        self.value = 0

    def reset(self):
        self.value = 0

    def add_dice_value(self, dice_value):
        self.value += dice_value


class Player(object):
    """Base class for different player types."""

    def __init__(self, name=None):
        # body of the constructor
        self.name = name
        self.score = 0

    def add_score(self, player_score):
        """Adds player_score to total score."""

        self.score += player_score

    def __str__(self):
        """Returns player name and current score."""

        return str(self.name) + ": " + str(self.score)


class ComputerPlayer(Player):
    # Inherit Base class player here
    cpu_names = ['Ca', 'Cb', 'Cc', 'Cd']

    def __init__(self, number):
        # body of the constructor
        """Assigns a cpu name from cpu_names, or Cpu#."""

        if number < len(self.cpu_names):
            name = self.cpu_names[number]
        else:
            name = 'Cpu{}'.format(number)

        super(ComputerPlayer, self).__init__(name)

    def keep_rolling(self, box):
        """Randomly decides if the CPU player will keep rolling."""
        while box.value < (10 + random.randint(1, 35)):
            print("  CPU will roll again.")
            return True
        print("  CPU will hold.")
        return False


class HumanPlayer(Player):
    # Inherit Base class player here
    def __init__(self, name):
        # body of the constructor
        super(HumanPlayer, self).__init__(name)

    def keep_rolling(self, box):
        """Asks the human player, if they want to keep rolling."""
        # gsfdgvb

        human_decision = input_number("  1 - Roll again, 0 - Hold? ", 0, 1)
        if human_decision == 1:
            return True
        else:
            return False


class GameManager:
    def __init__(self, humans=1, computers=1):
        # body of the constructor
        """Initialises the game, optionally asking for human player names."""
        self.players = []
        if humans == 1:
            self.players.append(HumanPlayer('Human'))
        else:
            for i in range(humans):
                player_name = input('Enter name of human player no. {}: '.format(i))
                self.players.append(HumanPlayer(player_name))

        for i in range(computers):
            self.players.append(ComputerPlayer(i))

        self.no_of_players = len(self.players)

        self.die = Die()
        self.box = Box()

    @staticmethod
    def welcome():
        """Prints a welcome message including rules."""

        print("*" * 70)
        print("Welcome to Pig Dice!".center(70))
        print("*" * 70)
        print("The objective is to be the first to reach 100 points.".center(70))
        print("On each turn, the player will roll a die.".center(70))
        print("The die value will stored in a temporary score box.".center(70))
        print("(If the die value is 1, the player earns no points,".center(70))
        print("and the turn goes to the next player.)".center(70))
        print("A human player has an option to either roll again,".center(70))
        print("or hold. If you hold, the score in the".center(70))
        print("temporary box will be added to your total score.".center(70))
        print(" Good luck! ".center(70, "*"))
        print(" Remember ".center(70, "*"))
        print(" Fortune favors the brave... ".center(70, "*"))
        print(" but chance favors the smart! ".center(70, "*"))
        print()
        print("I will now decide who starts".center(70, " "))
        print()

    def decide_first_player(self):
        """Randomly chooses a player to begin, and prints who is starting."""

        self.current_player = random.randint(1, self.no_of_players) % self.no_of_players

        print('{} starts'.format(self.players[self.current_player].name))

    def next_player(self):
        """Advanced self.current_player to next player."""
        self.current_player = (self.current_player + 1) % self.no_of_players

    def previous_player(self):
        """Changes self.current_player to previous player."""

        self.current_player = (self.current_player - 1) % self.no_of_players

    def get_all_scores(self):
        """Returns a join all players scores."""

        return ', '.join(str(player) for player in self.players)

    def play_game(self):
        """Plays an entire game."""
        self.final = False
        self.welcome()
        self.decide_first_player()
        while all(player.score < 100 for player in self.players):
            if not self.final:
                print('\nCurrent score --> {}'.format(self.get_all_scores()))
                print('\n*** {} to play ***'.format(self.players[self.current_player].name))
                self.box.reset()

                while self.keep_rolling():
                    if self.final:
                        break;
                    pass

                self.players[self.current_player].add_score(self.box.value)
                self.next_player()
            else:
                break;

        ## The previous player has won...
        if not self.final:
            self.previous_player()
            print(' {} has won '.format(self.players[self.current_player].name).center(70, '*'))

    def keep_rolling(self):
        """Adds rolled dice to box. Returns if human/cpu wants to continue.

        If either player rolls a 1, the box value is reset, and turn ends.
        """
        try:
            dice_value = self.die.roll()
            self.box.add_dice_value(dice_value)
            now = datetime.datetime.now()
            now_plus_10 = now + datetime.timedelta(minutes=1)
            try:
                if not self.now:
                    self.now = now
                    self.now_plus_10 = now_plus_10
            except:
                self.now = now
                self.now_plus_10 = now_plus_10

            if self.now_plus_10 <= now:
                self.score_list = []
                for player in self.players:
                    self.score_list.append(player.score)

                for player in self.players:
                    if max(self.score_list) != 0:
                        if player.score == max(self.score_list):
                            # import pdb;pdb.set_trace();
                            print(
                                "*************************** " + player.name + " has won ****************************")
                            self.final = True
                    else:
                        self.final = True
                        print("*************************** Match tie ****************************")
                        break;

            if not self.final:
                print('Last roll: {}, new box value: {}'.format(dice_value, self.box.value))

                # Check if human (by asking) or computer(calculating) will keep rolling
                return self.players[self.current_player].keep_rolling(self.box)

        except RolledOneException:
            print('  Rolled one. Switching turns')
            self.box.reset()
            return False


def main():
    human_players = input_number('How many human players? ')
    computer_players = input_number('How many computer players? ')

    game_manager = GameManager(human_players, computer_players)
    game_manager.play_game()


if __name__ == '__main__':
    main()

