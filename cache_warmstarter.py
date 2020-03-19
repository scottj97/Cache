#!/Users/Sushi/anaconda3/bin/python
###################################
## Cache WarmStarter
## Author : Sushant Sakhalkar
## Data   : 03/19/2020
###################################

from collections import OrderedDict

class WordAddr(int): #Get the Total Words for the given word address
    def get_words(self, num_words_per_block):
        for i in (num_words_per_block):
          return [i for i in (num_words_per_block)]

class BinaryAddress(str):
    #Calculate the Binary Address of a certain length for a base-10 word
    def __new__(cls, bin_addr=None, word_addr=None, num_addr_bits=0):
        if word_addr is not None:
            return super().__new__(
                cls, bin(word_addr)[2:].zfill(num_addr_bits))
        else:
            return super().__new__(cls, bin_addr)
    @classmethod
    def prettify(cls, bin_addr, min_bits_per_group):
        mid = len(bin_addr) // 2
        if mid < min_bits_per_group:
            # Return binary string immediately if bisecting the binary string
            # produces a substring which is too short
            return bin_addr
        else:
            # Otherwise, bisect binary string and separate halves with a space
            left = cls.prettify(bin_addr[:mid], min_bits_per_group)
            right = cls.prettify(bin_addr[mid:], min_bits_per_group)
            return ' '.join((left, right))
    
    # Returns the tag used to distinguish cache entries with the same index
    def get_tag(self, num_tag_bits):
        end = num_tag_bits
        tag = self[:end]
        if len(tag) != 0:
            #print("Tag",tag)
            return tag
        else:
            return None

    # Returns the index used to group Ways in Cache
    def get_index(self, num_offset_bits, num_index_bits):
        start = len(self) - num_offset_bits - num_index_bits
        end = len(self) - num_offset_bits
        index = self[start:end]
        #print("Index=",index)
        if len(index) != 0:
            return index
        else:
            return None

    # Returns the word offset used to select a word in the data pointed to by the given binary address
    def get_offset(self, num_offset_bits):
        start = len(self) - num_offset_bits
        offset = self[start:]
        if len(offset) != 0:
            #print("Offset=",offset)
            return offset
        else:
            return None

class AddrObj(object): #Create an object to return the Data
    def __init__(self, word_addr, num_addr_bits,
                 num_offset_bits, num_index_bits, num_tag_bits):
            
      self.word_addr = WordAddr(word_addr)
      self.bin_addr = BinaryAddress(
      word_addr=self.word_addr, num_addr_bits=num_addr_bits)
      self.offset = self.bin_addr.get_offset(num_offset_bits)
      self.index = self.bin_addr.get_index(num_offset_bits, num_index_bits)
      self.tag = self.bin_addr.get_tag(num_tag_bits)
      #print("Ref Index",int(self.index))
      #print("Return Done")
    def __str__(self):
        return str(OrderedDict(sorted(self.__dict__.items())))

class Cache(dict):
    cache_mem = {}
    # Initializes the reference cache with a fixed number of sets
    def __init__(self, cache=None, num_sets=None, num_index_bits=None):
        # A list of recently ordered addresses, ordered from least-recently
        
        cache_mem = {}
        self.recently_used_addrs = []
        self.cache_set_dict = {} #Dict to Store Data Per Block {Per Index}
        self.tag_dict       = {} #Dict to Store Tag Per Index

        if cache is not None:
            self.update(cache)
        else:
            for i in range(num_sets):
                index = BinaryAddress(
                    word_addr=WordAddr(i), num_addr_bits=num_index_bits)
                self[index] = []
                #print("\nin cache class:")
                #print(index)

    # indicating a hit; returns False otherwise, indicating a miss
    def is_hit(self, addr_index, addr_tag):
      if addr_index is None:
        blocks = self['0']
      elif addr_index in self:
        blocks = self[addr_index]
      else:
        return False
      #print("Blocks",blocks)
    
    def mark_ref_as_last_seen(self,index,tag): #Used in LRU Scheme 
        # The index and tag uniquely identify each address
        addr_id = (index,tag)
        print("\n\nAddr Id",addr_id)
        if addr_id in self.recently_used_addrs:
            self.recently_used_addrs.remove(addr_id)
        self.recently_used_addrs.append(addr_id)
    

    # Iterate through the recently-used entries in reverse order for LRU
    def replace_block(self,index_r,ref_r,replacement_policy):
      for recent_index, recent_tag in self.recently_used_addrs:
        #print("Recent Index",recent_index)
        if(replacement_policy=="lru"):
          if (recent_index == index_r and ref_r== recent_tag):
            self.tag_dict[index_r]["A"] = ref_r
            return
  
