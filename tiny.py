"a tiny module"
print(dir())
# list() superfluous on 2.x, on 3.x it is necessary because
# items() returns live iterator to the changing directory
for k,v in list(locals().items()):
    print("%s:%r" % (k,v if len(repr(v)) < 123 else type(v)))
del k,v
import sys
print("argv:{0!r}".format(sys.argv))
del sys
