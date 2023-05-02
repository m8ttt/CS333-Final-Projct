#!/usr/bin/env python3

# Matthew Tang
# 10/31/22
# CS457
# Programming Assignment 2: Basic Data Manipulation

import os
import shutil

home_directory = os.getcwd()

class ElementNotFoundError (Exception):
    pass
class WrongSingleQuotes (Exception):
    pass
class IncorrectFormat (Exception):
    pass


def ListToEquation(equation):
    if(equation[1] == '='):
        equation[1] = equation[1] + equation[1]
    
    if(equation[2].isnumeric()):
        if (eval(ListToString(equation))):
            return True
        else:
            return False
        
    else:
        equation = ListToString(equation).replace("'", "")
        equation = equation.split()
        
        if(equation[1] == '=='):
            if(str(equation[0]) == str(equation[2])):
                return True
            else:
                return False
            
        if(equation[1] == '!='):
            if(str(equation[0]) != str(equation[2])):
                return True
            else:
                return False
            
        elif(equation[1] == '>'):
            if(str(equation[0]) > str(equation[2])):
                return True
            else:
                return False
            
        else:
            if(str(equation[0]) < str(equation[2])):
                return True
            else:
                return False

def FindIndex(table, element):
    header = OBTAIN_HEADER(table)
    sub_list = header.split()
    index = sub_list.index(element)
    return int(index/3)

def CLEAN_FILE(table):
    file = open(table, "r")
    data = file.read().rstrip('\n')
    file.close()
 
    file = open(table, "w")
    file.write(data)
    file.close()

def OBTAIN_TUPLES(table):
    file = open(table, "r")
    header = file.readline()
    lines = file.readlines()
    file.close()
    return lines
   
def OBTAIN_HEADER(table):
    file = open(table, "r")
    header = file.readline()
    file.close()
    return header

def DELETE_TUPLE(table, equation):
    try:     
        if not os.path.exists(table):
            raise FileNotFoundError

        delete_counter = 0
        ElementCheck(table, equation[0])
        where_datatype_index = FindIndex(table, equation[0])
        header = OBTAIN_HEADER(table)
        lines = OBTAIN_TUPLES(table)
        
        file = open(table, "w")
        file.write(header)

        for tuples in lines:
            if(WHERE_TEST (where_datatype_index, tuples, ListToString(equation[1:]))):
                delete_counter = delete_counter + 1
            else:
                file.write(tuples)
                delete_counter = delete_counter
        file.close()

        CLEAN_FILE(table)

        if(delete_counter == 1):
            print('{0} record deleted.'.format(delete_counter))
        else:
            print('{0} records deleted.'.format(delete_counter))

    except FileNotFoundError:
        print("!Failed to alter table {0} because it does not exist.".format(table))
    except ElementNotFoundError:
        print("!Failed to query because {0} does not exist in table {1}.".format(equation[0] ,table))

def UPDATE_TABLE(table, then_EQ, if_EQ):
    try: 
        if not os.path.exists(table):
            raise FileNotFoundError
        
        modified_counter = 0
        temp_list = ' '
        temp_list = temp_list.split()
        header = OBTAIN_HEADER(table)
        lines = OBTAIN_TUPLES(table)
        
        element = if_EQ[0]
        ElementCheck (table, element)
        element = then_EQ[0]
        ElementCheck (table, element)
        
        where_datatype_index = FindIndex(table, if_EQ[0])
        set_index = FindIndex(table, then_EQ[0])
      
        file = open(table, "w")
        file.write(header)

        for tuples in lines:
            tuples = tuples.split()
            if (WHERE_TEST (where_datatype_index, ListToString(tuples), ListToString(if_EQ[1:]))):
                modified_counter = modified_counter + 1
                tuples[set_index * 2] = then_EQ[2]
            file.write(ListToString(tuples))
            file.write('\n') 

        file.close()

        CLEAN_FILE(table)

        if(modified_counter == 1):
            print('{0} record modified.'.format(modified_counter))
        else:
            print('{0} records modified.'.format(modified_counter))

    except FileNotFoundError:
        print("!Failed to alter table {0} because it does not exist.".format(table))
    except ElementNotFoundError:
        print("!Failed to query because {0} does not exist in table {1}.".format(element, table))

