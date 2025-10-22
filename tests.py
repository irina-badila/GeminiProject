from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file

# def tests():
      #check if the get_files_info works as expected
#     #check results for calculator directory
#     result=get_files_info("calculator","");
#     print("Results for current directory:");
#     print(result);
#     print("");

#     #check results for pkg directory
#     result=get_files_info("calculator","pkg");
#     print("Results for 'pkg' directory:");
#     print(result);
#     print("");

#     #check results for a directory outside working directory
#     result=get_files_info("calculator","/bin");
#     print("Results for '/bin' directory:");
#     print(result);
#     print("");

#     #check results for a directory outside working directory
#     result=get_files_info("calculator","../");
#     print("Results for '../' directory:");
#     print(result);

def main():
    #check if the get_file_content function works as expected
    # working_directory="calculator"
    # #check reading lorem.txt file
    # result=get_file_content(working_directory,"lorem.txt");
    # print('Content of "lorem.txt":');
    # print(result);
    # print("")

    # #check reading a non existing file
    # result=get_file_content(working_directory,"non_existing.txt");
    # print('Content of "non_existing.txt":');
    # print(result);
    # print("")

    # #check reading a file outside working directory
    # result=get_file_content(working_directory,"../tests.py");
    # print('Content of "../tests.py":');
    # print(result);
    # print("")

    # #check reading main.py file
    # result=get_file_content(working_directory,"main.py");
    # print('Content of "main.py":');
    # print(result);
    # print("")

    # #check reading calculator.py file
    # result=get_file_content(working_directory,"pkg/calculator.py");
    # print('Content of "pkg/calculator.py":');
    # print(result);
    # print("")

    # #check reading /bin/cat
    # result=get_file_content(working_directory,"/bin/cat");
    # print('Content of "/bin/cat":');
    # print(result);
    # print("")

    #check if the write_file function works as expected
    #working_directory="calculator"

    #check writing some text in the lorem.txt file
    # result=write_file(working_directory,"lorem.txt","New content for lorem.txt file.");
    # print('Writing to "lorem.txt":');
    # print(result);
    # print("")

    # #check writing to a new file
    # result=write_file(working_directory,"pkg/morelorem.txt","Content for morelorem.txt file.");
    # print('Writing to "pkg/morelorem.txt":');
    # print(result);
    # print("")

    # #check writing to a file outside working directory
    # result=write_file(working_directory,"../outside.txt","Content for outside.txt file.");
    # print('Writing to "../outside.txt":');
    # print(result);
    # print("")

    #check writing into a directory that does not exist
    # result=write_file(working_directory,"pkg2/file.txt","Content for file.txt file.");
    # print('Writing to "pkg2/file.txt":');
    # print(result);
    # print("")

    #check writing into a directory, not a file
    # result=write_file(working_directory,"pkg2","Content for pkg2 directory.");
    # print('Writing to "pkg2":');
    # print(result);
    # print("")

    #check if the run_python_file works as expected
    #check the run_python_file function
    # working_directory="calculator"

    # #check running calculator/main.py with arguments
    # result=run_python_file(working_directory,"main.py",["3 + 5"]);
    # print('Running "main.py":');
    # print(result);
    # print("");

    # #check running calculator/main.py without arguments
    # result=run_python_file(working_directory,"main.py");
    # print('Running "main.py":');
    # print(result);
    # print("");

    # #check running tests.py file
    # result=run_python_file(working_directory,"test.py");
    # print('Running "test.py":');
    # print(result);
    # print("");  

    # #check running ../main.py file outside working directory
    # result=run_python_file(working_directory,"../main.py");
    # print('Running "../main.py":');
    # print(result);
    # print("");

    # #check running a non existing file
    # result=run_python_file(working_directory,"non_existing.py");
    # print('Running "non_existing.py":');
    # print(result);
    # print("");

    # #check running a non python file
    # result=run_python_file(working_directory,"lorem.txt");
    # print('Running "lorem.txt":');
    # print(result);
    print("");

if __name__ == "__main__":
    main();