import random

class User:
    accounts=[]

    def __init__(self,name,email,address,account_type):
        self.name=name
        self.email=email
        self.address=address
        self.account_type=account_type
        self.transactions=[]
        self.balance=0
        self.loan=0
        self.account_number=self.generate_account_number()
        User.accounts.append(self)
        self.loan_count=0

    def generate_account_number(self):
        return random.randint(10000, 100000)

    def take_loan(self,amount):
        if self.loan_count<2:
            if amount>0:
                self.balance+=amount
                self.transactions.append(f"Loan Taken: ${amount}")
                self.loan_count+=1
                print(f"loan approved: ${amount} added to your balance")
            else:
                print("Invalid loan amount")
        else:
            print("You have reached the maximum number of loans")

    def transfer(self,receiver, amount):
        if amount>0 and amount<=self.balance:
            self.balance-=amount
            receiver.balance+=amount
            self.transactions.append(f"Transfer {amount} to {receiver.name}")
            receiver.transactions.append(f"Received {amount} from {self.name}")
            print(f"Transferred {amount} to {receiver.name}.New balance: {self.balance}")
        else:
            print("Invalid transfer amount")

    def deposit(self,amount):
        if amount>=0:
            self.balance+=amount
            print(f"Deposited {amount}.New balance: {self.balance}")
        else:
            print("Invalid deposit amount")

    def withdraw(self,amount):
        if amount>=0 and amount<=self.balance:
            self.balance-=amount
            print(f"Withdrew {amount}.New balance: {self.balance}")
        else:
            print("Withdrawal amount exceeded")

    def check_balance(self):
        return self.balance

    def transaction_history(self):
        return self.transactions

    def __str__(self):
        print( f"Account Number: {self.account_number}\nName: {self.name}\nEmail: {self.email}\nBalance: ${self.balance}\nAccount Type: {self.account_type}\n")

class Admin:
    def __init__(self):
        self.loan_feature_enabled=True

    def delete_account(self, user):
        if user in User.accounts:
           User.accounts.remove(user)
           print(f"Account for {user.name} deleted")
        else:
            print("Account Not found")


    def view_all_accounts(self):
        if User.accounts>0:
            print("List of all user account")
            for user in User.accounts:
               print(f"Account NUmber{ user.account_number},name:{user.name},Email:{user.mail}")


    def check_total_balance(self):
        total_balance=sum(user.balance for user in User.accounts)
        print(f"Total available balance in the bank: ${total_balance}")

    def total_loan(self):
        total_loan=sum(user.loan for user in User.accounts if user.loan<0)
        print(f"Total loan in the bank: {total_loan}")

    def loan_feature(self, enable):
        self.loan_feature_enabled = enable
        if enable:
            return "Loan feature enabled"
        else:
            return "Loan feature disabled"

admin=Admin()
current_user=None
admin_mode=False

while True:
    if current_user is None:
        print("No user logged in!")
        ch=input("Register/login (R/L),Admin login(A): ")
        if ch=="R":
            name=input("Name: ")
            email=input("Email: ")
            address=input("Address: ")
            account_type=input("Account Type (Savings/Current): ")
            current_user=User(name,email,address,account_type)
            print(f"Account created with account number:{current_user.account_number}")
        elif ch=="L":
            account_number=int(input("Account number: "))
            for user in User.accounts:
                if user.account_number==account_number:
                    current_user=user
                    break
            if current_user is None:
                print("Account not found.")
        elif ch=="A":
            admin_password=input("Enter admin password:")
            admin_mode=True        
    else:
        if admin_mode:
            print("Admin Menu:")
            print("1.Delete User Account")
            print("2.View All User Accounts")
            print("3.Check Total Balance")
            print("4.Check Total Loan")
            print("5.Loan Feature")
            print("6.Logout")
            op=input("Choose an option: ")

            if op=="1":
                account_number=int(input("Enter the account number to delete"))
                user_delete=None
                for user in User.accounts:
                    if user.account_number==account_number:
                        user_delete=user
                        break
                if user_delete:
                    admin.delete_account(user_delete)
                else:
                    print("User account no found")

            elif op=="2":
                admin.view_all_accounts()
            elif op=="3":
                admin.check_total_balance()

            elif op=="4":
                admin.total_loan()

            elif op=="5":
                enable_loan=input("Enable Loan Feature? (yes/no): ")
                if enable_loan=="yes":
                   admin.loan_feature(True)
                elif enable_loan=="no":
                    admin.loan_feature(False)
                else:
                  print("Invalid input.")

            elif op=="6":
                current_user=None
                admin_mode=False

            else:
                print("Invalid admin option")


        else:
            print(f"Welcome {current_user.name}\n")
            print("1.Withdraw")
            print("2.Deposit")
            print("3.Check Balance")
            print("4.Take Loan")
            print("5.Transfer")
            print("6.Transaction History")
            print("7.Logout")
        
            if admin.loan_feature_enabled:
               print("8.Loan Feature")

               op=input("Choose option: ")

               if op=="1":
                amount=int(input("Enter withdrawal amount: "))
                current_user.withdraw(amount)
            elif op=="2":
                amount=int(input("Enter deposit amount: "))
                current_user.deposit(amount)
            elif op=="3":
                 print(f"Available balance: {current_user.check_balance()}")
            elif op=="4":
                if admin.loan_feature_enabled:
                   amount=int(input("Enter loan amount: "))
                   current_user.take_loan(amount)
                else:
                   print("Loan feature is currently disabled.")
            elif op=="5":
                receiver_account_number=int(input("Enter receiver's account number: "))
                receiver=None
                for user in User.accounts:
                   if user.account_number==receiver_account_number:
                      receiver=user
                      break
                if receiver:
                  amount=int(input("Enter transfer amount: "))
                  current_user.transfer(receiver, amount)
                else:
                    print("Receiver's account  not exist.")
            elif op=="6":
                print("Transaction History:")
                for transaction in current_user.transaction_history():
                    print(transaction)
            elif op=="7":
                current_user=None
            elif op=="8" and admin.loan_feature_enabled:
                enable_loan=input("Enable Loan Feature? (yes/no): ")
                if enable_loan=="yes":
                   print(admin.loan_feature(True))
                elif enable_loan=="no":
                    print(admin.loan_feature(False))
                else:
                  print("Invalid input.")
            else:
                print("Invalid Option")