def INSERT_TABLE(table, arguments):
    try:     
        if not os.path.exists(table):
            raise FileNotFoundError

        arguments = arguments[arguments.find('(')+1:arguments.rfind(')')]
    
        file = open(table, "a")
        file.write('\n')
        for i in arguments:
            if(i == ','):
                file.write(' | ')
            else:
                file.write(i)
        file.close()
        print('1 new record inserted.')
   
    except FileNotFoundError:
        print("!Failed to alter table {0} because it does not exist.".format(table))

def CREATE_TABLE(new_table, arguments):
    try:
        if os.path.exists(new_table):
            raise FileExistsError
        file = open(new_table, "w+")
        info = arguments[arguments.find('(')+1:arguments.rfind(')')]
        
        for i in info:
            if(i == ','):
                file.write(' |')
            else:
                file.write(i)
        print('Table {0} created.'.format(new_table))
        file.close()
    
    except FileExistsError:
        print("!Failed to create table {0} because it already exists.".format(new_table))

def ALTER_TABLE(table, new_element):
    try:    
        if not os.path.exists(table):
            raise FileNotFoundError
        file = open(table, "a+")
        file.write(' | ' + new_element)
        file.close()
        print('Table {0} modified.'.format(table))
   
    except FileNotFoundError:
        print("!Failed to alter table {0} because it does not exist.".format(table))

def WHERE_TEST(element_where_index, tuples, EQ): 
    tuples = tuples.split()
    tuple_check = tuples[element_where_index * 2] + ' ' + EQ
    tuple_check = tuple_check.split()
     
    if(ListToEquation(tuple_check)):
        return True 
    else:
        return False

def SPECIFICS(tuples, output_elements, table):
    iterator = 0
 
    for search in output_elements: 
        search_index = FindIndex(table, search) * 2      
        print(tuples.split()[search_index], end='')
                            
        if(iterator < len(output_elements) -1 ):                   
            print('|' , end='') 
        else:
            print()

        iterator = iterator + 1


def SELECT_TABLE(command):
    try: 
        index_of_from = command.index('from')
        table = command[index_of_from + 1]
        header = OBTAIN_HEADER(table)
        lines = OBTAIN_TUPLES(table)
        wrong_element = ''
       
        if not os.path.exists(table):
            raise FileNotFoundError
  
        if('where' in command):
           command_where_index = command.index('where')
           element = command[command_where_index+1]
           ElementCheck(table, element)
           where_datatype_index = FindIndex(table, command[command_where_index+1])
           right_half_of_EQ = ListToString(command[command_where_index+2:command_where_index+4])
           
        if (command[1] == '*' and len(command) == 4):
            file = open(table, "r")
            print(file.read())
            file.close()
        
        elif (command[1] == '*' and 'where' in command):
            print(header, end='')
            for tuples in lines:
                if (WHERE_TEST (where_datatype_index, tuples, right_half_of_EQ)):
                    print(tuples, end='')

        else:
            outputs = command[1:index_of_from]
            outputs = ListToString(outputs).replace(',', '')
            outputs = outputs.strip()      
            outputs = outputs.split()
            
            try:
                for search in outputs:  
                    if (search not in header): 
                        wrong_element = search 
                        raise ElementNotFoundError         
                
                iterator = 0
                header_list = header.split()
                
                for search in outputs:
                    head_search_index = FindIndex(table, search) * 3                 
                    print(header_list[head_search_index], end=' ')
                    print(header_list[head_search_index + 1], end='') 
                    
                    if(iterator < len(outputs) -1 ):                              
                        print(' | ' , end='')
                    else:
                        print()
                    iterator = iterator + 1 

                for tuples in lines:
                     if ('where' in command and WHERE_TEST (where_datatype_index, tuples, right_half_of_EQ)):
                        SPECIFICS(tuples, outputs, table)
                     if ('where' not in command):
                        SPECIFICS(tuples, outputs, table)
            except ElementNotFoundError:
                print("!Failed to query because {0} does not exist in table {1}.".format(wrong_element ,table))

    except FileNotFoundError:
         print("!Failed to query table {0} because it does not exist.".format(table))       
    except ElementNotFoundError:
         print("!Failed to query because {0} does not exist in table {1}.".format(element, table))
    
