import math

class Category:

    def __init__(self, category):
        self.category = category
        self.ledger = []

    def __str__(self):
        title_length = len(self.category)
        asterisks = int((30 - title_length) / 2)
        return_string = "*" * asterisks + self.category + "*" * asterisks + "\n"
        for k in self.ledger:
            short_desc = k['description'][:23]
            desc_length = len(short_desc)
            rounded_amount = "{:.2f}".format(k['amount'])
            amount_length = len(str(rounded_amount))
            space_between = 30 - desc_length - amount_length
            space_between_str = " " * space_between
            return_string += "{}{}{}\n".format(short_desc, space_between_str, rounded_amount)
        balance = round(self.get_balance(), 2)
        return_string += "Total: {}".format(balance)
        return return_string

    def get_balance(self):
        balance = 0
        index = 0
        for j in self.ledger:
            itemamount = j['amount']
            balance = balance + itemamount
            index += 1
        return balance

    def check_funds(self, amount):
        balance = self.get_balance()
        if amount <= balance:
            return True
        else:
            return False

    def deposit(self, amount, description=""):
        self.ledger.append({"amount": amount, "description": description})

    def withdraw(self, amount, description=""):
        isFeasible = self.check_funds(amount)
        if isFeasible == True:
            self.ledger.append({"amount": -amount, "description": description})
            return True
        else:
            return False

    def transfer(self, amount, budget_category):

        isPossible = self.check_funds(amount)

        if isPossible == True:
            self.withdraw(amount, f"Transfer to {budget_category.category}")
            budget_category.deposit(amount, f"Transfer from {self.category}")
            return True
        else:
          return False

def create_spend_chart(categories):
    withdrawals = []
    withdrawal_total = 0
    for l in categories:
        w = 0
        for i in l.ledger:
            if i['amount'] < 0:
                w += i['amount'] * (-1)
        withdrawals.append(w)
        withdrawal_total += w
    withdrawals_percentage_to_round = [n * 10 / withdrawal_total for n in withdrawals]
    withdrawals_percentage_rounded = [math.floor(n) * 10 for n in withdrawals_percentage_to_round]
    chart = ""
    chart += ("Percentage spent by category\n")
    for i in range(100, -10, -10):
        line_string = " "
        if i != 0:
            line_string = "  "
        count = 0
        counto = 0
        for y in withdrawals_percentage_rounded:

            if (i) <= y:
                line_string += "o  "
                counto += 1
            else:
                line_string += "  "
                count += 1
        if counto < 2:
            line_string += " "
        if count == len(withdrawals_percentage_rounded):
            line_string += " "
        start_spaces = 3 - len(str(i))
        start_spaces_string = " " * start_spaces
        start_line_string = "{}{}|".format(start_spaces_string, i)
        chart += ("{}{}\n".format(start_line_string, line_string))

    line_length = len(line_string) + 4
    chart += (" " * 4 + "-" * (line_length-4) + "\n")

    categories_names = [r.category for r in categories]
    vertical_length = len(max(categories_names, key=len))
    split_categories = [list(t.category) for t in categories]

    for u in split_categories:
        if len(u) < vertical_length:
            spaces_to_add = vertical_length - len(u)
            for q in range(0, spaces_to_add):
                u.append(" ")
    count = 0
    for k in range(0, vertical_length):
        line_str = " "
        for w in split_categories:
            line_str += "{}  ".format(w[count])
        if k == vertical_length-1:
            chart +=("    {}".format(line_str))
        else:
            chart += ("    {}\n".format(line_str))
        count += 1
    return chart
