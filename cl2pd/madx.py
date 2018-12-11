import subprocess
import pandas
import fcntl
import os
import datetime
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

class _TFS:
    '''
       TFS parameters from MADX TFS output.
       The approach used is mainly inherithed from the class TWISS suggested by H. Bartosik et al.
    '''
           
    def __init__(self, filename): 
        self.indx={}
        self.keys=[]
        alllabels=[]
        #if '.gz' in filename:
        #    f=gzip.open(filename, 'rb')
        #else:
        f=open(filename, 'r')
            
        for line in f:
            if ("@ " not in line and "@" in line): 
                line = replace(line, "@" , "@ ")
            if ("@ " in line and "%" in line and "s" not in line.split()[2]) :
                label=line.split()[1]
                try:
                    exec("self."+label+"= "+str(float((line.replace( '"', '')).split()[3])))
                except:
                    print("Problem parsing: "+ line)
                    print("Going to be parsed as string")
                    try:
                        exec("self."+label+"= \""+(line.split()[3]).replace( '"', '')+"\"")
                    except:
                        print("Problem persits, let's ignore it!")
            elif ("@ " in line and "s"  in line.split()[2]):
                label=(line.split()[1]).replace(":","")
                exec("self."+label+"= \""+(line.replace('"', '')).split()[3]+"\"")

            if ("* " in line or "*\t" in line) :
                    alllabels=line.split()
                    for j in range(1,len(alllabels)):
                        exec("self."+alllabels[j]+"= []")
                        self.keys.append(alllabels[j])
                            
            if ("$ " in line or "$\t" in line) :
                alltypes=line.split()                

            if ("@" not in line and "*" not in line and "$" not in line) :
                values=line.split()   
                for j in range(0,len(values)):
                    if ("%hd" in alltypes[j+1]):                      
                        exec("self."+alllabels[j+1]+".append("+str(int(values[j]))+")")                 
                    if ("%le" in alltypes[j+1]):                      
                        exec("self."+alllabels[j+1]+".append("+str(float(values[j]))+")")
                    if ("s" in alltypes[j+1]):
                        try:
                            exec("self."+alllabels[j+1]+".append("+values[j]+")")
                        except:
                            exec("self."+alllabels[j+1]+".append(\""+values[j]+"\")") #To allow with or without ""
                        if "NAME"==alllabels[j+1]:
                            self.indx[values[j].replace('"', '')]=len(self.NAME)-1
                            self.indx[values[j].replace('"', '').upper()]=len(self.NAME)-1
                            self.indx[values[j].replace('"', '').lower()]=len(self.NAME)-1
        f.close()
        
        for j in range(1,len(alllabels)):
            if (("%le" in alltypes[j]) | ("%hd" in alltypes[j])  ):  
                exec("self."+alllabels[j]+"= np.array(self."+alllabels[j]+")") 


def _tfs2pd(myFile):
        '''
        Import a MADX TFS file in a pandas dataframe.
        
        ===Example=== 
        aux=importData.TFS2pd('/eos/user/s/sterbini/MD_ANALYSIS/2018/LHC MD Optics/collisionAt25cm_180urad/lhcb1_thick.survey')
        '''
        a=_TFS(myFile);
        aux=[]
        aux1=[]

        for i in dir(a):
            if not i[0]=='_':
                if type(getattr(a,i)) is float:
                    #print(i + ":"+ str(type(getattr(a,i))))
                    aux.append(i)
                    aux1.append(getattr(a,i))
                if type(getattr(a,i)) is str:
                    #print(i + ":"+ str(type(getattr(a,i))))
                    aux.append(i)
                    aux1.append(getattr(a,i))

        myList=[]
        myColumns=[]
        for i in a.keys:
            myContainer=getattr(a, i)
            if len(myContainer)==0:
                print("The column "+ i + ' is empty.')
            else:
                myColumns.append(i)
                myList.append(myContainer)
                
        if 'S' in a.keys:
            optics=pd.DataFrame(np.transpose(myList), index=a.S, columns=myColumns)
        else:
            optics=pd.DataFrame(np.transpose(myList), columns=myColumns)
        #optics=pd.DataFrame(np.transpose(myList), index=a.S,columns=myColumns)

        for i in optics.columns:
            aux3= optics.iloc[0][i]
            if type(aux3) is str:
                aux3=str.replace(aux3, '+', '')
                aux3=str.replace(aux3, '-', '')
                aux3=str.replace(aux3, '.', '')
                aux3=str.replace(aux3, 'e', '')
                aux3=str.replace(aux3, 'E', '')


                if aux3.isdigit():
                    optics[i]=optics[i].apply(np.double)

        aux.append('FILE_NAME')
        aux1.append(os.path.abspath(myFile))

        aux.append('TABLE')
        aux1.append(optics)

        globalDF=pd.DataFrame([aux1], columns=aux)
        globalDF=globalDF.set_index('FILE_NAME')
        globalDF.index.name=''
        return globalDF 
    
