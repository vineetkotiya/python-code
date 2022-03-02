global balance
balance = 100000
pin = 2321


def Bank(user):
    global balance
    if user == 1:
        print("Your Balance Is : ", balance)
    elif(opt == 2):
        withdraw = int(input("Enter Withdraw Amount : "))
        balance = balance-withdraw
        print("Your  withdraw Amount is ", withdraw)
        print("Your  Total Amount is ", balance)
    elif(opt == 3):
        deposite = int(input("Enter Deposite Amount : "))
        balance = balance+deposite
        print("Your  Deposite Amount is ", deposite)
        print("Your  Total Amount is ", balance)


print("""
            ** WELL COME TO DENA BANK **

            plase enter your ATM pin first.
""")
count = 3
while(count >= 1):
    userpin = input()
    if(userpin == pin):
        while True:
            print('''
                        1. for show  balance
                        2. for Creadite
                        3. for Deposite
                        4. Exit
            ''')
            
            opt = input()
            if opt in [1,2,3]:
                Bank(opt)
            else:
                print('''
                Exit Loading .....
                Loading .....
                Loading .....
                Loading .....
                Loading .....        
                .
                .
                .
                .
                .
                Thank You ......
                Exit Done !!
                ''')
                exit()

    else:
        if count > 1:
            count -= 1
            print("worng pin you have only ", count)
        else:
            print("You Enter Worng Pin multiple time Try Next Time   ")
            print('''
                  Thank You ....
            ''')
            exit()

