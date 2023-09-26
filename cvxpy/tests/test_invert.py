import cvxpy as cp
import numpy as np
from cvxpy.reductions.cone2cone.exotic2common import pow_nd_canon



# `ConeMatrixStuffing` test
# x = cp.Variable(shape=(3, 1))
# cone_con = cp.constraints.ExpCone(x[2], x[1], x[0])
# cons = [cp.sum(x) <= 1.0,
#                cp.sum(x) >= 0.1,
#                x >= 0,
#                cone_con]
# obj = cp.Minimize(3 * x[0] + 2 * x[1] + x[2])
# prob = cp.Problem(obj, cons)
# prob.solve(solver='MOSEK', verbose=True)

def runif_in_simplex(n):
  ''' Return uniformly random vector in the n-simplex '''

  k = np.random.exponential(scale=1.0, size=n)
  return k / sum(k)

# Simple `PowConeND` projection problem:
# axis = 1
dims = 6
x = cp.Variable(shape=(dims,))
x_power = cp.Variable(shape=(dims,))
alpha = runif_in_simplex(dims - 1)
pow_con = cp.PowConeND(x_power[:dims - 1], x_power[dims - 1], alpha)
obj = cp.Minimize(cp.norm(x - x_power))
canon_cons = pow_nd_canon(pow_con, pow_con.args[:2])[0]
cons = [pow_con,
        cp.bmat([[87 * x[0], x[1], x[2] / 3],
                  [100.0, 4 * 1e2, x[3] * 78],
                  [23 * x[4], 1e3, x[5]/144]]) >> 0]
prob = cp.Problem(obj, cons)
print(prob.solve(solver='MOSEK'))
f = lambda x: x.value
print(f"Dual vals: {pow_con.dual_value}")

# print(f"Canonicalization cons: {list(map(f, canon_cons.args))}")
# print(f"Dual vals: {np.vstack(canon_cons.dual_value)}")
# print(f"Alpha: {canon_cons.alpha}")
# print(f"Other cons: {cons[1].dual_value, cons[2].dual_value}")

# L = -obj + cp.scalar_product(cons[0].dual_value, cons[0].expr)
#          - cp.scalar_product(cons[1].args)

# `Exotic2Common` test
# axis = 0
# x = cp.Variable(shape=(3,))
# hypos = cp.Variable(shape=(2,))
# obj = cp.Maximize(cp.sum(hypos) - x[0])
# W = cp.bmat([[x[0], x[2]],
#                 [x[1], 1.0]])
# alpha = np.array([[0.2, 0.4],
#                     [0.8, 0.6]])
# if axis == 1:
#     W = W.T
#     alpha = alpha.T
# con = cp.PowConeND(W, hypos, alpha, axis=axis)
# cons = [
#     x[0] + x[1] + 0.5 * x[2] == 2,
#     # cp.PowConeND(W, hypos, alpha, axis=axis)
#     pow_nd_canon(con, (W, hypos))[0]
# ]
# prob = cp.Problem(obj, cons)
# print(prob.solve(solver='MOSEK'))
# print(np.vstack(cons[1].dual_value))
