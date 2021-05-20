import re
from math import *
import numpy as np
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import messagebox as msg

'''
A program to differentiate functions
Can differentiate:
1. Basic functions(should be present in deridict) and constants
2. Product rule d(uvw...)/dx
3. Chain rule d /dx (f(g(...(x))))
4. Combinations of 2 and 3
'''

#defining non in built functions
cosec = lambda x: 1/sin(x)
sec = lambda x: 1/cos(x)
cot = lambda x: 1/tan(x)

sinh = lambda x: (e**x - e**(-x))/2
cosh = lambda x: (e**x + e**(-x))/2
tanh = lambda x: (e**(2*x) - 1)/(e**(2*x) + 1)
cosech = lambda x: (1/sinh(x))
sech = lambda x: (1/cosh(x))
coth = lambda x: (1/tanh(x))

def plot(*funcs, a = -20, b = 20):#plots any f(x) taken in string
    x = np.arange(a,b,0.01)
    legnd = []
    for func in funcs:
        y = list(map(D.fvalue(func),x))
        plt.ylim([a,b])
        plt.xlim([a,b])
        legnd.append('y = '+func)
        plt.plot(x,y)
    plt.legend(legnd, loc='upper left')
    plt.grid(True)
    plt.minorticks_on()
    plt.show()
    
