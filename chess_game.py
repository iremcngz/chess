import sys
import math
import os   
#assertions
class Error(Exception):
    pass
class UndefinedParameterError(Error):
    pass
class ParameterNumberError(Error):
    pass
class InvalidCharacterinInputFileError(Error):
    pass
class InputFileisEmptyError(Error):
    pass
class InputFilenotFoundError(Error):
    pass
class KeyFilenotFoundError(Error):
    pass
class KeyFileisEmptyError(Error):
    pass
class InvalidCharacterinKeyFileError(Error):
    pass
class InputFileCouldnotbeReadError(Error):
    pass
class KeyFileCouldnotbeReadError(Error):
    pass
def check_inputfile(inputpath):
    f=open(inputpath,'r',encoding='utf-8')
    alphabet='ABCDEFGHIJKLMNOPQRSTUVWXYZ '
    alphabet2='abcdefghijklmnopqrstuvwxyz '
    line= f.readline()
    listq=[]
    q=None
    for i in range(len(line)):
        if line[i] in alphabet or line[i] in alphabet2:
            q=1
            listq.append(q)
        else:
            q=0
            listq.append(q) 
    if (not 1) in listq:
        q=0                
    return q   
          
#for keyfile control with ,
def check_keyfile(inputpath):
    f=open(inputpath,'r',encoding='utf-8')#r-->r+
    numbers='1234567890,\n-'
    line= f.read()
    listq=[]
    q=None
    for i in range(len(line)):
        if line[i] in numbers:
            q=1
            listq.append(q)
        else:
            q=0
            listq.append(q) 
    if (not 1) in listq:
        q=0                
    return q               
def check_isinputfileempty(inputpath):
    f=open(inputpath,'r',encoding='utf-8')   #r-->r+
    if f.readline()=='':
        a=0
    else: 
        a=1
    return a        

#check input file empty or not
try:
    isempty_sysargv3=check_isinputfileempty(sys.argv[3])
except FileNotFoundError:
    pass
def search_inputfile(inputfile):
    try:
        open(inputfile)
        a=1
    except:
        a=0    
    return a        
#convert the message to number
def get_message():
    message=''
    f=open(sys.argv[3])
    for line in f.readlines():
        line=line.upper()
        message+=str(line)+'\n'
    return message               
def just_convert_message(message):#message=get_message
    numbersofmessage=[]
    alphabet='ABCDEFGHIJKLMNOPQRSTUVWXYZ '
    for i in message:
        if i in alphabet:
          position=alphabet.find(i)
          numbersofmessage.append(position+1)
    return numbersofmessage        
#convert numbers to message
def just_convert_numbers(listnumbers):
    letters_of_message=''
    dict_for_numbers={
        1:'A',2:'B',3:'C',4:'D',5:'E',6:'F',7:'G',8:'H',9:'I',10:'J',11:'K',12:'L',13:'M',14:'N',15:'O',16:'P',17:'Q',18:'R',19:'S',20:'T',21:'U',22:'V',23:'W',24:'X',25:'Y',26:'Z',27:' '
    }
    for i in range(len(listnumbers)):
        letters_of_message += dict_for_numbers[listnumbers[i]]
    return letters_of_message
            
#get key1 
def get_key1_matrix():
    f=open(sys.argv[2])
    matrix=[]
    for line in f.readlines():
        numbers=[]
        for number in line.replace('\n','').split(','):
            try:
                numbers.append(int(number))
            except:
                pass    
        matrix.append(numbers)                
    return matrix     
#len key1 len message's letter
if sys.argv[1]=='enc': #add if
    try:
        a=just_convert_message(get_message()) 
        key1_len=int(len(get_key1_matrix())) 
        message_len=int(len(a))
    except ValueError:
        pass
    except FileNotFoundError:
        pass
try:
    key1_len=int(len(get_key1_matrix()))
except:
    pass
#matrix oluşturma
def createMatrix(rowCount, colCount, dataList):
    mat = []
    for i in range(rowCount):
        rowList = []
        try:
            for j in range(colCount):
              rowList.append(dataList[colCount * i + j])
        except:
             for j in range(int(key1_len)-len(rowList)):
              rowList.append(27)
        mat.append(rowList)

    return mat
#matrix inverse,minors,determinant

def find_minors(matrix):    
    if len(matrix)==3:
        minors1=[]
        minors2=[]
        minors3=[]
        minors4=[]
        minors5=[]
        minors6=[]
        minors7=[]
        minors8=[]
        minors9=[]
        for i in range(1,3):
            minors1.append(list([matrix[i][1],matrix[i][2]]))
        for i in range(1,3):
            minors2.append(list([matrix[i][0],matrix[i][2]]))   
        for i in range(1,3):
            minors3.append(list([matrix[i][0],matrix[i][1]]))
        for i in (0,2):
            minors4.append(list([matrix[i][1],matrix[i][2]]))
        for i in (0,2):
            minors5.append(list([matrix[i][0],matrix[i][2]]))
        for i in (0,2):
            minors6.append(list([matrix[i][0],matrix[i][1]]))
        for i in range(2):
            minors7.append(list([matrix[i][1],matrix[i][2]]))
        for i in range(2):
            minors8.append(list([matrix[i][0],matrix[i][2]]))
        for i in range(2):
            minors9.append(list([matrix[i][0],matrix[i][1]]))      
    return minors1,minors2,minors3,minors4,minors5,minors6,minors7,minors8,minors9  
