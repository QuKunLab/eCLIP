#!/usr/bin/python
from tabformat import parseTranscriptPeaks, parseTabWithName, packIndividualPeak
from optparse import OptionParser
import sys
#
opts=OptionParser()
usage="run mockenrichment.py\n%prog -p peak file -i merged file -m output mocktab file -o output enrichment peak file "
opts=OptionParser(usage=usage)
opts.add_option("-p", help="peak file generated by last step")
opts.add_option("-i", help="input merged file ")
opts.add_option("-m", help="output mocktab file")
opts.add_option("-o", help="output enrichment peak file")
options,arguments = opts.parse_args()
#
peak=options.p
inputtab=options.i
mocktab=options.m
output=options.o
#
class QueryTab:
    def __init__(self, fileName):
        self.file=open(fileName)
        self.name, self.tab=parseTabWithName(self.file.readline())

    def getTab(self, name):
        if self.name == name:
            return self.tab
        try:
            while True:
                self.name, self.tab = parseTabWithName(self.file.readline())
                if self.name == name:
                    return self.tab
        except:
            print >> sys.stderr, "Files don't match!!"
            sys.exit(-1)


def getRelativeEnrich(mocktab, inputtab, st, en):
    def enrich(tab):
        return sum(tab[st:en+1])
    if mocktab:
        mocked = enrich(mocktab)
        if mocked == 0: return None
        return enrich(inputtab)/mocked
    return None

mockTab = QueryTab(mocktab)
inputtab = QueryTab(inputtab)

peakInput = open(peak)
out = open(output, 'w')

for p in peakInput:
    name, peaks, pv, times = parseTranscriptPeaks(p)
    relEnrich = [getRelativeEnrich(mockTab.getTab(name), inputtab.getTab(name), st, en) for st, en in peaks]
    for (st, en), p, enrich, rel in zip(peaks, pv, times, relEnrich):
        print >> out, packIndividualPeak(name, st, en, p, enrich, rel)
