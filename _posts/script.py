import pygame
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((400, 450))
pygame.display.set_caption("Quantum Tic-Tac-Toe")
font = pygame.font.SysFont("arial", 24)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
QUANTUM_BLUE = (0, 191, 255)
ENTANGLED_PURPLE = (128, 0, 128)

# Game State
game_board = [None] * 9
quantum_circuit = QuantumCircuit(9, 9)
current_player = 'X'
move_count = 0
game_over = False
selected_cell = None
is_entangling = False
first_entangle_cell = None
DEBUG = True

def draw_board():
    screen.fill(WHITE)
    for i in range(1, 3):
        pygame.draw.line(screen, BLACK, (i * 133, 0), (i * 133, 400), 2)
        pygame.draw.line(screen, BLACK, (0, i * 133), (400, i * 133), 2)

    for i in range(9):
        x_pos = (i % 3) * 133 + 50
        y_pos = (i // 3) * 133 + 50

        if game_board[i] == 'Q':
            pygame.draw.circle(screen, QUANTUM_BLUE, (x_pos, y_pos), 30)
            screen.blit(font.render('?', True, BLACK), (x_pos-5, y_pos-10))
        elif game_board[i] == 'E':
            pygame.draw.circle(screen, ENTANGLED_PURPLE, (x_pos, y_pos), 30)
            screen.blit(font.render('E', True, WHITE), (x_pos-5, y_pos-10))
        elif game_board[i] in ['X', 'O']:
            screen.blit(font.render(game_board[i], True, BLACK), (x_pos-10, y_pos-10))
        elif selected_cell == i:
            pygame.draw.rect(screen, GRAY, (x_pos-40, y_pos-40, 80, 80), 2)
            screen.blit(font.render('?', True, GRAY), (x_pos-5, y_pos-10))

    buttons = [
        {"text": "Classical", "x": 10, "color": GRAY},
        {"text": "Hadamard", "x": 120, "color": QUANTUM_BLUE},
        {"text": "Entangle", "x": 230, "color": ENTANGLED_PURPLE},
        {"text": "End Game", "x": 340, "color": BLACK}
    ]

    for btn in buttons:
        pygame.draw.rect(screen, btn["color"], (btn["x"], 410, 100, 30))
        color = BLACK if btn["color"] != BLACK else WHITE
        screen.blit(font.render(btn["text"], True, color), (btn["x"]+10, 415))

    status = [
        f"Player Turn: {current_player}",
        f"Move Count: {move_count}",
        f"Selected: {selected_cell if selected_cell is not None else 'None'}",
        f"Entangling: {is_entangling}",
        f"First Cell: {first_entangle_cell if first_entangle_cell is not None else 'None'}"
    ]

    for i, line in enumerate(status):
        screen.blit(font.render(line, True, BLACK), (10, 350 + i * 20))

    if game_over:
        screen.blit(font.render("Game Over", True, BLACK), (150, 200))

    pygame.display.flip()

def apply_classical_move():
    global move_count, current_player, selected_cell
    if selected_cell is not None and game_board[selected_cell] is None and not game_over:
        game_board[selected_cell] = current_player
        if DEBUG:
            print(f"[DEBUG] Classical move by {current_player} at square {selected_cell}")
        move_count += 1
        current_player = 'O' if current_player == 'X' else 'X'
        selected_cell = None
        draw_board()

def apply_hadamard():
    global move_count, current_player, selected_cell
    if selected_cell is not None and game_board[selected_cell] is None and not game_over:
        quantum_circuit.h(selected_cell)
        game_board[selected_cell] = 'Q'
        if DEBUG:
            print(f"[DEBUG] {current_player} applied Hadamard gate at {selected_cell}")
        move_count += 1
        current_player = 'O' if current_player == 'X' else 'X'
        selected_cell = None
        draw_board()

def apply_entangle(cell1, cell2):
    global move_count, current_player, is_entangling, first_entangle_cell
    if game_board[cell1] is None and game_board[cell2] is None and cell1 != cell2 and not game_over:
        quantum_circuit.h(cell1)
        quantum_circuit.cx(cell1, cell2)
        game_board[cell1] = 'E'
        game_board[cell2] = 'E'
        if DEBUG:
            print(f"[DEBUG] {current_player} entangled cells {cell1} and {cell2}")
        move_count += 1
        current_player = 'O' if current_player == 'X' else 'X'
        is_entangling = False
        first_entangle_cell = None
        draw_board()

def measure_board():
    global game_over
    simulator = AerSimulator()
    job = simulator.run(quantum_circuit, shots=1)
    result = job.result()
    counts = result.get_counts()
    final_state = list(counts.keys())[0][::-1]  # Reverse bit order

    if DEBUG:
        print("\n[DEBUG] Final Quantum Measurement Result:")
        print(f"Measured bitstring (qubit 8 to 0): {final_state}")

    for i in range(9):
        if game_board[i] in ['Q', 'E']:
            game_board[i] = 'X' if final_state[i] == '0' else 'O'
            if DEBUG:
                print(f"  - Square {i}: {game_board[i]}")

    game_over = True
    draw_board()

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            x, y = event.pos
            if y < 400:
                cell = (y // 133) * 3 + (x // 133)
                if 0 <= cell < 9 and game_board[cell] is None:
                    if is_entangling:
                        if cell != first_entangle_cell:
                            apply_entangle(first_entangle_cell, cell)
                        else:
                            if DEBUG:
                                print("[DEBUG] Cannot entangle a cell with itself")
                    else:
                        selected_cell = cell
            else:
                if 10 < x < 110 and 410 < y < 440:
                    apply_classical_move()
                elif 120 < x < 220 and 410 < y < 440:
                    apply_hadamard()
                elif 230 < x < 330 and 410 < y < 440:
                    if selected_cell is not None and game_board[selected_cell] is None:
                        first_entangle_cell = selected_cell
                        is_entangling = True
                        selected_cell = None
                        if DEBUG:
                            print(f"[DEBUG] Preparing to entangle from cell {first_entangle_cell}")
                    else:
                        if DEBUG:
                            print("[DEBUG] Select a valid cell first for entangling")
                elif 340 < x < 440 and 410 < y < 440:
                    measure_board()
    draw_board()

pygame.quit()