def calculate_determinant(matrix):
    if len(matrix) == 2:
        return matrix[0][0]*matrix[1][1]-matrix[0][1]*matrix[1][0] 
    if len(matrix)==3:
        determinant=0
        for i in range(len(matrix)):
            determinant+=((-1)**(i))*matrix[0][i]*calculate_determinant(find_minors(matrix)[i])
    return determinant     
def transposeMatrix(m):
    return list(map(list,zip(*m)))
def find_inverse_matrix(matrix):
    cofactors=[]
    #cofactor_matrix=[]
    for i in range(len(matrix)**2):
        cofactors.append(((-1)**(i))*calculate_determinant(find_minors(matrix)[i]))
    cofactor_matrix=[]
    count=0
    for i in range(len(matrix)):
        row=[]
        for _ in range(len(matrix)):
            row.append((1/calculate_determinant(matrix))*cofactors[count])
            count+=1
        cofactor_matrix.append(row)    
    transpose_matrix=transposeMatrix(cofactor_matrix)
    return transpose_matrix
def calculate_inverse(matrix):
    if len(matrix) == 2:
        determinant=calculate_determinant(matrix)
        return [[matrix[1][1]/determinant, -1*matrix[0][1]/determinant],
                [-1*matrix[1][0]/determinant, matrix[0][0]/determinant]]
    if len(matrix)==3:
        return find_inverse_matrix(matrix)     
         
try:
    if sys.argv[1] !=  'enc' and sys.argv[1] != 'dec':
     raise UndefinedParameterError
    if len(sys.argv)!=5:
       raise ParameterNumberError
    if sys.argv[3][-3:] != 'txt':
       raise InputFileCouldnotbeReadError
    if sys.argv[2][-3:] != 'txt':
        raise KeyFileCouldnotbeReadError
    if search_inputfile(sys.argv[3])==0:
        raise InputFilenotFoundError
    if search_inputfile(sys.argv[2])==0:
        raise KeyFilenotFoundError
    
except UndefinedParameterError:
    print("Undefined Parameter Error")
except ParameterNumberError:
    print("Parameter Number Error")
except InputFileCouldnotbeReadError:
    print("The Input File Could not be Read Error")
except InputFilenotFoundError:
    print("Input file not found Error") 
except KeyFilenotFoundError:
    print("Key file not found Error")    
except KeyFileCouldnotbeReadError:
    print("Key File Could not be Read Error")                      
else:
    try:
        if check_isinputfileempty(sys.argv[2])==0:
            raise KeyFileisEmptyError
        if sys.argv[1]=='enc':
            if check_inputfile(sys.argv[3])==0:
                raise InvalidCharacterinInputFileError
            elif check_keyfile(sys.argv[2])==0:
                raise InvalidCharacterinKeyFileError  #added
        if isempty_sysargv3==0:
            raise InputFileisEmptyError
        if check_keyfile(sys.argv[2])==0:
            raise InvalidCharacterinKeyFileError
       
    except InvalidCharacterinInputFileError:
        print("Invalid Character in Input File Error")
    except InputFileisEmptyError:
        print("Input File is Empty Error")      
    except KeyFileisEmptyError:
        print("Key File is Empty Error")   
    except InvalidCharacterinKeyFileError:
        print("Invalid Character in Key File Error")
    
    else:   
        key1_len=int(len(get_key1_matrix()))
        if sys.argv[1]=='enc':
            mat = createMatrix(math.ceil(len(a)/key1_len),key1_len,a) 
            A=mat
            B=get_key1_matrix()
            C = [[0 for i in range(key1_len)] for i in range(math.ceil(len(a)/key1_len))]
            
            for i in range(math.ceil(len(a)/key1_len)):
                for j in range(key1_len):
                   for k in range(key1_len):
                       C[i][j] += A[i][k] * B[j][k]  
            #making output_enc.txt
            new_file=open(sys.argv[4],'w+')
            for i in range(len(C)):
                for j in range(len(C[i])):
                    new_file.write(str(C[i][j]))
                    new_file.write(',')
            new_file.seek(new_file.tell()-1,os.SEEK_SET)
            new_file.truncate() #to remove last ',' from output_enc.txt
            new_file.close()
        if sys.argv[1]=='dec':
            with open(sys.argv[3]) as ciphertext:
                listcipher=[] #[41, 61, 22, 23, 25, 36, 55, 69, 61, 84]
                for i in ciphertext.readline().split(','):
                    i=int(i) 
                    listcipher.append(i)  
                #creat matrix    
                matrix=createMatrix(math.ceil(len(listcipher)/key1_len),key1_len,listcipher)
                A=matrix
                #inverse
                B=calculate_inverse(get_key1_matrix())
                C = [[0 for i in range(key1_len)] for i in range(math.ceil(len(listcipher)/key1_len))]
                for i in range(math.ceil(len(listcipher)/key1_len)):
                    for j in range(key1_len):
                        for k in range(key1_len):
                            C[i][j] += A[i][k] * B[j][k] 
                listC=[] 
                for i in range(len(C)):
                    for k in range(key1_len):
                        listC.append(round(C[i][k]))
                #find the message
                str_of_outputdec=just_convert_numbers(listC)#message
                
                with open(sys.argv[4],'w+') as output:
                    output.write(str_of_outputdec)
                
            
    
      
         
    