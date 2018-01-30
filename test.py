import sys

for i in range(1000):
    sys.stdout.write('Hey ' + str(i) + '\r')
    sys.stdout.flush()

print()