class D:
    # The main dict which contains derivative of basic functions (can be added)
    deridict = {'sin':'cos(x)','cos':'-sin(x)','tan':'sec^2(x)',
               'cosec':'-cosec(x)cot(x)','sec':'sec(x)*tan(x)','cot':'-cosec^2(x)',
               'sinh':'cosh(x)','cosh':'-sinh(x)','tanh':'sech^2(x)',
               'cosech':'-cosech(x)*coth(x)','sech':'sech(x)tanh(x)','coth':'-cosech^2(x)',
               'e^':'e^(x)','log':'1/(x)','x^x':'(x)^(x)(1 + log(x))'}
    
    def __init__(self, function):
        self.f = function
        self.__deri = '' #string where the derivative will be stored later
        self.f = self.f.replace(' ','') #removing spaces from string for convenience


    @staticmethod
    def listjoin(list1, start, end, sep = ''):# returns a concatenated string with all the elements of a given list
        a = ''
        for i in range(start,end):
            if i != start:
                a += sep
            a += list1[i]
        return a
        
    @staticmethod
    def insert_mult(func): # inserts * sign at appropriate places for productrule() and simplify()
        func = func.replace(' ','')
        add = 0 #to compensate the addition in len of string in every iteration
        insert_mult_pattern = re.compile(r'(?P<n1>([a-wA-Z^yz]+)(?P<n2>[\w(^]+?x[)]+)|([0-9]+))(?=[\w^]+?[\w(^]+?x[)]+)') #pattern for adding * between 2 functions
        numpattern = re.compile(r"(P<n3>\d+)[\w\(]") #pattern for adding * before a number
        bracket_pat = re.compile(r'(?P<b1>[)])[(]') #pattern for adding * between )(

        for match in insert_mult_pattern.finditer(func):
            func = func[:match.end('n1')+add]+'*'+ func[match.end('n1')+add:]
            add += 1
            
        ad1 = 0
        for num in numpattern.finditer(func):# 5(sin(x)) or 52tan(x)
            func = func[:num.end('n3')+ad1]+'*'+ func[num.end('n3')+add:]
            ad1+=1
            
        adb = 0
        for brack in bracket_pat.finditer(func):
            func = func[:brack.end('b1')+adb]+'*'+ func[brack.end('b1')+adb:]
            adb +=1
            
        func = re.sub(r'(\d+)(x)','\g<1>*\g<2>',func) # add * between constants and x like 12*x
        func = re.sub(r'(?<![a-wA-Zyz\d][(])(x)([a-wA-Zyz])','\g<1>*\g<2>',func) # add * after x like x*sin(x)
        func = re.sub(r'(?<=[a-zA-Z)])(\d+[/])',r'*\g<1>',func) #add * before 1/x like sin(x)*1/x        
        return func

    @staticmethod
    def brackfunc(func, brack=0): #returns a string with complete brackets like (sin(x)) or (sin(x)cos(x)) from given string
        for i in range(len(func)):
            if func[i] == '(':
                brack +=1
            elif func[i] == ')':
                brack -= 1
            if brack == 0 and ('(' in func[:i]):
                return func[:i+1]
                break

    @staticmethod
    def sign_manager(func): # simplifies the signs like - - gives +, - + gives -, etc.
        func = re.sub(r'[-]\s*[-]', '+', func)
        func = re.sub(r'[-]\s*[+]', '-', func)
        func = re.sub(r'[+]\s*[-]', '-', func)
        func = re.sub(r'[+]\s*[+]', '+', func)
        return func
    

    @staticmethod
    def fvalue(funct, val = ''): #returns a function if value not specified else returns the value of a function at a particular point
        def fval(val):
            func = funct
            try:
                func = D.insert_mult(func)
                for i in re.finditer(r'(?P<f1>[a-wA-Zyz]+)(?P<r1>\^[\d]+)',func):
                    if i.group('f1') != 'e':
                        pow1 = i.group('r1')
                        infunc = D.brackfunc(func[i.end('r1'):])
                        func = func[:i.end('r1')+len(infunc)] + pow1 + func[i.end('r1')+len(infunc):]
                        func = func[:i.start('r1')] + func[i.end('r1'):]
                func = func.replace('^','**')
                func = func.replace('x',str(val))
                return eval(func)
            except ZeroDivisionError:
                msg.showerror('Division Error!','No dividing by 0')
        
        if val != '': #returns the value of the function at val or funct(val)
            return fval(val)
        else:
            return fval #returns the function


    @staticmethod
    def simplify(func): #simplifies a term like combining powers, calculating the const of the term, etc.
        i = re.search(r'(?P<f1>[a-wA-Zyz]+)(?P<pow1>\^[\d]+)?\(x\).*?(?<![a-wA-Z1-9yz/\^][(])(?P=f1)(?P<pow2>\^[\d]+)?(?P<x1>\(x\))',func)#to find 'f(x)...f(x)'
        while i and i.group('f1') in D.deridict.keys():
            power = 0 #total power of a factor in term like sin^3(x)
            for j in [i.group('pow1'),i.group('pow2')]:
                if j != None:
                    power += int(j[1:])
                else:
                    power += 1
            if i.end('pow1') == -1:
                pow1end = i.end('f1')
            else:
                pow1end = i.end('pow1')
            if i.start('pow2') == -1:
                pow2start = i.start('x1')
                pow2end = pow2start
            else:
                pow2start = i.start('pow2')
                pow2end = i.end('pow2')
            check_mult = i.start('x1') - (pow2end-pow2start) - len(i.group('f1'))-1
            if func[check_mult-1:check_mult+1] == '*-':
                func = func[:check_mult-1] + func[check_mult:]
                pow2start -= 1
                pow2end -= 1
                
            if func[check_mult] == '*':
                func = func[:check_mult] + func[check_mult+1:]
                pow2start -= 1
                pow2end -=1
            
            lf = len(func[i.start('f1'):i.end('f1')])
            func = func[:i.start('f1')] + func[(pow1end+3):(pow2start-lf)] + func[(pow2end+3):]
            func = i.group('f1')+'^'+str(power)+'(x)'+func
            i = re.search(r'(?P<f1>[a-wA-Z^yz]+)(?P<pow1>\^[\d]+)?\(x\).*?(?P=f1)(?P<pow2>\^[\d]+)?(?P<x1>\(x\))',func)

        const = 1 #calculating product of constants in term like 4*5
        m = re.search(r'(?<!\^)(?P<mult>\*)?(?P<n1>[\d]+)',func) #pattern to find constants in term
        while m:
            if m.end('n1') != len(func):
                if func[m.start('n1'):m.end('n1')+1] == '1/':
                    break
            if re.match(r'x\).*', func[m.end('n1'):]):
                    break
            else:
                n1start = m.start('n1')
                n1end = m.end('n1')
                if m.group('mult'):
                    func = func[:m.start('mult')] + func[m.end('mult'):]
                    n1start -= 1
                    n1end -= 1
                const *= int(m.group('n1'))
                func = func[:n1start] + func[n1end:]
            m = re.search(r'(?<!\^)(?P<mult>\*)?(?P<n1>[\d]+)',func)
        if const != 1:
            func = str(const)+func #function is modified like 5*7*sin^2(x) becomes 35*sin^2(x)
            
        sign_count = func.count('-') #to handle multiple '-' signs in a term
        signstr = '-' * sign_count
        func = func.replace('-','')
        signstr = D.sign_manager(signstr)
        func = signstr + func
        return func
        
    @staticmethod
    def fract_reducer(frac): # returns a rational p/q form of a float number having 2 decimal places
        num = int(frac*100)
        if num == 0:
            den = 1
        else:
            den = 100
        for i in range(2,min(den,num)): #removes common factors
            while num%i==0 and den%i==0:
                num/=i
                den/=i

        return (int(num),int(den)) # returns a tuple of p,q where p/q = frac
    
    def analyser(self):#separates functions according to + and - signs and appends them to self.flist
        self.flist = re.split('(\+|\-)',self.f)
        self.flist = list(filter(lambda s: s!='',self.flist))
        nums_removed_list = [] # removes constants in the function as their derivative is 0
        for i in range(len(self.flist)):
            if re.fullmatch('[\d]+',self.flist[i]):
                if i != 0:
                    del(nums_removed_list[-1])
            else:
                nums_removed_list.append(self.flist[i])
        if nums_removed_list == []:
            self.__deri = '0'
        self.flist = nums_removed_list
        flst = []
        for i in range(len(self.flist)):
            if (self.flist[i] != '+' and self.flist[i] != '-') and i != 0:
                flst.append(self.flist[i-1]+self.flist[i])
            else:
                flst.append(self.flist[i])
        self.flist = flst        
       
    def chainrule(self, func): # calculates d /dx (f(g(...(x))))
        cr = ''
        fsep = re.split(r'(\)|\()',func) # for eg, 'cos(x)sin(x)' becomes ['cos', '(', 'x', ')', 'sin', '(', 'x', ')', '']
        fsep = list(filter(lambda s: s!='',fsep)) #to remove the unwanted empty strings in list
        sub = 0
        for i in range(len(fsep)):
            raised = re.search(r'(?<=\^)(?P<r1>\d+)',fsep[i]) #pattern to check if f(x)^n in function
            check_const = re.match(r'(?P<c>[\d]+)',fsep[i]) #pattern to check if constants present in function
            if check_const:
                const = check_const.group('c')
                cr += const
                cr += '*'
                if re.match('\*', fsep[i][len(const):]):
                    fsep[i] = fsep[i][:len(const)] + fsep[i][len(const)+1:]
                fsep[i] = fsep[i][check_const.end('c'):]
                
            if fsep[i] in D.deridict.keys(): # manages terms like 'sin', 'cos', etc. to get chainrule
                cr1 = ''
                if i != 0:
                    cr1 += '*'
                if (fsep[i]=='log') and (i!=0 and D.listjoin(fsep,i+1,len(fsep)-sub)!='(x)'):
                    cr1 += '/(x)'
                else:
                    cr1 += D.deridict[fsep[i]]
                cr1 = cr1.replace('(x)',D.listjoin(fsep,i+1,len(fsep)-sub))
                cr += cr1
                sub += 1

            elif raised: #if there is a function raised to any power
                cr1 = ''
                n = raised.group('r1')
                if n =='2':
                    p = ''
                else:
                    p = '^'+str(int(n)-1)
                if i != 0:
                    cr1 += '*'
                cr1 += (n + '*' + fsep[i][:-len(n)-1] + p)
                if fsep[i][:-len(n)-1] != 'x':
                    innerfunc = D.listjoin(fsep,i+1,len(fsep)-sub)
                    cr1 += innerfunc + '*'
                    cr1 += D.deridict[fsep[i][:-len(n)-1]].replace('x',innerfunc[1:-1])
                cr += cr1
                sub += 1
        return cr
    
    def productrule(self,func): # calculates d /dx (uvw...)
        if func[0] == '+':
            sgn = '+'
            func = func[1:]
        elif func[0] == '-':
            sgn = '-'
            func = func[1:]
        else:
            sgn = '+'
            
        const = re.match(r'(?P<c>\d+)[*]',func)
        if const:            
            func = func[:const.start('c')] + func[const.end('c')+1:]
            const = const.group('c')
        else:
            const = ''
        prlist = func.split('*') #splits the function according to * like 'sin(x)*cos(x)' gives ['sin(x)', 'cos(x)']
        prdlist = [] #list containing derivative of uvw... one at a time like du v w, u dv w, u v dw, and so on.
        for i in range(len(prlist)):
            prdterm = ''
            if const:
                prdterm += (const+'*')
            prdterm += D.listjoin(prlist, 0, i)
            prdterm += self.chainrule(prlist[i])
            prdterm += D.listjoin(prlist, i+1, len(prlist))
            prdterm = D.simplify(prdterm)
            prdlist.append(prdterm)
        pr = D.listjoin(prdlist, 0, len(prdlist),sgn) #string which contains the total product rule (sum of derivatives in prdlist)
        if sgn == '-':
            pr = '-' + pr
        return pr
                       
            
    def __show(self,remove_mult=True): #simplifies and returns the derivative string, self.__deri        
        if self.__deri != '' and self.__deri[0] == '+':
            self.__deri = self.__deri[1:]
            
        self.__deri = D.sign_manager(self.__deri) #simplify any ambigious signs in self.__deri
        
        self.__deri = self.__deri.replace('+',' + ') #space added between signs to make it look nicer
        self.__deri = self.__deri.replace('-',' - ')
        remove_mult=True
        if remove_mult:
            self.__deri = re.sub(r'([\d]+)([*]1/)',r'\1/',self.__deri)
            self.__deri = self.__deri.replace('*','') # turns all * into '' because * sign is ignored in a term
        return self.__deri
    
    def derivative(self, remove_mult=True): #method that calculates the derivative of a function        
        if '/' in self.f:
            u,v = self.f.split("/")[0:2] #checks for quotient rule
            return self.quotientrule(u, v)
        self.f = D.insert_mult(self.f) #inserts * at appropriate places for productrule
        self.analyser() #separates terms according to + and - signs and appends them to self.flist
        for i in self.flist:
            if i == '+' or i == '-': #add the sign before a term directly to the derivative
                self.__deri += '+'
            elif i == 'x':
                self.__deri += '1'
            else:
                self.__deri += self.productrule(i) #calculate the productrule of the term
                
        if remove_mult:
            return self.__show() #returns the derivative as a string
        else:
            return self.__show(False)
        
    def quotientrule(self, u, v): #calculates d(u/v)
        u1 = D(u)
        v1 = D(v)
        t1 = (v+'*('+u1.derivative()+')').replace(' ','')
        t2 = (u+'*('+v1.derivative()+')').replace(' ','')
        self.__deri = '(' +t1+ '-' +t2+ ')/(' +v+ ')^2'  #* present in str for ease in value calculation. Replace * after * is added even after 
        return self.__show()

    def nth_deri(self,n): #calculates the nth derivative of a function
        nder = self.f
        for i in range(n):
            nder = D(nder)
            nder = nder.derivative()
        return nder

