import pyrtl 
import pyrtl.rtllib.matrix as Matrix
import random

''' Example matrices
a_vals = [[1, 2], [3, 4]]
b_vals = [[2, 4], [8, 10]]
a_vals = [[1, 2, 1, 2], [3, 4, 1, 2], [1, 2, 1, 2], [3, 4, 1, 2]]
b_vals = [[2, 4, 1 ,2], [8, 10, 1, 2], [2, 4, 1 ,2], [8, 10, 1, 2]]
'''

bits = 32

def create_matrix(m, n, p):
    a_ = [[random.randint(0, 10) for e in range(n)] for e in range(m)]
    b_ = [[random.randint(0, 10) for e in range(p)] for e in range(n)]
    return a_, b_

# Multipication of mxn and nxp matrics
m, n, p = 8, 8, 8
a_vals, b_vals = create_matrix(m, n, p)

print("Input matrices: \n", a_vals, '\n', b_vals)

a_in = pyrtl.Input(m * n * bits, 'a_in')
b_in = pyrtl.Input(n * p * bits, 'b_in')
a = Matrix.Matrix(m, n, bits, value=a_in)
b = Matrix.Matrix(n, p, bits, value=b_in)

output = pyrtl.Output(name='output')
c = a @ b
output <<= c.to_wirevector()


# Simulation
sim = pyrtl.Simulation()
sim.step({
    'a_in': Matrix.list_to_int(a_vals, bits),
    'b_in': Matrix.list_to_int(b_vals, bits)
})

out_matrix = Matrix.matrix_wv_to_list(sim.inspect('output'), m, p, c.bits)
print("Output matrices: \n", out_matrix)


# Timing and area analysis
def timing_analysis():
    ta = pyrtl.TimingAnalysis()
    print("Max frequency: ",{ta.max_freq()}," MhZ")
    print("Max timing delay: ",{ta.max_length()}," ps")

def area_est():
    logic, mem = pyrtl.area_estimation()
    print("Logic area est:", {logic})


print('Synthesizing....')
pyrtl.synthesize()
timing_analysis()
area_est()

print('\n')

print('Optimizing....')
pyrtl.optimize()
timing_analysis()
area_est()