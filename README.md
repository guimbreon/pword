### Grupo: SO-TI-13
# Aluno 1: Guilherme Soares (fc62372)
# Aluno 2: Duarte Soares (fc62371)
# Aluno 3: Vitória Correia (fc62211)

### Exemplos de comandos para executar o pword :
1) ./pword -m c -p 2 -d testLog.log -w palavra testFiles/file.txt 
2) ./pword -m l -w ola -p 1 testFiles/file.txt 
3) ./pword -m i -p 12 -w palavra testFiles/file.txt testFiles/file.txt
4) ./pword -p 2 -i 1 -w palavra testFiles/file.txt 
5) ./pword -m c -i 1 -d testLog.log  -w palavra testFiles/file1.txt testFiles/file2.txt

### Limitações da implementação:
- ...
- ...

### Abordagem para a divisão dos ficheiros:
-Caso haja mais processos filhos que ficheiros lidos,
 o número de processos filhos será igual ao número de ficheiros lidos.


-Caso haja mais ficheiros lidos do que processos filhos,
 o número de ficheiros será dividido entre os processo filhos, veremos como exemplo:
 existindo 5 ficheiros e 2 filhos, os processos filhos irão receber alternadamente cada ficheiro
 começando pelo primeiro filho, até que todos os ficheiros sejam distribuídos, assim
 sendo o primeiro processo filho ficará com 3 ficheiros e o segundo com 2.


-Caso haja um unico ficheiro e varios processos filhos,
 o ficheiro é divido em pedaços (chunks) para o número respetivo de processos filhos.

 
### Outras informações pertinentes:
- Se o SIGINT for ativado antes mesmo da distribuição dos ficheiros(ou chunks) o seguinte decorrerá:
	-Antes da divisão dos ficheiros -> sys.exit(0) será ativado e um erro na tela aparecerá, pois interromperá antes da divisão dos ficheiros.
	-Antes da distribuição dos ficheiros -> sys.exit(0) será ativado e um erro na tela aparecerá, pois interromperá antes da distribuição dos ficheiros.