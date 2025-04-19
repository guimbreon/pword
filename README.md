# pword Project

Também pode consultar este README em português. [Click here](README-PT.md)

---

### Group: SO-TI-13  
# Student 1: Guilherme Soares  
# Student 2: Duarte Soares  
# Student 3: Vitória Correia  

### Example commands to execute `pword`:
1) `./pword -m c -p 2 -d testLog.log -w palavra testFiles/file.txt`  
2) `./pword -m l -w ola -p 1 testFiles/file.txt`  
3) `./pword -m i -p 12 -w palavra testFiles/file.txt testFiles/file.txt`  
4) `./pword -p 2 -i 1 -w palavra testFiles/file.txt`  
5) `./pword -m c -i 1 -d testLog.log -w palavra testFiles/file1.txt testFiles/file2.txt`

### Log registration interval  
- If `-i` is not provided, the default value will be 3.  
- If the value is provided, it will be updated accordingly. For example:  
  - `-i 1` -> sets the interval to 1 second

### Approach for dividing files:
- If there are more child processes than files,  
  the number of child processes will be equal to the number of files.

- If there are more files than child processes,  
  the files will be distributed among the child processes. For example:  
  if there are 5 files and 2 child processes, the files will be assigned alternately  
  starting with the first process, until all files are distributed.  
  In this case, the first child process will handle 3 files and the second one 2 files.

- If there is only one file and multiple child processes,  
  the file is split into chunks corresponding to the number of child processes.

### Other relevant information:
- If SIGINT is triggered before the distribution of files (or chunks), the following will occur:  
  - Before the division of files -> `sys.exit(0)` will be triggered, and an error will be displayed on screen, as the process will be interrupted before file division.  
  - Before file distribution -> `sys.exit(0)` will be triggered, and an error will be displayed on screen, as the process will be interrupted before file distribution.

--- 

Let me know if you'd like it polished further for documentation or presentation!
