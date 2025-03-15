from sympy import * 

x,y,z,a,b= symbols('x y z a b', real=True)

xp = a*x + b*y +z
yp = 3*x + y + 5*z
zp = y/3 + z

m = Matrix([[diff(xp,x),diff(xp,y),diff(xp,z)],[diff(yp,x),diff(yp,y),diff(yp,z)],[diff(zp,x),diff(zp,y),diff(zp,z)]])

v = Matrix([1,5,11])
print("------------------")

print(latex(m*v))
print("------------------")

r = sqrt(x**2 +y**2)
phi = atan(y/x)

m = Matrix([[diff(r,x),diff(r,y)],[diff(phi,x),diff(phi,y)]])

print(latex(m))
print("--------------------------")
r, varphi = symbols('r , varphi',real=True)
j = Matrix([[cos(varphi),sin(varphi)],[-sin(varphi)/r ,cos(varphi)/r]])

x = r*cos(varphi)
y = r*sin(varphi)
a_nu = Matrix([x**2 , 2*y**2])

print(latex(j*a_nu))