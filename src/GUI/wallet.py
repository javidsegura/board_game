class Wallet:
    def __init__(self, initial_balance=1000):
        self.balance = initial_balance
        self.current_bet = 0
        self.current_multiplier = 1
        self.current_profit = 0

    def place_bet(self, amount):
        if amount <= 0:
            raise ValueError("Bet amount must be greater than zero.")
        self.current_bet = amount
        self.balance -= amount

    def update_multiplier(self, new_multiplier):
        self.current_multiplier = new_multiplier
        self.current_profit = self.current_bet * (self.current_multiplier - 1)

    def cash_out(self):
        winnings = self.current_bet * self.current_multiplier
        self.balance += winnings
        self.reset_bet()
        return winnings

    def reset_bet(self):
        self.current_bet = 0
        self.current_multiplier = 1
        self.current_profit = 0

    def get_balance(self):
        return self.balance

    def get_current_bet(self):
        return self.current_bet

    def get_current_multiplier(self):
        return self.current_multiplier

    def get_current_profit(self):
        return self.current_profit

    def calculate_percentage_bet(self, percentage):
        return abs(self.balance) * (percentage / 100)
