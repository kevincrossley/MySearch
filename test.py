# Lightbulb $.5 1s
# register $.001 .4ns
# DRAM n$ .58	12ns

c = 300000 #km/s
lb = c*1.
rg = c*(1000/1)*(1./1000000000)*.4
dm = c*(1000/1)*(1./1000000000)*12

print lb, rg, dm