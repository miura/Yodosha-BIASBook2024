import jarray
 
#create example data arrays
xa = [1, 2, 3, 4]
ya = [3, 3.5, 4, 4.5]
 
#convert to java arrays
jxa = jarray.array(xa, 'i')
jya = jarray.array(ya, 'd')
print(jxa)
print(jya)