def DROP_TABLE(user_file):
    try:
        os.remove('{0}/{1}'.format(os.getcwd(), user_file))
        print('Table {0} deleted.'.format(user_file))
   
    except FileNotFoundError:
        print("!Failed to delete {0} because it does not exist.".format(user_file))

def CREATE_DATABASE(new_database):
    try:
        os.chdir(home_directory)
        os.mkdir(new_database)
        print('Database {0} created.'.format(new_database))
    
    except FileExistsError:
        print("!Failed to create database {0} because it already exists.".format(new_database))

def DROP_DATABASE(user_directory):
    try:
        shutil.rmtree('{0}/{1}'.format(home_directory, user_directory))
        print('Database {0} deleted.'.format(user_directory))

    except FileNotFoundError:
        print("!Failed to delete {0} because it does not exist.".format(user_directory))

def USE(user_directory):
    try: 
        os.chdir('{0}/{1}'.format(home_directory, user_directory))
        print("Using database {0}.".format(user_directory))
   
    except FileNotFoundError:
        print("!Failed because database {0} does not exist.".format(user_directory))

def ListToString(list_element): 
    parameter_string = " "
    return(parameter_string.join(list_element))

def LowerAndConsiderQuotes(sentence):
     quote_count = 0
     new_sentence = ''
  
     for word in sentence:
        if(word == "'"):
           quote_count = quote_count + 1
        if(quote_count % 2 == 0):
            new_sentence = new_sentence + word.lower()       
        else:
            new_sentence = new_sentence + word
            
        new_sentence = new_sentence.replace("'", '')
     if(quote_count % 2 != 0):
        raise WrongSingleQuotes
     return new_sentence
 
def ElementCheck(table, element):
    header = OBTAIN_HEADER(table)
    if(element not in header):
        wrong_element = element
        raise ElementNotFoundError 
           
def StringEquationToList(Equation_String):   
    LEQ = ''
    prev_letter = ''
        
    for letter in Equation_String:
        if((letter == '=' and prev_letter == '') or letter == '>' or letter == '<'):
            LEQ = LEQ + ' ' + letter + ' '
            
        elif(letter == '!'):
            prev_letter = letter
            LEQ = LEQ + ' ' + letter
            
        elif(prev_letter == '!' and letter == '='):
            LEQ = LEQ + letter + ' '
            
        else: 
            LEQ = LEQ + letter

    LEQ = LEQ.strip()
    LEQ = LEQ.split()
        
    if(len(LEQ) > 3): 
        raise IncorrectFormat

    return LEQ

def FixEQFormat(user_input):
    if('where' in user_input): 
        where_input_index = user_input.index('where')        
        if(len(user_input) != where_input_index + 4):
            if(len(user_input) == where_input_index + 2):
                 Fixed_EQ = StringEquationToList(ListToString(user_input[where_input_index+1 : where_input_index + 2]))
                 old_EQ = ListToString(user_input[where_input_index+1 : where_input_index + 2])
                 user_input.remove(old_EQ)
                 user_input = user_input + Fixed_EQ
                 
            elif(len(user_input) == where_input_index + 3):
                 Fixed_EQ = StringEquationToList(ListToString(user_input[where_input_index+1 : where_input_index + 3]))
                 old_EQ_Left = user_input[where_input_index+1]
                 old_EQ_Right = user_input[where_input_index+2]
                 user_input.remove(old_EQ_Left)
                 user_input.remove(old_EQ_Right)
                 user_input = user_input + Fixed_EQ
                 
            else:
                 raise IncorrectFormat
             
    if('set' in user_input):
        set_input_index = user_input.index('set')
        if(len(user_input) !=  set_input_index + 8):
            if(len(user_input) == set_input_index + 6):
                 Fixed_EQ = StringEquationToList(ListToString(user_input[set_input_index+1 : set_input_index + 2]))
                 start_of_command = user_input[0 : set_input_index+1]
                 rest_of_command = user_input[set_input_index+2 : ]
                 user_input = start_of_command + Fixed_EQ + rest_of_command
                 
            elif(len(user_input) == set_input_index + 7):
                 Fixed_EQ = StringEquationToList(ListToString(user_input[set_input_index+1 : set_input_index + 3]))
                 start_of_command = user_input[0 : set_input_index+1]
                 rest_of_command = user_input[set_input_index+3: ]
                 user_input = start_of_command + Fixed_EQ + rest_of_command
                 
            else:
                 raise IncorrectFormat
             
    return user_input

