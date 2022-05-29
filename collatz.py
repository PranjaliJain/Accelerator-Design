import pyrtl

inp = pyrtl.Input(32,name="input")
n = pyrtl.Register(32, name='n')
out = pyrtl.Output(32, name="output")
cycle = pyrtl.Register(bitwidth=32, name='cycle')

with pyrtl.conditional_assignment:
    with cycle ==0:
        n.next |= inp
        cycle.next |= cycle + 1 
    with n == 1:
        out |= cycle
    with n & 1 == 0:
        n.next |= pyrtl.shift_right_arithmetic(n,1)
        cycle.next |= cycle + 1
    with n & 1 == 1:
        n.next |= 3*n + 1
        cycle.next |= cycle + 1


sim_trace = pyrtl.SimulationTrace()
sim = pyrtl.Simulation(tracer=sim_trace)
for cycle in range(15):
    sim.step({
        'input' : 10
    })
num_cycles = sim.inspect(out)

sim_trace.render_trace()

print("Number of cycles to reach 1: ", num_cycles)

# with open(f"collatz.gv", 'w') as f:
        # pyrtl.output_to_graphviz(f)