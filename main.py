import subprocess
import sys
import csv
from xml.etree.ElementTree import tostring

# https://stackoverflow.com/a/23038606
# helper function, ignore line endings generated on windows/linux
def compareFilesByLine(path1, path2):
    line1 = line2 = True
    with open(path1, 'r') as f1, open(path2, 'r') as f2:
        while line1 and line2:
            line1 = f1.readline()
            line2 = f2.readline()
            if line1 != line2:
                return False
    return True

testDirections = []

# make it easier to get test conversion directions (remove comments from csv file first)
with open('./acts-output.csv', newline='') as file:
    
    actsTests = csv.DictReader(file)

    for row in actsTests:
        testDirections.append(row['ConversionDirection'].lower())

# which tests should be making the program return an error code (according to our spec)?
# manually generated
# test 1: valid XML contains tags with pattern 7 and that's it
# test 2: valid json containing all tags and and non-contiguous text
# test 3: empty file xml->json
# test 4: non-empty file with garbage data
# test 5: file contains XML/JSON tags but also contains garbage data
# test 6: file contains valid XML with some tags and non-contiguous text
# test 7: file contains valid JSON with some tags and no non-contiguous text
# test 8: file contains valid XML with some tags and non-contiguous text
# test 9: file contains valid JSON with some tags and non-contiguous text
# test 10: file contains XML/JSON tags but also contains garbage data with non-contiguous text
# test 11: file contains XML/JSON tags but also contains garbage data with non-contiguous text
# test 12: file contains valid JSON with some tags and no non-contiguous text
# test 13: empty file json->xml

expectedFailures = [0,0,1,1,1,0,0,0,0,1,1,0,1]

def runEachTest():
    for i in range(0, 13):
        outputFile = f'./TestOutput/Files/Output{i+1}'
        inputFile = f'./TestData/TestFiles/test{i+1}'

        testCommand = ['python', './xml2json.py', '-t', testDirections[i], '-o', outputFile, inputFile]
        test = subprocess.run(testCommand, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
       
        retcode = test.returncode
       
        expectedMatch = compareTestExpected(i, outputFile, retcode)
        
        print(f'\n  {" ".join(testCommand)}')
        print(f'TEST {i+1}: ', end='')
        if expectedMatch == True:
            print("SUCCEEDED")
        else:
            print("FAILED")
            if (expectedFailures[i] == 1 and retcode == 0) or (expectedFailures[i] == 0 and retcode != 0):
                print(f'\treturncode {retcode}, expected {"non-zero" if expectedFailures[i] else "0"}')
            else:
                print("\tfile mismatch")
                
        #output = test.stdout.decode("utf-8")
        #print(output)
        #print(test.stderr.decode("utf-8"))
        

def compareTestExpected(testNum, output, retcode):
    i = testNum
    shouldFail = expectedFailures[i]
    expectedOutputFile = f'./TestData/ExpectedOutput/Output{i+1}'
    
    if (shouldFail == 1 and retcode == 0) or (shouldFail == 0 and retcode != 0):
        # program should have failed when it should succeed or vice versa (according to the spec)
        
        return False
    
    if shouldFail == 1 and retcode != 0:
        # program failed successfully
        return True
    
    # otherwise we should check the outputs to see if they match
    
    fileoutput = compareFilesByLine(output, expectedOutputFile)
    if fileoutput == False: # outputs are not equal to expected
        return False
    
    # fallthrough, retcode is equal or test output is equal
    return True


def main():
    #xml2json -t xml2json -o file.json file.xml
    runEachTest()

main()
