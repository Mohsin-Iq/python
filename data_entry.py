import datetime as datetime

date_format = '%Y-%m-%d'
CATEGORIES = {'I': 'Income', 'E': 'Expense'}

def get_date(prompt , allow_default = False) -> datetime:
  date_str =  input(prompt)
  if allow_default and not date_str:
    return datetime.datetime.now().strftime(date_format)

  try:
    valid_date = datetime.datetime.strptime(date_str, date_format)
    return valid_date.strftime(date_format)
  except ValueError:
   print('Invalid date. Please try again')
   return get_date(prompt , allow_default)

def get_amount() -> float:
    try:
      amount = float(input("Enter the amount: "))
      if amount <= 0:
        return ValueError("Amount must be greater than 0.")
      return amount
    except ValueError as e:
      print(e)
      return get_amount()

def get_category() -> str:
  category = input("Enter the category ('I' for the Income or 'E' for Expanse): ").upper()
  if category in CATEGORIES:
    return CATEGORIES[category]
  
  print("Invalid category. Please enter ('I' for the Income or 'E' for Expanse)")
  return get_category()
  
def get_description() -> str:
  description = input("Enter the description (optional): ")
  return description