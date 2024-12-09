### Grupo: SO-TI-13
### Aluno 1: Guilherme Soares (fc62372)
### Aluno 2: Duarte Soares (fc62371)
### Aluno 3: Vitoria Correia (fc62211)

import sys
from multiprocessing import Process, Value, Lock, Array, Queue
from time import sleep, time, strftime
from signal import signal, SIGINT, SIG_IGN
queue = None
counter = None
nProcesses = 0
totalFiles = 0
processingFiles = 0
processedFiles = None
mutex = None
stopProcessing = Value('b', True)  
def createProcesses(dividedFiles, wordCount, word, interval, stout):
    """
    Create and start multiple processes to count occurrences of a word in divided file data.

    Args:
        dividedFiles (dict): Dictionary with:
                                - key (str): Combined file paths or a portion of a file for each process.
                                - value (list of str): Lines of file data to be processed by each process.
        wordCount (function): Function to count occurrences of the word in each file.
        word (str): Word to search for in each file.
    """
    processes = []
    for i, (filePath, data) in enumerate(dividedFiles.items()):
        if wordCount == pwordC:
            process = Process(target=wordCount, args=(data, word))
        else:
            process = Process(target=wordCount, args=(data, word, i))
        processes.append(process)
        process.start()

    if(stout == writeLI or stout == writeC):
        queueList = stout(time(), processes, interval, "logTest.txt")
    else:
        queueList = stout(processes, interval, nProcesses)

    for process in processes:
        process.join()

    return queueList, counter

def signalHandler(sig, frame):
    global stopProcessing
    stopProcessing.value = False
    print("System stopped")
    
def readFile(filePaths):
    """
    Reads contents from multiple files and returns their data as a dictionary.

    Args:
        filePaths (list of str): List of file paths to read.

    Returns:
        dict: A dictionary where each key is a file path and each value is a list of lines in that file.
    """
    allFiles = {}
    for filePath in filePaths:
        with open(filePath, 'r') as file:
            data = file.readlines()
            allFiles[filePath] = data
    return allFiles

    
def stoutIL(processes, interval, nProcesses):
    """
    DOES STOUT OF -m l and -m i
    """
    aggregatedSets = 0
    previousCounter = [0] * nProcesses
    finished = True
    firstTime = time()
    global processedFiles
    global totalFiles
    
    queueList = []
    while any(process.is_alive() for process in processes) or finished:
        secondTime = time()
        if(secondTime - firstTime >= interval):
            # Aggregate the results from `counter`
            for i in range(nProcesses):
                if(not queue.empty()):
                    queueList.append(queue.get())
                aggregatedSets += counter[i] - previousCounter[i]
                previousCounter[i] = counter[i]
            print(f"Partial count updated: {aggregatedSets}")
            print("The processed amount of processed files is: ", processedFiles.value)
            print("The processed amount of files left is: ", totalFiles - processedFiles.value)
            firstTime = time()

        if(len(queueList) == nProcesses):
            return queueList

def stdoutC(processes, interval, nProcesses):
    firstTime = time()
    global processedFiles
    global totalFiles
    while any(process.is_alive() for process in processes):
        secondTime = time()
        if(secondTime - firstTime >= interval):
            print(f"\nPartial count updated: {counter.value}")
            print("The processed amount of processed files is: ", processedFiles.value)
            print("The processed amount of files left is: ", totalFiles - processedFiles.value)
                
            firstTime = time()


