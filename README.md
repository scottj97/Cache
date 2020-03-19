# Cache
Python Program to Fill Up the Cache during Initialization
Cache Warmstarter Design
========================
Goal: initialize CPU cache memories to a warmed-up state before
starting simulation.

How: create a series of *.hex files, one per RAM, which the testbench
will load at simulation startup via $readmemh().

Cache Configuration
-------------------
The data cache is 16384 bytes, 4-way set associative, 64 byte line
size. Each way is composed of two RAMs: tag and data, with 64 entries
each.

The design looks up an entry in the cache based on a 44-bit physical
address like so:

paddr[5:0]: offset within line
paddr[11:6]: index into cache arrays
paddr[43:12]: tag

Each tag is 33 bits wide:
tag[32]: valid
tag[31:0]: paddr[43:12]



Input
-----
A Python data structure: list of tuples of (address, data_string). For example:                                                                               

data = [
    (0x000_80010040, "aabbccdd_11223344_55667788_99aabbcc_aabbccdd_11223344_55667788_99aabbcc_aabbccdd_11223344_55667788_99aabbcc_aabbccdd_11223344_55667788_99aabbcc"),
    (0x000_80010080, "11223344_55667788_99aabbcc_aabbccdd_11223344_55667788_99aabbcc_aabbccdd_11223344_55667788_99aabbcc_aabbccdd_11223344_55667788_99aabbcc_aabbccdd"),
]

Output
------
Eight files, each with 64 lines of hex numbers:
dtagA.hex
dtagB.hex
dtagC.hex
dtagD.hex
dcacheA.hex
dcacheB.hex
dcacheC.hex
dcacheD.hex


### Script
The script has following features :-     
-- It will fill up the Cache according to the User Input for the Given Index and Way in that Index  
-- If the same address is given again, the script will use LRU scheme to replace the Tag and Data     
-- If the User Doesn't give addresses to cover all 64 Sets of the Cache, then the Script will automatically initialize them to be zero
