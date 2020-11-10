"""
git: https://github.com/mirceachira/flcd_class/blob/main/lab_3.py

BNF Representation of the input file:

symbol := 0 | 1 | 2 | ... | 9
start_symbol := symbol
<is_final> := 0 | 1
value := 'a' | 'b' | 'c' | ... | 'z'
value_symbol_pair := value symbol
array_of_values := value_symbol_pair | value_symbol_pair symbol array_of_values
first_row := start_symbol is_final array_of_values
secondary_row := symbol is_final array_of_values
multiple_rows := secondary_row | secondary_row multiple_rows
program := first_row | first_row multiple_rows

Input file examples:
file 1:
0 0 a 1 b 3
1 1 a 1 b 2
2 1 a 1 b 3
3 0 a 3 b 3

file 2:
0 0 a 1 b 3
1 1 a 1 b 2 a 3 b 3
2 1 a 1 b 3
3 0 a 3

file 3:
0 0 a 1 b 3
1 1 a 1 b 2
2 1 a 1

"""


class FiniteAutomaton:

    def __init__(self, filename):
        self.states = []
        self.final_states = []
        self.input_symbols = []
        self.transitions = {}

        with open(filename, 'r') as f:
            automaton_string = f.read()

        rows = automaton_string.split('\n')
        
        self.get_row_data(rows[0], is_initial_state=True)
        for row in rows[1:]:
            self.get_row_data(row)

    def get_row_data(self, row_string, is_initial_state=False):
        # 1 1 a 1 b 2 a 3 b 3
        
        q, is_final, *others = row_string.split()
        is_final = is_final == '1'

        self.states.append(q)
        
        if is_final:
            self.final_states.append(q)
        
        if is_initial_state:
            self.initial_state = q

        self.input_symbols = set(list(self.input_symbols) + others[::2])
        self.transitions[q] = dict(zip(others[1::2], others[::2]))

    def __str__(self):
        automaton_string_representation = f"""
    Finite Automaton
        Initial state: Q{self.initial_state}
        Final states: {', '.join(sorted([f'Q{s}' for s in self.final_states]))}
        Full set of states: {', '.join(sorted([f'Q{s}' for s in self.states]))}
        Alphabet: {', '.join(sorted(list(self.input_symbols)))}
        Transitions:"""
        
        for state, arrows in self.transitions.items():
            valued_arrows = ' | '.join([f'{val}Q{s}' for s, val in arrows.items()]) 
            automaton_string_representation += f'\n\t\tQ{state} -> {valued_arrows}'
        
        return automaton_string_representation
        
    ### BONUS
    def recursive_test_nodes(self, token, current_node):
        if (token == '') or (current_node not in self.transitions):
            return (token == '') and (current_node in self.final_states)
        
        result = False
        for key, value in self.transitions[current_node].items():
            if token[0] == value:
                result = result or self.recursive_test_nodes(token[1:], key)

        return result

    def validate_token(self, token): # abc
        return self.recursive_test_nodes(token, self.initial_state)
        

with open('FA.in', 'w') as f:
    f.write("""0 0 a 1 b 3
1 1 a 1 b 2 a 3 b 3
2 1 a 1 b 3
3 0 a 3""")

# Finite Automaton
#         Initial state: Q0
#         Final states: Q1, Q2
#         Full set of states: Q0, Q1, Q2, Q3
#         Alphabet: a, b
#         Transitions:
# 		Q0 -> aQ1 | bQ3
# 		Q1 -> aQ1 | bQ2 | bQ3
# 		Q2 -> aQ1 | bQ3
# 		Q3 -> aQ3

fa = FiniteAutomaton("FA.in")
print(fa.validate_token("abc"))   # False
print(fa.validate_token("a"))     # True
print(fa.validate_token("aaaa"))  # True
print(fa.validate_token("bb"))    # False


## Base tests
# with open('FA.in', 'w') as f:
#     f.write("""0 0 a 1 b 3
# 1 1 a 1 b 2
# 2 1 a 1 b 3
# 3 0 a 3 b 3""")

# print(FiniteAutomaton("FA.in"))

# with open('FA.in', 'w') as f:
#     f.write("""0 0 a 1 b 3
# 1 1 a 1 b 2 a 3 b 3
# 2 1 a 1 b 3
# 3 0 a 3""")

# print(FiniteAutomaton("FA.in"))

with open('FA.in', 'w') as f:
    f.write("""0 0 a 1 b 3
1 1 a 1 b 2
2 1 a 1""")

print(FiniteAutomaton("FA.in"))
