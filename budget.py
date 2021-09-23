class Category:
  def __init__(self, t):
    self.type = t
    self.ledger = []
    self.reserves = 0
    self.spent = 0
  
  def getType(self):
    return self.type

  def check_funds(self, amount):
    return self.reserves >= amount

  def deposit(self, amount, description=""):
    obj = {"amount":amount, "description":description}
    self.ledger.append(obj)
    self.reserves = self.reserves + amount
  
  def withdraw(self, amount, description=""):
    if not self.check_funds(amount):
      return False
    obj = {"amount":-amount, "description":description}
    self.ledger.append(obj)
    self.reserves = self.reserves - amount
    self.spent = self.spent + amount
    return True

  def get_balance(self):
    return self.reserves

  def get_total_spent(self):
    return self.spent

  def transfer(self, amount, category):
    if(self.withdraw(amount, "Transfer to "+ category.getType())):
      category.deposit(amount, "Transfer from "+self.type)
      return True
    return False

  def __str__(self):
    left = (30 - len(self.type))//2
    right = 30 - len(self.type) - left
    s = "*"*left + self.type + "*"*right + "\n"
    for t in self.ledger:
      descr = t["description"]
      if len(descr) > 23:
        descr = descr[:23]
      amount = '%.2f' % round(t["amount"],2)
      if len(amount) > 7:
        amount = amount[:7]
      s = s + descr + (30 - len(descr) - len(amount))*" " + amount + "\n"
    s = s + "Total: " + '%.2f' % round(self.reserves, 2)
    return s

def create_spend_chart(categories):
  spent = []
  for c in categories:
    spent.append(c.get_total_spent())
  total_spent = sum(spent)
  spent_percents = []
  for s in spent:
    spent_percent = 100 * s / total_spent
    spent_percents.append(spent_percent)
  result = "Percentage spent by category\n"
  current = 100
  while current >= 0:
    current_string = str(current)
    current_string = " "*(3 - len(current_string)) + current_string + "| "
    for s in spent_percents:
      if s >= current:
        current_string = current_string + "o  "
      else:
        current_string = current_string + "   "
    result = result + current_string + "\n"
    current = current - 10
  result = result + 4 * " " + (1 + 3 * len(categories)) * "-" + "\n"
  names = list(map(lambda x: x.getType(), categories)) 
  for i in range(len(max(names, key=len))):
    result = result + 5 * " "
    for n in names:
      if len(n) <= i:
        result = result + 3 * " "
      else:
        result = result + n[i] + 2 * " "
    result = result + "\n"


  return result[:-1]