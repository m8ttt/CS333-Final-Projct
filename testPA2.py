import PA2
import unittest
import os
import io
import sys
sys.path.append('..')
from unittest.mock import patch

home_directory = os.getcwd()

class TestBasicDataManipulation(unittest.TestCase):
    
    def test_ListToEquation_Evaluation(self):
        self.assertEqual(PA2.ListToEquation(['3', '+', '2']), True)
        self.assertEqual(PA2.ListToEquation(['3', '-', '2']), True)
        self.assertEqual(PA2.ListToEquation(['3', '*', '2']), True)
        self.assertEqual(PA2.ListToEquation(['6', '/', '2']), True)
        self.assertEqual(PA2.ListToEquation(['6', '%', '4']), True)
    
    def test_ListToEquation_Comparison(self):
        self.assertEqual(PA2.ListToEquation(['2', '==', '2']), True)
        self.assertEqual(PA2.ListToEquation(['2', '==', '3']), False)
        self.assertEqual(PA2.ListToEquation(['2', '!=', '3']), True)
        self.assertEqual(PA2.ListToEquation(['2', '!=', '2']), False)
        self.assertEqual(PA2.ListToEquation(['2', '>', '1']), True)
        self.assertEqual(PA2.ListToEquation(['2', '>', '2']), False)
        self.assertEqual(PA2.ListToEquation(['1', '<', '2']), True)
        self.assertEqual(PA2.ListToEquation(['2', '<', '2']), False)
    
    def test_ListToString(self):
        self.assertEqual(PA2.ListToString(['Hello', 'world']), "Hello world")
        self.assertEqual(PA2.ListToString(['Hello', "world's"]), "Hello world's")
        self.assertEqual(PA2.ListToString(['Hello', '123']), "Hello 123")
        
    def setUp(self):
        # create a sample table/file for testing
        self.table = 'test_table.txt'
        self.header = 'pid int | name varchar(20) | price float\n'
        self.rows = [
            '1 | Gizmo | 19.99\n',
            '2 | PowerGizmo | 29.99\n',
            '3 | SingleTouch | 149.99\n',
            '4 | MultiTouch | 199.99\n',
            '5 | SuperGizmo | 49.99\n'
        ]
        with open(self.table, 'w') as f:
            f.write(self.header)
            f.writelines(self.rows)
    
    def tearDown(self):
        os.remove(self.table)
    
    def test_CLEAN_FILE(self):
        # make sure CLEAN_FILE removes the trailing newline character
        PA2.CLEAN_FILE(self.table)
        with open(self.table, 'r') as f:
            data = f.read()
            self.assertNotEqual(data[-1], '\n')
    
    def test_OBTAIN_TUPLES(self):
        # make sure OBTAIN_TUPLES returns the expected list of rows
        rows = PA2.OBTAIN_TUPLES(self.table)
        self.assertEqual(rows, self.rows)
    
    def test_OBTAIN_HEADER(self):
        # make sure OBTAIN_HEADER returns the expected header string
        header = PA2.OBTAIN_HEADER(self.table)
        self.assertEqual(header, self.header)
        
    def test_FindIndex(self):
        # test finding the index of a valid element in the header
        index = PA2.FindIndex(self.table, 'name')
        self.assertEqual(index, 1)
        
        # test finding the index of a different valid element
        index = PA2.FindIndex(self.table, 'price')
        self.assertEqual(index, 2)
        
        # test finding the index of an invalid element
        with self.assertRaises(ValueError):
            PA2.FindIndex(self.table, 'color')
        
        # test finding the index of an element in an empty header
        empty_table = 'empty_table.txt'
        with open(empty_table, 'w') as f:
            f.write('')
        with self.assertRaises(ValueError):
            PA2.FindIndex(empty_table, 'name')
        os.remove(empty_table)
        
    def test_DELETE_TUPLE(self):
        # create a sample table for testing
        table = 'test_table2.txt'
        header = 'pid int | name varchar(20) | price float\n'
        tuples = ['1 | Gizmo | 19.99\n', '2 | PowerGizmo | 29.99\n', '3 | SingleTouch | 149.99\n']
        with open(table, 'w') as f:
            f.write(header)
            for t in tuples:
                f.write(t)        
        
        # test deleting a single tuple
        equation = ['pid', '=', '2']
        PA2.DELETE_TUPLE(table, equation)
        with open(table, 'r') as f:
            lines = f.readlines()
        self.assertEqual(len(lines), 3)
        self.assertNotIn('2 | PowerGizmo | 29.99\n', lines)
        
        # test deleting multiple tuples
        equation = ['price', '>', '50']
        PA2.DELETE_TUPLE(table, equation)
        with open(table, 'r') as f:
            lines = f.readlines()
        self.assertEqual(len(lines), 2)
        os.remove(table)
        
    def test_UPDATE_TABLE(self):
        # create a sample table for testing
        table = 'test_table3.txt'
        header = 'pid int | name varchar(20) | price float\n'
        tuples = ['1 | Gizmo | 19.99\n', '2 | PowerGizmo | 29.99\n', '3 | SingleTouch | 149.99\n']
        with open(table, 'w') as f:
            f.write(header)
            for t in tuples:
                f.write(t)

        # test updating a single tuple
        then_EQ = ['price', '=', '39.99']
        if_EQ = ['pid', '=', '1']
        PA2.UPDATE_TABLE(table, then_EQ, if_EQ)
        with open(table, 'r') as f:
            lines = f.readlines()
        self.assertIn('1 | Gizmo | 39.99\n', lines)

        # test updating multiple tuples
        then_EQ = ['name', '=', 'NewGizmo']
        if_EQ = ['price', '>', '20']
        PA2.UPDATE_TABLE(table, then_EQ, if_EQ)
        with open(table, 'r') as f:
            lines = f.readlines()
        self.assertIn('2 | NewGizmo | 29.99\n', lines)
        self.assertNotIn('1 | Gizmo | 39.99\n', lines)
        os.remove(table)
        
    def test_matching_value(self):
        element_where_index = 1
        tuples = '1 | Gizmo | 19.99\n'
        EQ = '= Gizmo'
        self.assertTrue(PA2.WHERE_TEST(element_where_index, tuples, EQ))
        
    def test_non_matching_value(self):
        element_where_index = 2
        tuples = '2 | PowerGizmo | 29.99\n'
        EQ = '> 50'
        self.assertFalse(PA2.WHERE_TEST(element_where_index, tuples, EQ))
        
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_SELECT_TABLE(self, mock_stdout):
        table = "test_table4.txt"
        with open(table, "w") as f:
            f.write("pid int | name varchar(20) | price float\n")
            f.write("1 | Gizmo | 19.99\n")
            f.write("2 | PowerGizmo | 29.99\n")
            f.write("3 | SingleTouch | 149.99")   
            
        PA2.SELECT_TABLE(["select", "*", "from", table])
        expected_output = "pid int | name varchar(20) | price float\n1 | Gizmo | 19.99\n2 | PowerGizmo | 29.99\n3 | SingleTouch | 149.99\n"
        self.assertEqual(mock_stdout.getvalue(), expected_output)

        if os.path.exists(table):
            os.remove(table)
            
    def test_DROP_TABLE(self):
        # Create test table
        file = open('test_table5.txt', 'w')
        file.write('pid int | name varchar(20) | price float\n1 | Gizmo | 19.99\n2 | PowerGizmo | 29.99\n3 | SingleTouch | 149.99\n')
        file.close()

        # Test deleting existing table
        PA2.DROP_TABLE('test_table5.txt')
        self.assertFalse(os.path.exists('test_table5.txt'))

        # Test deleting non-existing table
        PA2.DROP_TABLE('non_existing_table.txt')
        self.assertTrue(True)
        
    def test_list_to_string(self):
        test_list = ["apple", "banana", "cherry"]
        result = PA2.ListToString(test_list)
        self.assertEqual(result, "apple banana cherry")
        
    def test_normal_sentence(self):
        sentence = "This is a normal sentence."
        expected_output = "this is a normal sentence."
        result = PA2.LowerAndConsiderQuotes(sentence)
        self.assertEqual(result, expected_output)

    def test_sentence_with_single_quotes(self):
        sentence = "This is a sentence 'with single quotes'."
        expected_output = "this is a sentence with single quotes."
        result = PA2.LowerAndConsiderQuotes(sentence)
        self.assertEqual(result, expected_output)

    def test_sentence_with_wrong_single_quotes(self):
        sentence = "This is a sentence 'with wrong single quotes."
        with self.assertRaises(PA2.WrongSingleQuotes):
            PA2.LowerAndConsiderQuotes(sentence)
            
    def test_correct_equation(self):
        equation = "x = 3"
        result = PA2.StringEquationToList(equation)
        expected = ['x', '=', '3']
        self.assertEqual(result, expected)

    def test_extra_space(self):
        equation = "x   =     3"
        result = PA2.StringEquationToList(equation)
        expected = ['x', '=', '3']
        self.assertEqual(result, expected)

    def test_multiple_comparisons(self):
        equation = "x = 3 > 4"
        with self.assertRaises(PA2.IncorrectFormat):
            PA2.StringEquationToList(equation)

    def test_incorrect_operator(self):
        equation = "x ^ 3 = 5"
        with self.assertRaises(PA2.IncorrectFormat):
            PA2.StringEquationToList(equation)
            
    def test_FixEQFormat(self):
        # Test with one equation string missing a value
        input2 = ['update', 'table1', 'set', 'col1', '=', 'val1', ',', 'col2', '=', 'where', 'col3', '=', 'val3']
        with self.assertRaises(PA2.IncorrectFormat):
            PA2.FixEQFormat(input2)
        
        # Test with one equation string missing an operator
        input3 = ['update', 'table1', 'set', 'col1', '=', 'val1', ',', 'col2', 'val2', 'where', 'col3', '=', 'val3']
        with self.assertRaises(PA2.IncorrectFormat):
            PA2.FixEQFormat(input3)
        
        # Test with two equation strings missing values
        input4 = ['update', 'table1', 'set', 'col1', '=', ',', 'col2', '=', 'where', 'col3', '=', 'val3']
        with self.assertRaises(PA2.IncorrectFormat):
            PA2.FixEQFormat(input4)
        
        # Test with two equation strings missing an operator
        input5 = ['update', 'table1', 'set', 'col1', '=', 'val1', ',', 'col2', 'val2', 'where', 'col3', 'val3']
        with self.assertRaises(PA2.IncorrectFormat):
            PA2.FixEQFormat(input5)
        
    def test_CREATE_DATABASE(self):
        new_database = 'test_database'
        PA2.CREATE_DATABASE(new_database)
        self.assertTrue(os.path.isdir(new_database))
        os.rmdir(new_database)
        
    def test_DROP_DATABASE(self):
        test_database = 'test_database'
        os.mkdir(test_database)

        PA2.DROP_DATABASE(test_database)
        self.assertFalse(os.path.exists(test_database))
    
    def test_INSERT_TABLE(self):
        table_name = "test_table6.txt"
        with open(table_name, "w") as f:
            f.write("pid int | name varchar(20) | price float\n")
            f.write("1 | Gizmo | 19.99\n")
            f.write("2 | PowerGizmo | 29.99\n")
            f.write("3 | SingleTouch | 149.99\n")
        
        arguments = "(4,NewGizmo,39.99)"
    
        PA2.INSERT_TABLE(table_name, arguments)
        
        with open(table_name, "r") as f:
            lines = f.readlines()
            self.assertEqual(len(lines), 6)
            self.assertEqual(lines[-1].strip(), "4 | NewGizmo | 39.99") 
    
        os.remove(table_name)
        
    def test_ALTER_TABLE(self):
        table = "test_table7.txt"
        file_content = "pid int | name varchar(20) | price float\n1 | Gizmo | 19.99\n2 | PowerGizmo | 29.99\n3 | SingleTouch | 149.99"
        new_element = "inventory int"
        with open(table, "w") as file:
            file.write(file_content)
            
        PA2.ALTER_TABLE(table, new_element)
        
        with open(table, "r") as file:
            updated_content = file.read()
            self.assertIn(new_element, updated_content)
            self.assertEqual(updated_content.count("|"), 9)
        
        os.remove(table)

    def test_ElementCheck(self):
        table = "test_table8.txt"
        file_content = "pid int | name varchar(20) | price float\n1 | Gizmo | 19.99\n2 | PowerGizmo | 29.99\n3 | SingleTouch | 149.99"
        with open(table, "w") as file:
            file.write(file_content)
        element = "pid"
        try:
            PA2.ElementCheck(table, element)
        except PA2.ElementNotFoundError:
            self.fail("ElementNotFoundError raised unexpectedly.")
        os.remove(table)
        
    def test_ElementCheck_with_non_existing_element(self):
        table = "test_table9.txt"
        file_content = "pid int | name varchar(20) | price float\n1 | Gizmo | 19.99\n2 | PowerGizmo | 29.99\n3 | SingleTouch | 149.99"
        with open(table, "w") as file:
            file.write(file_content)
        element = "non_existing_element"
        with self.assertRaises(PA2.ElementNotFoundError):
            PA2.ElementCheck(self.table, element)
        os.remove(table)

    def test_USE(self):
        test_directory = 'test_db'
        PA2.USE(test_directory)
        self.assertNotEqual(os.getcwd(), os.path.abspath(test_directory))
        
    def test_USE_non_existing_database(self):
        captured_output = io.StringIO()
        expected_output = "!Failed because database non_existing_db does not exist.\n"
        with unittest.mock.patch('sys.stdout', new=captured_output):
            PA2.USE('non_existing_db')
            self.assertEqual(captured_output.getvalue(), expected_output)
            
    def test_file_not_found_ALTER_TABLE(self):
        table = "non_existing_table.txt"
        new_element = "new_element"
        try:
            PA2.ALTER_TABLE(table, new_element)
        except FileNotFoundError:
            self.fail("FileNotFoundError raised unexpectedly.")
            
    def test_file_found_ALTER_TABLE(self):
        table = "existing_table.txt"
        new_element = "new_element"
        with open(table, "w") as file:
            file.write("existing_element")
        PA2.ALTER_TABLE(table, new_element)
        with open(table, "r") as file:
            content = file.read()
        self.assertIn(new_element, content)
        os.remove(table)
        
    def test_file_exists_CREATE_TABLE(self):
        new_table = "existing_table.txt"
        arguments = "(column1, column2, column3)"
        with open(new_table, "w") as file:
            file.write("existing_data")
        try:
            PA2.CREATE_TABLE(new_table, arguments)
        except FileNotFoundError:
            self.fail("FileNotFoundError raised unexpectedly.")
        os.remove(new_table)
        
if __name__ == '__main__':
    unittest.main()