def d(func): #function for quickly testing derivatives
    dfunc = D(func)
    print(dfunc.derivative())

def testcases():
    #testing basic functions
    d('x^6 - 4x^3 + 7x - 8')
    d('cos^2(x) + sinh(x) -tan(x)')
    d('sin(x) + 4cosech(x) - 12log(x) - 34')
    #testing chainrule
    d('cos(sin(tan(e^(x))))')
    d('15sin(cos(log(x))) - 3sech(tan(x)) +441')
    d('9sin^3(cos(x))')
    #testing productrule
    d('-4sinh(x)cos(x)')
    d('15cosec(x)cot(x)')
    d('-5sin(x)cos(x) + 6 e^(x) log(x)')
    d('sin(x)cos(x)tan(x)')
    d('2x^8+ 14e^(x)sin(x)')
    d('12x^4 x^7')
    #testing quotientrule
    d('4sin(x)/cos(x)')
    d('sin(x)cos(x)/2x^6')
    #testing chainrule and productrule at same time
    d('xcos(e^(x))')
    d('3sin(cos(tan(x)))e^(x)')
    d('-log(tan(x))cos(x)')
    d('-3sin^2(e^(x))log(x)')

testcases()


def GUI(): #GUI is written inside function to have a choice of using/not using GUI
    w = Tk() #the main window which contains all widgets
    w.geometry('970x430') #defining dimensions of the window
    w.title('Derivative Calculator') #defining title of the window
    global state #for managing state of g(x) button in f(x)/g(x)
    state = 0


    def expand(): #shows the g(x) blank of the f(x)/g(x) on the screen
        global state, line, f_x
        state += 1
        state = state % 2
        if state == 1:
            line = Label(w, text = '_'*70)
            line.place(x = 150, y = 55)
            f_x = Entry(w, font = ('Times New Roman', 14), bd = 3, justify ='center', width = 40)
            f_x.grid(row = 1, column = 1)
        else:
            line.place_forget() #removes the g(x) box from the window
            f_x.grid_remove()
            del f_x

    def total_fx(): #return the total function given by the user
        try:
            if f_x.get() == '':
                return fx.get()
            
            f1 = f_x.get()
            if f1 == '0':
                raise ZeroDivisionError
            
            return fx.get()+'/'+f1
        except ZeroDivisionError:
            msg.showerror('Division Error!','No dividing by 0')
        except NameError:
            return fx.get()

    def diff_fx(): #Calculates derivative and shows it in appropriate box as output
        try:
            if total_fx() == '':
                msg.showerror('Invalid Input!','Please enter f(x)')

            d1 = D(total_fx())
            f1x_out.delete(0,END)
            f1x_out.insert(0,d1.derivative(False))
        except SyntaxError:
           msg.showerror('Invalid Input!','Please enter correct f(x)')
           
    def plot_fx(): #Plots the graph of the function
        try:
            plot(total_fx())
        except SyntaxError:
           msg.showerror('Invalid Input!','Please enter correct f(x)')
        except NameError:
           msg.showerror('Invalid Input!','Please enter correct f(x)')
        except ValueError:
            msg.showerror('Cannot plot function','Functions cannot take values out of its domain')
           
    def plot_f1x(): #Plots the graph of the derivative of the function
        try:
            d1 = D(total_fx())
            plot(d1.derivative())
        except SyntaxError:
           msg.showerror('Invalid Input!','Please enter correct f(x)')
        except ValueError:
            msg.showerror('Cannot plot function','Functions cannot take values out of its domain')

    def nth_der(): #Calculates the nth derivative and shows it in appropriate box as output
        try:
            n = int(n_in.get())
            d2 = D(total_fx())
            fnx_out.delete(0,END)
            fnx_out.insert(0,d2.nth_deri(n))
        except SyntaxError:
           msg.showerror('Invalid Input!','Please enter correct f(x)')
        
    def get_tan(): #Calculates the tangent equation and shows it in appropriate box as output
        try:
            xval = eval(x_coor.get())
            d1 = D(total_fx())
            slope = D.fvalue(d1.derivative(),xval)
            m = round(slope,2)
            p,q = D.fract_reducer(m)
            c = int(q * D.fvalue(total_fx(),xval) - p * xval)
            if q>0:
                q1 = ' - '+str(q)+'y'
            else:
                q1 = ' + '+str(q)+'y'
            if c>0:
                c1 = ' + '+str(c)+' = 0 '
            else:
                c1 = ' - '+str(c)+' = 0 '
            tan_eq = str(p)+'x'+q1+c1
            tan_eq = D.sign_manager(tan_eq)

            tan.delete(0,END)
            tan.insert(0,tan_eq)

            y = D.sign_manager('('+str(p)+'*x'+c1[:-4]+')/('+str(q)+')')
            return y
        except ZeroDivisionError:#SyntaxError
            msg.showerror('Division Error!','No dividing by 0')
        except SyntaxError:
            msg.showerror('Invalid Input!','Please enter correct f(x)')

    def get_nor(): #Calculates the normal equation and shows it in appropriate box as output
        try:
            xval = eval(x_coor.get())
            d1 = D(total_fx())
            slope = -1/D.fvalue(d1.derivative(),xval)
            m = round(slope,2)
            p,q = D.fract_reducer(m)
            c = int(q * D.fvalue(total_fx(),xval) - p * xval)
            if q>0:
                q1 = ' - '+str(q)+'y'
            else:
                q1 = ' + '+str(q)+'y'
            if c>0:
                c1 = ' + '+str(c)+' = 0 '
            else:
                c1 = ' - '+str(c)+' = 0 '
            nor_eq = str(p)+'x'+q1+c1
            nor_eq = D.sign_manager(nor_eq)

            nor.delete(0,END)
            nor.insert(0,nor_eq)

            y = D.sign_manager('('+str(p)+'*x'+c1[:-4]+')/('+str(q)+')')
            return y
        except ZeroDivisionError:#SyntaxError
            msg.showerror('Division Error!','No dividing by 0')
        except SyntaxError:
            msg.showerror('Invalid Input!','Please enter correct f(x)')
    
    def plot_tan(): #Plots the tangent equation and function given by user
        try:
            plot(get_tan(),total_fx())
        except SyntaxError:
           msg.showerror('Invalid Input!','Please enter correct f(x)')
        except ValueError:
            msg.showerror('Cannot plot function','Functions cannot take values out of its domain')

    def plot_nor(): #Plots the normal equation and function given by user
        try:
            plot(get_nor(),total_fx())
        except SyntaxError:
           msg.showerror('Invalid Input!','Please enter correct f(x)')
        except ValueError:
            msg.showerror('Cannot plot function','Functions cannot take values out of its domain')


    def quitb(): #A quit button to close the GUI
        if msg.askokcancel('Quit','Do you want to quit?'):
            w.destroy()
            
    #Defining the appropriate input, output and display boxes in the GUI
    Label(w, text = 'Enter  f(x)  = ', font = ('Times New Roman', 14), padx=10, pady=30, fg='blue').grid(column = 0, row = 0) #Enter f(x) = 
    
    fx = Entry(w, font = ('Times New Roman', 14), justify='center', bd = 3, width = 40) #f(x) numerator input
    fx.grid(row = 0, column = 1)

    showdenom = Button(w, text='f(x)/g(x)', font=('Times New Roman', 14),bg='#D4FB90', width=7, bd=3, command=expand) #f(x)/g(x) Button
    showdenom.place(x=25, y=60)

    Label(w, text = "f '(x) = ", font = ('Times New Roman', 14), padx=10, fg='blue').grid(row=3, column=0) #f'(x) = 

    f1x_out = Entry(w, font=('Times New Roman', 14), width=45, bd=3, justify='center') #display f'(x)
    f1x_out.grid(row = 3, column = 1)

    diff = Button(w, text=' Differentiate! ', font=('Times New Roman', 14), bg='#D4FB90', width=10, bd=3, command=diff_fx) #Differentiate Button
    diff.grid(row=5, column=1)

    fx_plot = Button(w, text="Plot f (x)", font=('Times New Roman', 14), width=7, bg='#D4FB90', bd=3, command=plot_fx) #Plot f(x) Button
    fx_plot.grid(row=2, column=1)

    f1x_plot = Button(w, text="Plot f '(x)", font=('Times New Roman', 14), width=7, bg='#D4FB90', bd=3, command=plot_f1x) #Plot f'(x) Button
    f1x_plot.grid(row=6, column=1)

    Label(w, text = 'Enter  n = ', font = ('Times New Roman', 14), pady = 20, fg='blue').grid(column = 0, row = 7) #Enter n = 
    
    n_in = Entry(w, font=('Times New Roman', 14), bd=3, width=15,)# n val input
    n_in.grid(row = 7, column = 1)

    Label(w, text = "f⁽ⁿ⁾(x) = ", font = ('Times New Roman', 14), padx=10, fg='blue').grid(row=8, column=0) #f⁽ⁿ⁾(x) = 

    fnx_out = Entry(w, font=('Times New Roman', 14), bd=3, width=45) #display f⁽ⁿ⁾(x)
    fnx_out.grid(row = 8, column = 1)

    calc_n_der = Button(w, text='Calculate nᵗʰ Derivative!', font=('Times New Roman', 14), bg='#D4FB90',  bd=3, command=nth_der) #Calculate nᵗʰ derivative Button
    calc_n_der.grid(row=9, column=1)

    Label(w, text = 'Enter x coordinate :  ', font = ('Times New Roman', 14), padx= 10, fg='blue').grid(column = 2, row = 0) #Enter x coordinate:

    x_coor = Entry(w, font=('Times New Roman', 14), bd=3, width=15) #x coordinate input
    x_coor.grid(row = 0, column = 3)

    Label(w, text = 'Tangent Equation of f(x) is :  ', font = ('Times New Roman', 14), padx= 10, fg='blue').grid(column = 2, row = 1) #Tangent Equation f(x) is: 

    tan = Entry(w, font=('Times New Roman', 14), bd=3, width=15) #Display tangent equation
    tan.grid(row = 1, column = 3)

    Label(w, text = 'Normal Equation of f(x) is :  ', font = ('Times New Roman', 14), padx= 10, fg='blue').grid(column = 2, row = 2) #Normal Equation f(x) is: 

    nor = Entry(w, font=('Times New Roman', 14), bd=3, width=15) #Display normal equation
    nor.grid(row = 2, column = 3)

    tan_get = Button(w, text="Get Tangent!", font=('Times New Roman', 14), bd=3, bg='#D4FB90', command=get_tan) #Get tangent Button
    tan_get.grid(row=3, column=2)

    nor_get = Button(w, text="Get Normal!", font=('Times New Roman', 14), bd=3, bg='#D4FB90', command=get_nor) #Get normal Button
    nor_get.grid(row=3, column=3)

    tan_plot = Button(w, text="Plot tangent of f(x)!", font=('Times New Roman', 14), bd=3, bg='#D4FB90', command=plot_tan) #Plot tangent of f(x) Button
    tan_plot.grid(row=5, column=2)

    nor_plot = Button(w, text="Plot normal of f(x)!", font=('Times New Roman', 14), bd=3, bg='#D4FB90', command=plot_nor) #Plot normal of f(x) Button
    nor_plot.grid(row=5, column=3)

    quitbutton = Button(w, text="Quit!", font=('Bold Times New Roman', 14), bg='#FF4B4B', fg='white', width=10, bd=3, command=quitb) #Plot normal of f(x) Button
    quitbutton.grid(row=7, column=2)

    w.mainloop() #infinite loop of the GUI that runs in the background to detect user interaction

GUI() #calling the GUI() enables us to run the GUI. Can skip GUI by commenting this line


