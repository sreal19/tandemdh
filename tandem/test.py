__author__ = 'sbr'

key = 'name'
d1 = {}
d1.setdefault(key, []).append('Jim')
d1.setdefault(key, []).append('Bill')
d1.setdefault(key, []).append('Bob')
print d1

list_of_values = d1[key]
print list_of_values
print 'blue'
for key,val in d1.iteritems():
    print key,val