class Cache_WarmStart(object):
    # Retrieves a list of address references for use by simulator
    # Add entry to cache
    def add_entry(self, cache,data,word_addr, num_addr_bits, num_offset_bits,num_index_bits, num_tag_bits,replacement_policy):
      #Data List used to collect Data Cache Entry to print to dCache.hex Files
      list_cacheA = [] 
      list_cacheB = []
      list_cacheC = []
      list_cacheD = []

      #Tag List used to collect Tag Entry to print dTag.hex Files
      list_tagA = []
      list_tagB = []
      list_tagC = []
      list_tagD = []

      #Files with dCache Entries
      dCacheA = open("dcacheA.hex","w")
      dCacheB = open("dcacheB.hex","w")
      dCacheC = open("dcacheC.hex","w")
      dCacheD = open("dcacheD.hex","w")

      #Files with dTag Entried
      dTagA = open("dtagA","w")
      dTagB = open("dTagB","w")
      dTagC = open("dtagC","w")
      dTagD = open("dTagD","w")

      list_cache=[]
      list_tag=[]

      for r in range(64):
        list_cache.append(r)
        list_tag.append(r)

      for d in range(len(data)): # Iterating through a provided List of Tuples
        #print("Index\t >> ",d)
        ref_addr=data[d][0]
        #print("Address",hex(ref_addr))
        addr=(AddrObj(ref_addr,num_addr_bits, num_offset_bits,
                num_index_bits,num_tag_bits))

        addr_idx=int(addr.index,base=2)
        
        cache.mark_ref_as_last_seen(addr.index,addr.tag)
        #print("CACHE LRU",cache.recently_used_addrs)
        #print("Ref Tag",ref.tag)
     
        if(addr_idx not in cache.tag_dict.keys()): ## Adding Entries to Tag Dic Per Index
          cache.tag_dict[addr_idx] = {'tagA': '', 'tagB': '', 'tagC' : '', 'tagD' : ''} 
    
        if(bool(cache.tag_dict[addr_idx]["tagA"])==False):
          print("\nAdding entry:" +str(addr.tag) + " at Set Index: and Way ",addr_idx,"tagA")
          cache.tag_dict[addr_idx]["tagA"] = addr.tag
        elif(bool(cache.tag_dict[addr_idx]["tagB"])==False):
          print("\nAdding entry:"+str(addr.tag) + " at Set Index: and Way ",addr_idx,"tagB")
          cache.tag_dict[addr_idx]["tagB"] = addr.tag
        elif(bool(cache.tag_dict[addr_idx]["tagC"])==False):
          print("\nAdding entry:"+str(addr.tag) + " at Set Index: and Way ",addr_idx,"tagC")
          cache.tag_dict[addr_idx]["tagC"] = addr.tag
        elif(bool(cache.tag_dict[addr_idx]["tagD"])==False):
          print("\nAdding entry:"+str(addr.tag) + " at Set Index:and Way",addr_idx,"tagD")
          cache.tag_dict[addr_idx]["tagD"] = addr.tag
        else:
          print("Tag for the {%0d} is Full",addr_idx,cache.tag_dict[addr_idx])
          cache.replace_block(addr_idx,addr.tag,replacement_policy)
        
        print("Addr Index",addr_idx)

        if(addr_idx not in cache.cache_set_dict.keys()):
          #print("Cache Dict Way",cache_dict_way)
          cache.cache_set_dict[addr_idx] = {'A': '', 'B': '', 'C' : '', 'D' : ''}
        #print(cache_set_dict)
        
        if(bool(cache.tag_dict[addr_idx]["tagA"])==True):
          print("\nAdding entry:" +str((data[d][1:])) + " at Set Index: and Way ",addr_idx,"A")
          cache.cache_set_dict[addr_idx]["A"] = data[d][1:]
        else:
          cache.cache_set_dict[addr_idx]["A"] =('0')
        if(bool(cache.tag_dict[addr_idx]["tagB"])==True):
          print("\nAdding entry:" +str((data[d][1:])) + " at Set Index: and Way ",addr_idx,"B")
          cache.cache_set_dict[addr_idx]["B"] = data[d][1:]
        else:
          cache.cache_set_dict[addr_idx]["B"] =('0')
        if(bool(cache.tag_dict[addr_idx]["tagC"])==True):
          print("\nAdding entry:" +str((data[d][1:])) + " at Set Index: and Way ",addr_idx,"C")
          cache.cache_set_dict[addr_idx]["C"] = data[d][1:]
        else:
          cache.cache_set_dict[addr_idx]["C"] =('0')
        if(bool(cache.tag_dict[addr_idx]["tagD"])==True):
          print("\nAdding entry:" +str((data[d][1:])) + " at Set Index: and Way ",addr_idx,"D")
          cache.cache_set_dict[addr_idx]["D"] = data[d][1:]
        else:
          cache.cache_set_dict[addr_idx]["D"] =('0')
     
      for k in cache.tag_dict.keys():  ## Fill Up Remaining Tags with 'h0' for the index as corresponding address not provided 
        list_tagA.append(cache.tag_dict[k]["tagA"])
        list_tagB.append(cache.tag_dict[k]["tagB"])
        list_tagC.append(cache.tag_dict[k]["tagC"])
        list_tagD.append(cache.tag_dict[k]["tagD"])

      for ks in cache.cache_set_dict.keys():
        list_cacheA.append(cache.cache_set_dict[ks]["A"][0])
        list_cacheB.append(cache.cache_set_dict[ks]["B"][0])
        list_cacheC.append(cache.cache_set_dict[ks]["C"][0])
        list_cacheD.append(cache.cache_set_dict[ks]["D"][0])
      
      for nd in list_cache:
        if(nd not in cache.cache_set_dict.keys()):  ## Index Address Not provided, Initialize to 0
          #print("Cache Dict Way",cache_dict_way)
          cache.cache_set_dict[nd] = {'A': '', 'B': '', 'C' : '', 'D' : ''}
          cache.cache_set_dict[nd]["A"]=('0')
          cache.cache_set_dict[nd]["B"]=('0')
          cache.cache_set_dict[nd]["C"]=('0')
          cache.cache_set_dict[nd]["D"]=('0')
           
          ## Collect Entries per Way to be Printed
          list_cacheA.append(cache.cache_set_dict[nd]["A"][0]) 
          list_cacheB.append(cache.cache_set_dict[nd]["B"][0])
          list_cacheC.append(cache.cache_set_dict[nd]["C"][0])
          list_cacheD.append(cache.cache_set_dict[nd]["D"][0])

      for nt in list_tag:
        if(nt not in cache.tag_dict.keys()):  ## Index Address Not provided, Initialize to 0
          #print("Present",nt)
          #print("Cache Dict Way",cache_dict_way)
          cache.tag_dict[nt] = {'A': '', 'B': '', 'C' : '', 'D' : ''}

          cache.tag_dict[nt]["tagA"]=('0')
          cache.tag_dict[nt]["tagB"]=('0')
          cache.tag_dict[nt]["tagC"]=('0')
          cache.tag_dict[nt]["tagD"]=('0')
          ## Collect Entries per Way to be Printed
          list_tagA.append(cache.tag_dict[nt]["tagA"])
          list_tagB.append(cache.tag_dict[nt]["tagB"])
          list_tagC.append(cache.tag_dict[nt]["tagC"])
          list_tagD.append(cache.tag_dict[nt]["tagD"])
      
      #Printing to Files {.hex}
      for a in (list_cacheA):
        if(a!=""):
          #print("\nSetA",hex(int(a)))
          #dCacheA.write((a))
          dCacheA.write(str(hex(int(a)))+'\n')
      
      print("List Cache Final",str(int(len(list_cacheB))))
      for b in (list_cacheB):
        if(b!=""):
          #print(b)
          #print("\nSetB",hex(int(b)))
          #dCacheB.write((b))
          dCacheB.write(str(hex(int(b)))+'\n')

      for c in (list_cacheC):
        if(c!=""):
          #print("\nSetC",hex(int(c)))
          dCacheC.write(str(hex(int(c)))+'\n')

      for d in (list_cacheD):
        if(d!=""):
          #print("\nSetD",hex(int(d)))
          dCacheD.write(str(hex(int(d)))+'\n')

      for at in (list_tagA):
        if(at!=""):
          #print("\nTagA",(at))
          dTagA.write(str((at))+'\n')
          
      for bt in (list_tagB):
        if(bt!=""):
          #print("\nSetB",bt)
          dTagB.write(str((bt))+'\n')
          
      for ct in (list_tagC):
        if(ct!=""):
          #print("\nSetC",(ct))
          dTagC.write(str((ct))+'\n')

      for dt in (list_tagD):
        if(dt!=""):
          #print("\nSetD",(dt))
          dTagD.write(str((dt)) +'\n')
      
      dCacheA.close()
      dCacheB.close()
      dCacheC.close()
      dCacheD.close()

      dTagA.close()
      dTagB.close()
      dTagC.close()
      dTagD.close()
        
    # Run the entire cache simulation
    def run_init(self,num_blocks_per_set,num_words_per_block,data,cache_size,replacement_policy,num_addr_bits):
      print("Initialize")
      num_blocks      = cache_size
      num_sets        = num_blocks_per_set
      num_addr_bits   = int(44) 
      num_offset_bits = int(6)
      num_index_bits  = int(6)
      num_tag_bits = int(num_addr_bits - num_index_bits - num_offset_bits)
   
      list_addr=[]

      for k in range(len(data)):
        #print("Address",hex(data[k][0]))
        list_addr.append(data[k][0])

      cache = Cache(
        num_sets=num_sets,
        num_index_bits=num_index_bits)

      self.add_entry(cache,data,list_addr,num_addr_bits,
            num_offset_bits, num_index_bits,num_tag_bits,replacement_policy)

