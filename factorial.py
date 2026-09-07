#First method.
import math
n=int(input("Enter the number :"))
fact=math.factorial(n-1+1)
print(fact)



#Alternate method.
import math
n=int(input("Enter the number :"))
fact=1
for i in range(1,n+1):
    fact = fact*i
print(fact)