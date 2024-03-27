"""
ITCS 6150 - Intelligent Systems
Project 2: Solving N-queens problem using hill-climbing search and its variants
Porject by : 
1. Srushti Sanjay Samant (801198218)
2. Himanshu Kiran Garud  (801365910)
"""


#Import Statements
import random
import sys

'''Crteating a NQueen Class'''
class NQueens:


    def __init__(self, n=8):
        self.n = n
        self.reset_board()

    # Reset Board Function
    def reset_board(self):
        """Resets the board to a new random state."""
        self.board = [random.randint(0, self.n - 1) for _ in range(self.n)]

    # Print Board Function
    def print_board(self, heuristic):
        """Prints the board and the current heuristic value."""
        for i in range(self.n):
            row = ['x' if self.board[j] != i else 'Q' for j in range(self.n)]
            print(" ".join(row))
        print(f"heuristic (conflicting pairs): {heuristic}\n")

    # Heuristic Function
    def get_heuristic(self, board=None):
        """Calculates the number of conflicting pairs of queens on the board."""
        if board is None:
            board = self.board
        conflicts = 0
        for i in range(self.n):
            for j in range(i + 1, self.n):
                if board[i] == board[j] or abs(board[i] - board[j]) == j - i:
                    conflicts += 1
        return conflicts
    
    # Function to identify the best move that is available in the current state
    def find_move(self, sideways_moves_allowed=False):
        """Finds the best move; allows sideways moves if specified."""
        best_heuristic = self.get_heuristic()
        best_moves = []
        for col in range(self.n):
            original_row = self.board[col]
            for row in range(self.n):
                if row == original_row:
                    continue  # Skip the current position
                self.board[col] = row
                heuristic = self.get_heuristic()
                if heuristic < best_heuristic:
                    best_heuristic = heuristic
                    best_moves = [(col, row)]
                elif heuristic == best_heuristic and sideways_moves_allowed:
                    best_moves.append((col, row))
                self.board[col] = original_row  # Reset to original position
        return best_moves, best_heuristic

    # Function to implement the Hill Climbing algorithm
    def hill_climbing(self, variant='basic', max_sideways=100):
        steps = 0
        success = False
        restarts = 0 if variant.startswith('random_restart') else None
        sideways_moves_left = max_sideways if variant.endswith('sideways') else 0

        while True:
            current_heuristic = self.get_heuristic()
            if current_heuristic == 0:
                success = True
                break  # Solution found

            best_moves, best_heuristic = self.find_move(sideways_moves_allowed=variant.endswith('sideways'))
            
            if best_moves:
                if best_heuristic < current_heuristic or (variant.endswith('sideways') and sideways_moves_left > 0 and best_heuristic == current_heuristic):
                    move = random.choice(best_moves)
                    self.board[move[0]] = move[1]
                    if variant.endswith('sideways') and best_heuristic == current_heuristic:
                        sideways_moves_left -= 1
                    steps += 1
                else:
                    if restarts is not None:
                        self.reset_board()
                        restarts += 1
                        sideways_moves_left = max_sideways if variant.endswith('sideways') else 0
                    else:
                        break  # No improvement or restarts left
            else:
                if restarts is not None:
                    self.reset_board()
                    restarts += 1
                    sideways_moves_left = max_sideways if variant.endswith('sideways') else 0
                else:
                    break  # No moves and no restarts left

        return steps, self.get_heuristic(), success, restarts
    

''' This function handles running tests to solve the N-Queens problem with different setups and 
versions of the hill climbing algorithm.'''
def N_Queens():

    # Choose the number of Queens

    n_choice = input("\nDo you want the number of queens to be default (8)? (yes/no): ").lower()
    if n_choice == 'yes':
        n = 8
    elif n_choice == 'no':
        n = int(input("\nEnter the number of queens: "))
    else:
        print("\nInvalid choice.")
        print("\nExiting the program")
        sys.exit()

    # Choose the desired number of iterations 
    
    iterations_choice = input("\nSelect from the following iterations:\n1. 50\n2. 100\n3. 1500\n4. Enter the number of iterations\nChoice: ")
    if iterations_choice == '1':
        iterations = 50
    elif iterations_choice == '2':
        iterations = 100
    elif iterations_choice == '3':
        iterations = 1500
    elif iterations_choice == '4':
        iterations = int(input("\nEnter the number of iterations: "))
    else:
        print("\nInvalid choice.")
        print("\nExiting the program")
        sys.exit()

    # Choose the variation of Hill Climbing 
    variant_choice = input("\nWhich variation of Hill Climbing do you want to use?\n1. Hill Climbing without Sideways moves\n2. Hill-climbing search with sideways move\n3. Random-restart hill-climbing search without sideways moves\n4. Random-restart hill-climbing search with sideways moves\nChoice: ")
    if variant_choice == '1':
        variant = 'basic'
    elif variant_choice == '2':
        variant = 'sideways'
    elif variant_choice == '3':
        variant = 'random_restart'
    elif variant_choice == '4':
        variant = 'random_restart_sideways'
    else:
        print("\nInvalid choice.")
        print("\nExiting the program")
        sys.exit()

    # Initializing variables for tracking the results
    total_success = 0
    total_steps = 0
    total_failures = 0
    total_restarts = 0
    success_steps = []
    failure_steps = []

    # Run the loop for the specified number of iterations 
    for i in range(iterations):
        print(f"\n--- Iteration {i+1} / Variant: {variant} ---")
        problem = NQueens(n)
        problem.print_board(problem.get_heuristic())
        steps, final_heuristic, success, restarts = problem.hill_climbing(variant)
        print(f"Iteration {i+1} Summary: {'Success' if success else 'Failure'}, Steps: {steps}, Final Heuristic: {final_heuristic}, Restarts: {restarts}")

        if success:
            total_success += 1
            success_steps.append(steps)
        else:
            total_failures += 1
            failure_steps.append(steps)
        if restarts is not None:
            total_restarts += restarts
        total_steps += steps

    print("\n\n--- Summary of Results ---")
    total_runs = iterations
    success_rate = (total_success / total_runs) * 100
    failure_rate = (total_failures / total_runs) * 100 if total_runs != 0 else 0
    avg_restarts = total_restarts / total_success if total_success > 0 else 0
    avg_steps = total_steps / total_runs
    avg_success_steps = sum(success_steps) / len(success_steps) if success_steps else 0
    avg_failure_steps = sum(failure_steps) / len(failure_steps) if failure_steps else 0


    # Prints Summary Results
    print(f"Total Number of Runs: {total_runs}")
    print(f"Total Successful Runs: {total_success}, Success Rate: {success_rate}%")
    print(f"Total Failures: {total_failures}, Failure Rate: {failure_rate}%")
    if variant in ['random_restart', 'random_restart_sideways']:
        print(f"Total Number of Random Restarts: {total_restarts}")
        print(f"Average Number of Random Restarts: {avg_restarts}")
    print(f"Average Number of Steps: {avg_steps}")

    if variant in ['basic', 'sideways']:
        print(f"Average Number of Steps (Success): {avg_success_steps}")
        print(f"Average Number of Steps (Failure): {avg_failure_steps}")

# Main function
if __name__ == '__main__':
    # Calling N_Queens() function inside the main function
    N_Queens()
