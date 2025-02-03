import pandas as pd
import csv 
import datetime as datetime
from data_entry import get_amount, get_category, get_description , get_date
import matplotlib.pyplot as plt

class CSVHandler:
    CSV_FILE = 'Finance_data.csv'
    COLUMNS = ['Date', 'Amount', 'Category', 'Description']
    DATE_FORMAT = '%Y-%m-%d'

    @classmethod
    def initialize_csv(cls):
     try:
      pd.read_csv(cls.CSV_FILE)
     except FileNotFoundError:
       df = pd.DataFrame(columns= cls.COLUMNS)
       df.to_csv(cls.CSV_FILE, index=False)  

    @classmethod
    def dd_entry(cls ,date, amount, category, description):
        # date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        data_entry = {
            'Date': date,
            'Amount': amount,
            'Category': category,
            'Description': description
        }
        with open(cls.CSV_FILE, 'a' , newline="") as file:
            writer = csv.DictWriter(file , fieldnames=cls.COLUMNS)
            writer.writerow(data_entry)
        print('Data Entry Successful')
    
    @classmethod
    def get_transaction(cls , start_date , end_date):
        df = pd.read_csv(cls.CSV_FILE)
        df["Date"] = pd.to_datetime(df["Date"] , format=cls.DATE_FORMAT)
        start_date = datetime.datetime.strptime(start_date, cls.DATE_FORMAT)
        end_date = datetime.datetime.strptime(end_date, cls.DATE_FORMAT)
        mask = (df['Date'] >= start_date) & (df['Date'] <= end_date)
        filtered_data =  df.loc[mask]
        if filtered_data.empty:
            print('No data found for the given date range')
        else:
            print(f"Transaction form {start_date.strftime(cls.DATE_FORMAT)} to {end_date.strftime(cls.DATE_FORMAT)}")
            print(
                filtered_data.to_string(
                    index=False , 
                    formatters={'Date': lambda x: x.strftime(cls.DATE_FORMAT)}
                    )
                )
            total_income = filtered_data[filtered_data['Category'] == 'Income']['Amount'].sum()
            total_expanse = filtered_data[filtered_data['Category'] == 'Expense']['Amount'].sum()
            print("\nSummary")
            print(f"Total Income: ${total_income:,.2f}")
            print(f"Total Expense: ${total_expanse:,.2f}")
            print(f"Net Saving: ${total_income - total_expanse:,.2f}")
            print(f"Total Amount: ${filtered_data['Amount'].sum():,.2f}")                
        return filtered_data    
    @classmethod
    def add(cls):
      cls.initialize_csv() 
      date = get_date("Enter the date (YYYY-MM-DD) or press Enter for today's date: ", allow_default=True)
      amount = get_amount()
      category = get_category()
      description = get_description()
      cls.dd_entry(date, amount, category, description) 

def plot_graph(df):
    df.set_index('Date', inplace=True)
    
    income_fd = df[df['Category'] == 'Income'].resample('D').sum().reindex(df.index , fill_value=0)
    expense_fd = df[df['Category'] == 'Expense'].resample('D').sum().reindex(df.index , fill_value=0)
    plt.figure(figsize=(10, 5))
    plt.plot(income_fd.index, income_fd['Amount'], label='Income' ,color='g')
    plt.plot(expense_fd.index, expense_fd['Amount'], label='Expense', color='r')
    plt.xlabel('Date')
    plt.ylabel('Amount')
    plt.title('Income vs Expense chart')
    plt.legend()
    plt.grid(True)
    plt.show()

def main():
   while True:
         print("1. Add a new transaction")
         print("2. View transactions and summary")
         print("3. Exit")
         choice = input("Enter your choice: ")
         if choice == '1':
              add()
         elif choice == '2':
              start_date = ("Enter the start date (YYYY-MM-DD): ")
              end_date = get_date("Enter the end date (YYYY-MM-DD): ")
              df = CSVHandler.get_transaction(start_date, end_date)
              if input("Do you want to plot the graph (y/n): ").lower() == 'y':
                  plot_graph(df)

         elif choice == '3':
              print("Exiting the program")
              break
         else:
              print("Invalid choice. choose again between 1, 2, and 3")
              continue
         
if __name__ == '__main__':
    main()         

#CSVHandler.get_transaction('2025-01-31' , '2025-01-31')
#add()
# CSVHandler.dd_entry(1000 , 'Income', 'Salary')       