def divideFileList(allFiles):
    """
    Divide file data into chunks for each process.

    Args:
        allFiles (list of str): List of file paths.
        nProcesses (int): Number of processes to divide the data into.

    Returns:
        dict: A dictionary with:
                    - key (str): Combined file paths or portions of a file.
                    - value (list of str): Data chunk for each process.
    """
    finalDict = {}
    allData = readFile(allFiles)

    
    global nProcesses
    global totalFiles
    totalFiles = len(allData)
    
    if nProcesses == 1:
        filePath = ""
        data = []
        for item in allData:
            filePath += item + "\n"
            data += allData[item]
        finalDict[filePath] = [data]
        return finalDict
    
    if len(allData) != 1:
        nProcesses = min(len(allData), nProcesses)
        filePaths = []
        data = []
        nFiles = len(allFiles) - 1
        index = 0
        for i in range(nProcesses):
            filePaths.append(())
            data.append([])
        
        # Distribute files across chunks
        while(nFiles >= 0):
            if index >= nProcesses:
                index = 0
            filePaths[index] += (allFiles[nFiles],)
            data[index].append(allData[allFiles[nFiles]])
            
            index += 1
            nFiles -= 1

        for i in range(len(filePaths)):
            finalDict[filePaths[i]] = data[i]
    else:
        linhas = list(allData.values())[0]  # assuming this gets the list of lines
        nProcesses = min(len(linhas), nProcesses)
        numLinhasDiv = len(linhas) // nProcesses  # number of lines per process 
        totalFiles = nProcesses #number of chunks is the number of processes
        
        for i in range(nProcesses):
            startIndex = i * numLinhasDiv
            # If this is the last chunk, include all remaining lines
            if i == nProcesses - 1:
                chunk = linhas[startIndex:]
            else:
                endIndex = startIndex + numLinhasDiv
                chunk = linhas[startIndex:endIndex]
            key = list(allData.keys())[0] + f" Parte {i + 1}" 
            finalDict[key] = [chunk]

    return finalDict




def pwordC(dados, word):
    """
    Count the total occurrences of a word as a substring in each line.

    Args:
        data (list of str): Lines of data read from the specified files.
        word (str): Word to count.
        file (str): File path or part label of the processed data.
    """
    signal(SIGINT, SIG_IGN)  #assim o filho "nao ouve"
    global counter
    global processedFiles  
    global mutex  
    global stopProcessing
    for file in dados:
        if(stopProcessing.value == 1):
            processingFiles.value += 1
            for frase in file:
                for item in frase.split(" "):
                    if word in item.rstrip():
                        mutex.acquire()
                        counter.value += 1
                        mutex.release()
            processedFiles.value += 1
        
        
def pwordL(dados, word, index):
    """
    Count the total lines containing a specific word.

    Args:
        data (list of str): Lines of data read from the specified files.
        word (str): Word to count.
        file (str): File path or part label of the processed data.
    """
    signal(SIGINT, SIG_IGN)  #assim o filho "nao ouve" 
    lineCount = 0
    uniqueLines = set()
    global queue
    global counter
    global processedFiles
    global processingFiles
    global stopProcessing
    for file in dados:
        if(stopProcessing.value == 1):
            processingFiles.value += 1
            for line in file:
                if word in line:
                    sublist = (lineCount,line)
                    uniqueLines.add(sublist)
                    lineCount += 1
                counter[index] = lineCount
            processedFiles.value += 1
            
        

    counter[index] = lineCount
    queue.put(uniqueLines)


def pwordI(dados, word, index):
    """
    Count exact occurrences of a word in each line.

    Args:
        data (list of str): Lines of data read from the specified files.
        word (str): Word to count.
        file (str): File path or part label of the processed data.
    """
    signal(SIGINT, SIG_IGN)  #assim o filho "nao ouve"
    global stopProcessing
    wordCount = 0

    for file in dados:
        if(stopProcessing.value == 1):
            processingFiles.value += 1
            for frase in file:
                for item in frase.split(" "):
                    if word == item.rstrip():  # Check if the substring is equals to word
                        wordCount += 1

                    counter[index] = wordCount
            processedFiles.value += 1
    
    counter[index] = wordCount
    queue.put(wordCount)


def pwordLSum(nProcesses, queueList):
    totalCount = 0
    i = 0
    
    for item in queueList:
        totalCount += len(item)

    return totalCount


def pwordISum(nProcesses, queueList):
    totalCount = 0
    processesCounter = 0
    queueList

    while(processesCounter < nProcesses):
        childCount = queueList[processesCounter]
        totalCount += childCount
        processesCounter+=1

    return totalCount

