class Student:
    def __init__(self, **obj):
        for key, value in obj.items():
            print(key, value)

        # print('Name':)


stud = [{'roll': 121, 'name': 'vineet', 'address': 'indore'},
        {'roll': 131, 'name': 'Sonu', 'address': 'viajynagar'}]
while True:
    print('''
            1.Show All details      
            2.Show Student details      
            3.Add New Student
            4.Exit
    ''')
    i = input()
    if i == 1:
        scl_pin = input("Enter School Pin : ")
        if scl_pin == 2525:
            for st in stud:
                Student(**st)
    elif(i == 2):
        userroll = input("Enter Roll : ")
        for obj in stud:
            if userroll == obj["roll"]:
                Student(**obj)
    elif (i == 3):
        d={}
        roll=int(input("Enter roll :"))
        name=raw_input("Enter  Name :")
        address=raw_input("Enter Address :")
        print(name)
        d["roll"]=roll
        d["name"]=name
        d["address"]=address
        print("New Student Add !",d)
        stud.append(d)
    elif(i==4):
        exit()