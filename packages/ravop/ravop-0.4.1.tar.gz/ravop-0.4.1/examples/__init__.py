from dotenv import load_dotenv

load_dotenv()

import ravop as R

R.initialize("12345")
g = R.Graph(name="My graph", algorithm="add", approach="distributed")
a = R.t(10)
b = R.t(20)

c = a+b
print(c())

g.end()