def writeLI(masterTime, processes, interval, log_file):
    global totalFiles
    global processedFiles
    aggregatedSets = 0
    previousCounter = [0] * nProcesses
    finished = True
    
    queueList = []
    totalFileLines = []
    firstTime = time()
    while any(process.is_alive() for process in processes) or finished:
        secondTime = time()
        if(secondTime - firstTime >= interval):
            # Aggregate the results from `counter`
            for i in range(nProcesses):
                if(not queue.empty()):
                    queueList.append(queue.get())
                aggregatedSets += counter[i] - previousCounter[i]
                previousCounter[i] = counter[i]
            log_entry = f"{strftime('%d/%m/%Y-%H:%M:%S')} {int(round(secondTime - masterTime, 5)*1_000_000)} {aggregatedSets} {processedFiles.value} {totalFiles - processedFiles.value}"
            #aq meto para guardar numa lst
            totalFileLines.append(log_entry + "\n")  
            firstTime = time()
        if((len(queueList) == nProcesses) or (stopProcessing.value == 0 and len(queueList) == processingFiles.value)):
            #aq faz write
            with open(log_file, "w") as file:
                for line in totalFileLines:
                    file.write(line)
            return queueList

def writeC(masterTime,processes, interval, log_file):
    firstTime = time()
    global processedFiles
    global totalFiles
    totalFileLines = []
    while any(process.is_alive() for process in processes):
        secondTime = time()
        if(secondTime - firstTime >= interval):
            log_entry = f"{strftime('%d/%m/%Y-%H:%M:%S')} {int(round(secondTime - masterTime, 5)*1_000_000)} {counter.value} {processedFiles.value} {totalFiles - processedFiles.value}"

            totalFileLines.append(log_entry + "\n")  
            firstTime = time()
    
    with open(log_file, "w") as file:
        for line in totalFileLines:
            file.write(line)
            
            
def main(args):
    """
    Main function to execute the script and handle user input.

    Args:
        args (list): The command-line arguments passed to the script.
    """
    print('Programa: pword.py')
    print('Argumentos: ', args)
    #CONSTANTS
    M_MODE = 1
    P_MODE = 3
    INTERVAL = 5
    LOG_FILE = 7
    WORD = 9
    FILES = 10
    files = args[FILES:]
    signal(SIGINT, signalHandler)
    global queue
    global counter
    #Atributting a different function deppending on the M_MODE
    global nProcesses
    nProcesses = int(args[P_MODE])
    global processedFiles
    processedFiles = Value("i", 0)
    global processingFiles
    processingFiles = Value("i", 0)
    
    global mutex
    
    if(args[M_MODE] == "c"):
        wordCount = pwordC
        counter = Value("i", 0)
        mutex = Lock()
        if(args[LOG_FILE] == "stdout"):        
            stout = stdoutC
        else:
            stout = writeC
    elif(args[M_MODE] == "i"):
        wordCount = pwordI
        queue = Queue()
        counter = Array('i', nProcesses)
        if(args[LOG_FILE] == "stdout"):        
            stout = stoutIL
        else:
            stout = writeLI
    elif(args[M_MODE] == "l"):
        wordCount = pwordL
        queue = Queue()
        counter = Array('i', nProcesses)
        if(args[LOG_FILE] == "stdout"):        
            stout = stoutIL
        else:
            stout = writeLI

    if stopProcessing.value == 0:
        print("Divided Files not activated:\n userSignal activated before file division.")
        sys.exit(0)
    else:
        dividedFiles = divideFileList(files)

    
    #creates the processes
    if stopProcessing.value == 0:
        print("Any process was atributed:\n userSignal activated before file distribution")
        sys.exit(0)
    else:
        queueList = createProcesses(dividedFiles, wordCount, args[WORD] ,float(args[INTERVAL]), stout)

    

    if(args[M_MODE] == "c"):
        totalCount = counter.value
    elif(args[M_MODE] == "i"):
        totalCount = pwordISum(nProcesses, queueList[0])
    elif(args[M_MODE] == "l"):
        totalCount = pwordLSum(nProcesses, queueList[0])
    
    
    print(f"Total unique lines: {totalCount}")

if __name__ == "__main__":
    main(sys.argv[1:])