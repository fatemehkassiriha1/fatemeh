from FunctionCalindex import CalcutIdexs  
from random import choice
from abc import ABC,abstractmethod

from infohang import infohang
class hangman(ABC):
    def __init__(self  , randomword ,showword , inputchar,guess, rate = 0,checking = None):
        self.rate = rate
        self.guess = guess
        self.checking = checking
        self.inputchar = inputchar
        self.randomword = randomword
        self.showword = showword
    @abstractmethod
    def checkingfunc(self):
        if self.inputchar in self.randomword:
            self.checking = True
            self.rate += 10 
        elif self.inputchar not in self.randomword:
            self.checking = False
            self.rate = self.rate - 1
    @abstractmethod
    def showingword(self):
        listshow = list(self.showword)
        if self.checking == True :
            listindex = CalcutIdexs(self.inputchar , self.randomword)
            for i in listindex:
                listshow[2*i] = self.inputchar
            self.showword = ''
            for j in listshow: 
                self.showword += j
        elif self.checking == False: 
            self.showword = self.showword   

class hangmansimple(hangman):
    
    def __init__(self , randomword ,showword, inputchar ='',guess = 0 , rate = 0 ,checking = None):
        super().__init__(randomword ,showword ,inputchar ,guess, rate ,checking )

    def checkingfunc(self):
        super().checkingfunc()
    def showingword(self) : 
        super().showingword()
    def __neg__(self):
        self.guess -= 1
        return self.guess
        
# class hangmanhard(hangman):
#     def __init__(self , randomword ,showword ,inputchar='', guess = 4 , rate = 0 , checking = None):
#         super().__init__( randomword ,showword ,inputchar ,guess, rate ,checking )
#     def checkingfunc(self):
#         super().checkingfunc()
#     def showingword(self):
#         super().showingword()
#     def __neg__(self):
#         self.guess -= 1
#         return self.guess



# /////////////////main code
print('welcome to the hangman :)')
listabc = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r'
,'s','t','u','v','w','x','y','z']

simplehard = ''

while True:
    #choose hard or simple
    simplehard = ''
    while True:
        simplehard = input('\nplease choose level :(simple / hard) : ')
        if simplehard == 'hard' or simplehard == 'simple':
            break

    listoffeild = ['animal' , 'jobs', 'color', 'fruit' , 'food' ,'country']
    if simplehard == 'hard' :
        listoffeild = [ e +'h' for e in listoffeild]
    feild = choice(listoffeild)
    y = feild + '.txt'

    with open(y) as file:
        try:
            randword = choice(file.readlines())
        finally:
            file.close()

        randword = randword.strip() #\n ro az akhar harf hazf mikonam
        li = len(randword)
        randomcharset = set(randword)
        lenranchars = len( randomcharset)

        guessnum = 0
        numabc = 0
        if simplehard == 'hard':
            numabc = 12
            guessnum = 4
        else:
            numabc = 8
            guessnum = 6

        #8/6 ta char bara user entekhab mikone
        while lenranchars < numabc:
            randomcharset.update(choice(listabc))
            lenranchars = len( randomcharset)

        #first state for simple hangman \\\\\\\\\\\\
        # print(randword)
        dashword = (li) * '- '
        objhangman = hangmansimple( randword , dashword ,'',guessnum)
        firstguess = objhangman.guess * 'x '
        infohang(feild , objhangman.showword , firstguess , objhangman.rate)
        print('this is the list of character to choose: ' , list(randomcharset))
        randchar = input('please enter a character : ')
        objhangman.inputchar = randchar
        losewin = None
        previouschar = []

        #other state for simple hangman \\\\\\\\\\\\\\\\
        while objhangman.guess > 0:
            if randchar not in list(randomcharset): # if e.g  =>'lk' or 'p' enter or that char isnt in list
                print('\nthis is not in the character list take new .')
            elif  randchar in previouschar :
                print('\nbefore you choose , take new.') #not precious char   
            else:
                objhangman.inputchar = randchar
                objhangman.checkingfunc()
                if objhangman.checking == True:
                    print('\nthats true:)')
                    objhangman.showingword()
                elif objhangman.checking == False:
                    print('\nthats false:(')
                    -objhangman
            if objhangman.guess == 0:
                losewin = False
                break
            guessing =  objhangman.guess * 'x '
            infohang(feild , objhangman.showword , guessing ,objhangman.rate) #show information game to user
            #agar barande shede bod az halghe bere biron
            if ('-' not in objhangman.showword):
                losewin = True # it means win 
                break
            print('this is the list of character to choose: ' , list(randomcharset))
            previouschar.append(randchar)
            randchar = input('please enter a character : ') 
        if losewin == True:
            print('game over\nyou win.congratulations \\\\\\///')
            
            #update top ten list\\\\\\\\\\\\
            with open('rate.txt' , 'r' ) as fr , open('rate.txt' , 'a') as fw:
                readlinerate = fr.readlines()
                readlinerate = set(readlinerate)
                readlinerate = list(readlinerate) 
                linerate = sorted(int(elemnt.strip()) for elemnt in readlinerate )#\n az akhar har readline ha haf mishe va sort mishe
                if linerate[:] == []:
                    fw.write(str(objhangman.rate)+ '\n')
                else:  
                    linerate[:] = linerate[::-1] #chon sort adad bozorg akhar mire e,g[20,50,90]
                    for i in range(0 ,10):
                        try:
                            if objhangman.rate == linerate[i]:
                                break
                            elif objhangman.rate > linerate[i]:
                                linerate[i:i] = [objhangman.rate]
                                break
                        except IndexError:
                            linerate[i:i+1] = [objhangman.rate]
                            break
                    fw.truncate(0) #file ro khali mikone dobare adad haro minevisim
                    fw.write('\n'.join(str(e) for e in linerate))
                fw.close()    
                fr.close()
        else:
            print('game over\nyou lose ! :(((')  
            print('this is word : ' ,randword)
        #top ten rate showwing \\\\\\\\\\\\\\
        fileshow = input('do you want to see all rates?(\'y\' as yes/\'n\' as no) : ')
        while True:
            if fileshow == 'y':
                with open('rate.txt') as rate:
                    read = rate.readlines()
                    read = [int(e.strip()) for e in read]
                    print(read)
                    rate.close()
                    break
                
            elif fileshow == 'n':
                break
            else:
                fileshow = input('just type y or n : ')

        #playagin\\\\\\\\
        try:
            playagain = input('do you like to play agin ? y / n : ')
            while True: 
                if playagain == 'n':
                    print('bye')
                    exit()
                elif playagain =='y':
                    break
                
                else: 
                    try:
                        playagain = input('please enter y or n :')
                    except Exception as d:
                        print('dont enter ctrl + c' ,d)# ctrl + c
                        continue
        except EOFError as e: #raise e.g =>^z ctrl + z
            print(e)
    