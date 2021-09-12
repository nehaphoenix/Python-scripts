"""
Module for injecting fault in source code for mimicing customer site failures.
Usage : python3 fault_injection.py <operation_name> <step_name>
operation : Operation during which the fault needs tob e injected.
step_name : Step during which the fault will be triggered.
"""
import sys
import json

class FaultInjection():
  """
  step1: Creates backup file of original file on which fault will be injected.
  step1: Locates the function in the file based on the step passed at runtime.
  step2: Determines indentation of the next executable line in the function.
  step3: Forms new line with the appropriate custom errormsg to the step.
  step4: Inserts line at calculated indentation to raise exception in the source file.
  """
  def __init__(self):
    """
    Declaring common variables used across class
    """
    self.filename = ""
    self.funcname = ""
    self.custom_error = ""

  def create_backup_file(self, filename):
    """
    Creates backup of the original source code file before injecting fault.
    """
    print("<<<< Taking backup of original file >>>>")
    fb = open(self.filename, "r")
    self.temp_file_content = fb.readlines()
    fb.close()
    backup_filename = self.filename + "bkpfile"
    fw = open(backup_filename, "w+")
    fw.writelines(self.temp_file_content)

  def read_json_file(self):
    """
    Fetches inputs needs for error injection based on op_name and step_name
    Sample json file format as below where filename, function name is based
    on which step of the operation needs to be failed.
    ops_details = {
      "operation1": {
        "begin": {
          "filename" : "abc/def/ghi.py"
          "funcname" : "function1",
          "custom_error" : "Injected fault during operation1"
        }
      },
      "operation2": {
        "begin": {
          "filename" : "mno/pqr/stu.py"
          "funcname" : "function2",
          "custom_error" : "Injected fault during operation2"
        }
      }
    }
    Returns:
      output of json file load
    """
    json_file = "error_injection.json"
    with open(json_file) as jf:
      json_obj = json.load(jf)
    return json_obj

  def locate_function(self, funcname):
    """
    Locates the function in which fault needs to be injected.
    Args:
     funcname (str): Function at which fault needs to be injected.
    Returns:
      line_to_w : Current line content at which exception will be raised
      line_count : Line number at which exception will be raised
    """
    funcname = self.funcname
    search_str = "def" + " " + funcname
    print("<<<< Locating function : {0} in {1} ".format(search_str, \
      self.filename))
    line_count = prev_line_count = count = 0
    line_to_w = ""
    file_ptr = open(self.filename, "r+")

    for line in file_ptr:
      line_count += 1
      if search_str in line and "):" in line:
        print("{0} - Function definition found".format(search_str))
        print("Get line number & first line inside the function")
        line_to_w = file_ptr.readline()
        print("First line of the function:", line_to_w)
        break
      elif search_str in line and "):" not in line:
        print("Function def found, traversing to find the end of function def")
        prev_line_count = line_count
        print("Previous line count calculated : {}", prev_line_count)
        search_char = "):"
        while True:
          new_read_line = file_ptr.readline()
          print("Next line of the function : ", new_read_line)
          if search_char in new_read_line:
            print("Count in IF loop :", count)
            line_to_w = file_ptr.readline()
            break
          else:
            count += 1
            print("Count in ELSE loop : ", count)
    print(prev_line_count)
    if prev_line_count == 0:
      line_count = line_count
    else:
      line_count = prev_line_count + count + 1
    print("END of def line count : ", line_count)
    file_ptr.close()
    return (line_to_w, line_count)

  def calculate_indent(self, line_to_w):
    """
    Args:
      line_to_w (str): Current line content returned from locate_function() at
      at which exception needs to be raised
    Returns:
      indent : indentation of the line where we need raise exception
    """
    print("<<<< Calculating Indentation >>>>")
    indent = 0
    indent = len(line_to_w) - len(line_to_w.lstrip())
    print("Indentation of first line inside function: ", indent)
    return indent

  def form_newline_to_insert(self, indent, custom_error):
    """
    Args:
      indent (int): calculated indentation from calculate_indent function
      custom_error (str): custom error string passed
    Returns:
      line_to_add : Forms the exception line using the custom custom_error passed
    """
    print("<<<< Forming new line >>>>")
    line_to_add = " " * indent+"raise Exception(\"{}\")".format(custom_error) +'\n'
    print("New line to be inserted :", line_to_add)
    return line_to_add

  def modify_original_file(self, line_count, line_to_add):
    """
    Modifies the content of the function passed in the file with the new line
    formed using custom errorstring with the appropriate indentation.
    Args:
      line_count (int): Line number at which exception needs to be raised
      line_to_add (str): Newline formed for inserting at line number passed.
    Returns:
      None
    """
    print("<<<< Modifying the original file >>>>")
    fnew = open(self.filename, "r")
    contents = fnew.readlines()
    print("Line number at which error to be raised:", line_count)
    temp = line_count - 1
    contents.insert(temp, line_to_add)
    fnew.close()

    print("Write to the original file")
    f1 = open(self.filename, "w")
    contents = "".join(contents)
    f1.write(contents)
    f1.close()

  def trigger_error(self, operation, step):
    """
    Args:
      operation (str): Operation during which fault must be injected
      step (str): Step at which fault will be injected by raising Exception in source code.
    Returns:
      None
    """
    ops_details = self.read_json_file()
    self.filename = ops_details['operation']['step']['filename']
    self.funcname = ops_details['operation']['step']['funcname']
    self.custom_error = ops_details['operation']['step']['custom_error']
    print("###### Beginning Fault injection #######")
    self.create_backup_file(self.filename)
    new_line, line_loc = self.locate_function(self.funcname)
    print("Line at which insert to be made : ", new_line)
    new_line_loc = line_loc + 1
    print("Line number at which insert to be made :", new_line_loc)
    new_indent = self.calculate_indent(new_line)
    line_to_add = self.form_newline_to_insert(new_indent, self.custom_error)
    self.modify_original_file(new_line_loc, line_to_add)

if __name__ == '__main__':
  FAULTINJ_OBJ = FaultInjection()
  USER_INPUTS = sys.argv
  OPNAME = USER_INPUTS[1]
  STEP_NAME = USER_INPUTS[2]
  FAULTINJ_OBJ.trigger_error(OPNAME, STEP_NAME)

