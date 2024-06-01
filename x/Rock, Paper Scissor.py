# rock, paper and scissors
choice = int(input ("What do you choose? Type 0 for Rock, 1 for Paper or 2 for Scissors."))
import random
game = random.randint(0, 2)
if choice == 0:
    if game == 0:
        print ("Computer chose rock")
    
    elif game == 1:
        print("Computer chose paper")
    
    elif game == 2:
        print ("Compter chose scissor")
    
    else:
        print ("Error")

elif choice == 1:
    if game == 0:
        print ("Computer chose rock")
    
    elif game == 1:
        print("Computer chose paper")
    
    elif game == 2:
        print ("Compter chose scissor")
    
    else:
        print ("Error")

elif choice == 2:
    if game == 0:
        print ("Computer chose rock")
    
    elif game == 1:
        print("Computer chose paper")
    
    elif game == 2:
        print ("Compter chose scissor")
    
    else:
        print ("Error")

else :
    print ("Error")
    

if choice == game:
    print ("Its a draw. Try again '-' ")
elif choice == 0 and game == 2:
    print ("You win !")
elif choice == 2 and game == 0:
    print ("You loose")
elif choice == 1 and  game == 0:
    print ("You win!")
elif choice == 2 and game == 1:
    print ("You win!")
elif choice < game:
    print ("You loose")
else:
    print ("You typed an invalid number")