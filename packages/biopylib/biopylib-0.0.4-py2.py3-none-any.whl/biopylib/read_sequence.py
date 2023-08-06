from biopylib.sequence import SQ
from re import sub, search

# NCBI identifiers
identifiers_dic = {'lcl':'local(nodb)','bbs':'GenInfo backbone seqid',
                   'bbm':'GenInfo backbone moltype','gim':'GenInfo import ID',
                   'gb':'GenBank','emb':'EMBL','pir':'PIR','sp':'SWISS-PROT',
                   'pat':'patent','pgp':'pre-grant patent','ref':'RefSeq',
                   'gnl':'general database reference','prf':'PRF','pdb':'PDB',
                   'gi':'GenInfo integrated database','dbj':'DDBJ'}

# FASTA format names
dict_FASTA = {'fa':'generic','fasta':'generic','fna':'nucleic acid',
             'ffn':'nucleotide of gene regions','faa':'amino acid',
             'frn':'non-coding RNA'}

# Class to read different files and store info only
class readSeq(SQ):
  
    def __init__(self,name):
        self.name = name
        self.format = name.rsplit('.',1)[1]    
        if(self.format in dict_FASTA):      # if one of the fasta formats
            self.read(self.name)
      
    # read FASTA format
    
    def read(self,filename):
        
        self.filename = filename # store filename
        tseq = None; self.lst_seq = []     # list of sequences
        thead = None; self.lst_header = [] # list of sequence identifications
        ff = dict_FASTA[filename.rsplit('.',1)[1]]
        file = open(filename,'r')
      
        for line in file:
            if(search(">.*", line)): # get lines w/ >
                    if(tseq != None and thead != None and tseq != ""):
                        self.lst_seq.append(tseq)
                    thead = line; self.lst_header.append(line)              
                    tseq = ""
            else:
                if(tseq == None):
                    return None
                else: 
                    tseq += sub("\s","",line)
                  
        if(tseq != None and thead != None and tseq != ""):
            self.lst_seq.append(tseq)
          
        print(f'[note] read -> FASTA [{ff}] | #seq: {len(self.lst_seq)}')
        file.close()
      
    # store the sequences 
    # [1] if file has more than one seq -> output list of SQ
    # [2] if file has one seq -> return SQ 
    
    def store(self):
        
        lst_out = []
        # If there's more than one sequence
        
        if(len(self.lst_seq) > 1):
            for i in range(0,len(self.lst_seq)):
                lst_types = ['dna','rna','aa']
                for check in lst_types:
                    if(SQ(seq=self.lst_seq[i],seq_type=check).validate()):
                        lst_out.append(SQ(self.lst_seq[i],
                                          seq_type=check,
                                          origin=self.filename,
                                          description=self.lst_header[i]))
            return lst_out
      
        # return just the one file
        
        else:
            lst_types = ['dna','rna','aa']
            for check in lst_types:
                if(SQ(self.lst_seq[0],check).validate()): # if valid sq
                    return SQ(seq=self.lst_seq[0],
                              seq_type=check,
                              origin=self.filename,
                              description=self.lst_header[0])