cache_ws= Cache_WarmStart()
#cache_sim.run_simulation(4,[0xaabbccdd,0x11223344,0x55667788,0x99aabbcc,0xaabbccdd,0x11223344,0x55667788,0x99aabbcc],512,'lru',6,[0x00080010040, 0x000800010080])  
cache_ws.run_init(4,64,[(0x00080010040,0xaabbccdd112233445566778899aabbccaabbccdd112233445566778899aabbccaabbccdd112233445566778899aabbccaabbccdd112233445566778899aabbcc),
(0x00080010040,0x112233445566778899aabbccaabbccdd112233445566778899aabbccaabbccdd112233445566778899aabbccaabbccdd112233445566778899aabbccaabbccdd),
(0x00080010040,0x112233445566778899aabbccaabbccdd112233445566778899aabbccaabbccdd112233445566778899aabbccaabbccdd112233445566778899aabbcc11223344),
(0x00080010040,0x112233445566778899aabbccaabbccdd112233445566778899aabbccaabbccdd112233445566778899aabbccaabbccdd112233445566778899aabbccaabbccdd),
(0x00080010080,0x112233445566778899aabbccaabbccdd112233445566778899aabbccaabbccdd112233445566778899aabbccaabbccdd112233445566778899aabbcc77889999),
(0x00080010080,0x112233445566778899aabbccaabbccdd112233445566778899aabbccaabbccdd112233445566778899aabbccaabbccdd112233445566778899aabbccaabbccdd),
(0x00080010080,0x112233445566778899aabbccaabbccdd112233445566778899aabbccaabbccdd112233445566778899aabbccaabbccdd112233445566778899aabbccaabbccdd),
(0x00080010080,0x112233445566778899aabbccaabbccdd112233445566778899aabbccaabbccdd112233445566778899aabbccaabbccdd112233445566778899aabbccaabbccdd),
(0x000800100c0,0x112233445566778899aabbccaabbccdd112233445566778899aabbccaabbccdd112233445566778899aabbccaabbccdd112233445566778899aabbccaabbccdd),
(0x000800100c0,0x112233445566778899aabbccaabbccdd112233445566778899aabbccaabbccdd112233445566778899aabbccaabbccdd112233445566778899aabbccaabbccdd),
(0x000800100c0,0x112233445566778899aabbccaabbccdd112233445566778899aabbccaabbccdd112233445566778899aabbccaabbccdd112233445566778899aabbccaabbccdd),
(0x000800100f0,0x112233445566778899aabbccaabbccdd112233445566778899aabbccaabbccdd112233445566778899aabbccaabbccdd112233445566778899aabbccaabbccdd),
(0x000800100f0,0x112233445566778899aabbccaabbccdd112233445566778899aabbccaabbccdd112233445566778899aabbccaabbccdd112233445566778899aabbccaabbccdd),
(0x000800100f0,0x112233445566778899aabbccaabbccdd112233445566778899aabbccaabbccdd112233445566778899aabbccaabbccdd112233445566778899aabbccaabbccdd),
(0x000800100f0,0x112233445566778899aabbccaabbccdd112233445566778899aabbccaabbccdd112233445566778899aabbccaabbccdd112233445566778899aabbccaabbccdd),
(0x000800100f0,0x112233445566778899aabbccaabbccdd112233445566778899aabbccaabbccdd112233445566778899aabbccaabbccdd112233445566778899aabbccaabbccdd),
(0x000800100f0,0x112233445566778899aabbccaabbccdd112233445566778899aabbccaabbccdd112233445566778899aabbccaabbccdd112233445566778899aabbccaabbccdd),
(0x00080010140,0x112233445566778899aabbccaabbccdd112233445566778899aabbccaabbccdd112233445566778899aabbccaabbccdd112233445566778899aabbccaabbccdd),
(0x00080010140,0x112233445566778899aabbccaabbccdd112233445566778899aabbccaabbccdd112233445566778899aabbccaabbccdd112233445566778899aabbccaabbccdd),
(0x00080010140,0x112233445566778899aabbccaabbccdd112233445566778899aabbccaabbccdd112233445566778899aabbccaabbccdd112233445566778899aabbccaabbccdd),
(0x00080010140,0x112233445566778899aabbccaabbccdd112233445566778899aabbccaabbccdd112233445566778899aabbccaabbccdd112233445566778899aabbccaabbccdd)],512,'lru',6)