def Main():
    while(True):
        user_input = ''
        user_input = user_input.strip()
        user_input = user_input.split()
        
        try:
            while(not ListToString(user_input).endswith(';')): 
                new_input = input('') 
                if('--' in new_input or len(new_input) == 0):
                    new_input = '' 
                else:
                    new_input = LowerAndConsiderQuotes(new_input)
                    new_input.strip()
                    
                    user_input = user_input + new_input.split()
                    
                    if(len(user_input) == 1 and user_input[0] == '.exit'):
                        print('All done.') 
                        exit()

            user_input = ListToString(user_input).replace(';',' ')
            user_input = user_input.split() 
            user_input = FixEQFormat(user_input) 
        
            if(ListToString(user_input) == '.exit'):  
                print('All done.') 
                exit()
            
            elif(len(user_input) == 2 and user_input[0] == 'use'):   
                USE(user_input[1])
                
            elif(len(user_input) == 3 and user_input[0] == 'create' and user_input[1] == 'database'): 
                CREATE_DATABASE(user_input[2])
                
            elif(len(user_input) == 3 and user_input[0] == 'drop' and user_input[1] == 'database'):  
                DROP_DATABASE(user_input[2])
                
            elif(len(user_input) == 3 and user_input[0] == 'drop' and user_input[1] == 'table'): 
                DROP_TABLE(user_input[2])
                
            elif(len(user_input) > 3 and user_input[0] == 'alter' and user_input[1] == 'table' and user_input[3] == 'add'):  
                ALTER_TABLE(user_input[2], ListToString(user_input[4:]))
                
            elif(len(user_input) > 3 and user_input[0] == 'create' and user_input[1] == 'table'): 
                CREATE_TABLE(user_input[2], ListToString(user_input[3:]))
                
            elif(user_input[0] == 'select' and 'from' in user_input): 
                SELECT_TABLE(user_input)
                
            elif(len(user_input) > 3 and user_input[0] == 'insert' and user_input[1] == 'into' and ( user_input[3].startswith("values(") or user_input[3].startswith("values") ) ):
                INSERT_TABLE(user_input[2], ListToString(user_input[3:]))
                
            elif(len(user_input) == 10 and user_input[0] == 'update' and user_input[2] == 'set' and user_input[6] == 'where'): 
                UPDATE_TABLE(user_input[1], user_input[3:6], user_input[7:])
                
            elif(len(user_input) == 7 and user_input[0] == 'delete' and user_input[1] == 'from' and user_input[3] == 'where'): 
                DELETE_TUPLE(user_input[2], user_input[4:])
                
            elif(len(user_input) == 0 ): 
                print (" ")
                
            else:
                print ("!Failed, please review documentation concerning acceptable commands")
                
        except WrongSingleQuotes:  
            print("!Failed because of unbalanced quotations")
        except IncorrectFormat:
            print("!Failed to query because equation (or element near equation) is in wrong format.") 
        except ElementNotFoundError:
            print("!Failed to query because {0} does not exist in table {1}.")

if __name__ == "__main__":      
    Main()