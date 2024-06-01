num1 = float(input("Enter your first number:"))
num2 = float(input("Enter your second number:"))
op = input("Enter your desired operater")

if op == "+":
    print(num1+num2)

elif op == "-":
    print(num1-num2)

elif op == "x":
    print(num1*num2)
    
elif op == "%":
    print(num1/num2)

else:
    print("Choose a operator")