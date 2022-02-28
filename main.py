import subprocess
import sys
import filecmp
from xml.etree.ElementTree import tostring

def runEachTest():
    for i in range(1, 6):
        subprocess.call(['python.exe', './xml2json.py', '-t', 'xml2json', '-o', './TestData/TestFiles/test' + str(i) + '.json', 'TestOutput/Files/Output' + str(i) + '.xml']);

def CompareTestExpected():
    for i in range(1, 6):
        print(filecmp.cmp('TestOutput/Files/Output' + str(i) + '.xml', './TestData/ExpectedOutput/Output' + str(i) + '.xml', shallow=True))


def main():
    #xml2json -t xml2json -o file.json file.xml
    runEachTest()
    CompareTestExpected()

main()