def tfs2pd(myList):
    '''
        Import a MADX TFS file in a pandas dataframe.
        
        ===Example=== 
        aux=importData.tfs2pd(['/eos/user/s/sterbini/MD_ANALYSIS/2018/LHC MD Optics/collisionAt25cm_180urad/lhcb1_thick.survey',
        '/eos/user/s/sterbini/MD_ANALYSIS/2018/LHC MD Optics/collisionAt25cm_180urad/lhcb1_thick.twiss'])
    '''
    if isinstance(myList, list):
        aux=[]
        for i in np.unique(myList):
            aux.append(_tfs2pd(i))
        return pd.concat(aux)
    else:
        return _tfs2pd(myList)
    
class MadX:
    '''Simple MAD-X wrapper written with the fundamental help of E. Laface (thanks a lot!).
       It is using pipes for communicate with MAD-X (tested on MAC and UNIX).
    '''
    def __init__(self, executable, verbose=True, preamble_script='option, echo, warn,info;\n'):
        self.executable = executable
        self.header=None
        self.table=None
        self.result=[]
        self.log=[]
        self.preamble_script=preamble_script
        self.start_section='!!************************************************START************************************************\n! '
        self.end_section='!!*************************************************END*************************************************\n\n'

        self.p = subprocess.Popen([self.executable], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        fd = self.p.stdout.fileno()
        fl = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)
        
        self.log+=['! >>> START: '+datetime.datetime.utcnow().strftime("%a %b %d %H:%M:%S.%f UTC %Y\n")]
        self.result+=['init']
        while self.result[-1]!='X:> ':
            self.result+=[i.decode() for i in self.p.stdout.readlines()]
        self.result=self.result[1:-1]
        self._clearResult()
        self.log+=self.result
        self.log+=['! <<< STOP: '+datetime.datetime.utcnow().strftime("%a %b %d %H:%M:%S.%f UTC %Y\n\n")]
        if verbose==True:
            for i in self.result:
                        print(i[0:-1])
            print('\n')
        self._preamble()
    
    def _preamble(self):
        self.input(self.preamble_script)
    
    def input(self, script, verbose=True):
        try:
            script+="print,text='ENDOFSCRIPT';\n"
            self.p.stdin.write(script.encode())
            self.p.stdin.flush()
            self.result=[]
            self.log+=['! >>> START: '+datetime.datetime.utcnow().strftime("%a %b %d %H:%M:%S.%f UTC %Y\n")]
            self.log+=[script];
            while not ('ENDOFSCRIPT\n' in self.result):
                self.result+=[i.decode() for i in self.p.stdout.readlines()]
            
            self.log+=self.result
            self.log+=['! <<< STOP: '+datetime.datetime.utcnow().strftime("%a %b %d %H:%M:%S.%f UTC %Y\n\n")]
            
            self._clearResult()
            if verbose==True:
                self._clearResult()
                for i in self.result:
                            print(i[0:-1])
        except:
            print('ERROR WITH THE EXECUTION, PLEASE CHECK IT.')
            return   
        
    def print_log(self):
        for i in self.log:
            print(i[:-1])
            
    def _clearResult(self):
        for string in ["print,text='ENDOFSCRIPT';\n",'X:>\n','X:> ','X:> \n','X:> X:> ','X:> X:> \n','ENDOFSCRIPT\n','\n']:
            while string in self.result: self.result.remove(string)    
        
        for i in range(len(self.result)):
            self.result[i]=str.replace(self.result[i],'X:> ','')
            if self.result[i]==self.end_section[0:-1]:
                self.result[i]=self.end_section
            
    def close(self):
        self.p.kill()
 
    def buildInput(self,myInputDictionary, myInputList, verbose=True):
        aux=''
        for i in myInputList:
            #if i=='HEADER':
            #    aux='option, echo, warn,info;\n'+aux
            if verbose: 
                aux=aux+self.start_section+i+''
            aux=aux+myInputDictionary[i]
            if verbose: 
                aux=aux+self.end_section
        return aux
    
    def buildFileFromDictionary(self,myInputDictionary,myFile="input.txt"):
        text_file = open(myFile, "w")
        text_file.write(madx.buildInput(myInputDictionary,myInputDictionary.keys()))
        text_file.close()
   
    def buildDictionaryFromFile(self,myFile="input.txt"):
        myInputDictionaryFromFile=OrderedDict()
        text_file = open(myFile, "r")
        a=text_file.read()
        text_file.close()

        myInputDictionaryFromFile=OrderedDict()
        myList=a.splitlines()
        aux=[i for i, j in enumerate(myList) if j == madx.start_section[0:-3]]

        for i in range(len(aux)):
            myAux=aux.copy()
            myAux.append(len(myList))
            j=myAux[i]
            k=myAux[i+1]

            myString="""
            {}""".format("\n".join(myList[(j+2):(k-2)]))
            myString=myString+'\n'
            while '\n ' in myString:
                myString=myString.replace('\n ', '\n')
            myInputDictionaryFromFile[myList[j+1][2:]]=myString
        return myInputDictionaryFromFile
