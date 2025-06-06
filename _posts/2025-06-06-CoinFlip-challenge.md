# 🎮 Quantum Coin Flip Challenge

Welcome to the **Quantum Coin Flip Challenge**! In this fun and simple game, you'll learn how quantum computers can flip a coin in a way that's different from regular computers — using the power of quantum physics!

This tutorial is designed beginners. By the end, you'll understand some basic ideas in quantum computing and how to write your first quantum game in Python.

## 🧠 What is Quantum Computing?

Before we begin, let’s understand what makes quantum computers special:

* **Classical computers** use bits: either `0` or `1`.
* **Quantum computers** use qubits: they can be `0`, `1`, or a mix of both — this is called **superposition**.
* Quantum computers also use **interference** to increase or decrease the chances of outcomes.
* When you **measure** a qubit, it picks one outcome: 0 or 1.

## 🪙 What is a Quantum Coin?

Imagine a regular coin: heads or tails. In a quantum world:

* The coin can be in a state that is **both heads and tails** at once.
* When you flip it, it lands on either heads or tails — but **you can bias the flip** using quantum logic!

In this game:

* You get 5 flips.
* You can use a limited amount of quantum power.
* You apply this power to **tilt** the quantum coin.
* Use **negative power** to make heads more likely, **positive power** for tails.

## ⚙️ Setting Up Your Game

First, let’s install the tools we need:

```bash
pip install qiskit qiskit-aer matplotlib numpy
```

## 🛠️ Step-by-Step Code Breakdown

Let’s build the game in small parts.

### 1. Import Libraries

These libraries help with quantum computing, math, and plotting.

```python
import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
import matplotlib.pyplot as plt
```

* `numpy`: for math.
* `qiskit`: for creating quantum circuits.
* `AerSimulator`: to simulate the quantum flips.
* `matplotlib`: to visualize probabilities.

### 2. Define Game Rules

```python
MAX_POWER = np.pi / 2 
FLIPS = 5
```

* You get 5 coin flips.
* You have a limited amount of quantum power: about 1.57.

Why power? Because we use it to tilt the quantum coin using the **RY gate**, which rotates a qubit around the Y-axis.

### 3. Game Introduction

```python
print("🎮 QUANTUM COIN FLIP CHALLENGE!")
print("================================")
print(f"• You have {FLIPS} quantum coin flips")
print(f"• Total quantum power: {MAX_POWER:.2f}")
print("• Use NEGATIVE numbers for HEADS bias (⚪)")
print("• Use POSITIVE numbers for TAILS bias (⚫)")
print("================================")
```

This prints your game instructions.

### 4. Get User Inputs

```python
powers = []
remaining_power = MAX_POWER

while len(powers) < FLIPS and remaining_power > 0:
    try:
        power = float(input(f"\n⚛️ FLIP {len(powers)+1}: Enter quantum power: "))
        if abs(power) <= remaining_power:
            powers.append(power)
            remaining_power -= abs(power)
            print(f"   Remaining power: {remaining_power:.2f}")
        else:
            print(f"❌ Too much power! Max left: {remaining_power:.2f}")
    except ValueError:
        print("Please enter a number (ex: -0.5 or 0.3)")

while len(powers) < FLIPS:
    powers.append(0.0)
    print(f"⚠️  Flip {len(powers)}: No power left, auto-setting to 0.0")
```

You get to enter a value for each flip. This controls how much you tilt the quantum coin.

Use less power in early turns so you have enough later!

### 5. Simulate Quantum Flips

Now comes the quantum part!

```python
simulator = AerSimulator()
results = []

for i, power in enumerate(powers):
    qc = QuantumCircuit(1, 1)
    qc.ry(2 * power, 0) 
    qc.h(0)             
    qc.measure(0, 0)   
```

* `ry(2 * power, 0)`: rotates the qubit. Negative = more heads, positive = more tails.
* `h(0)`: creates a superposition. The coin is both heads and tails until measured.
* `measure`: collapses it into heads or tails.

### 6. Calculate Probabilities

```python
    job = simulator.run(qc, shots=1000)
    result = job.result()
    counts = result.get_counts()

    prob_heads = counts.get('1', 0) / 1000
    prob_tails = counts.get('0', 0) / 1000
```

We simulate 1000 flips to see how likely heads or tails is.

### 7. Visualize Each Flip

```python
    plt.subplot(1, FLIPS, i+1)
    plt.bar(['HEADS', 'TAILS'], [prob_heads, prob_tails], color=['blue', 'red'])
    plt.title(f"Flip {i+1}\nPower={power:.2f}")
    plt.ylim(0, 1)
```

This draws a bar chart showing how your quantum coin was biased.

### 8. Get Actual Result of One Flip

```python
    job = simulator.run(qc, shots=1)
    result = job.result()
    counts = result.get_counts()
    outcome = "HEADS ✅" if '1' in counts else "TAILS ❌"
    results.append(outcome)
```

This time we simulate only **1 shot** — this is your actual coin result.

### 9. Show Results

```python
heads_count = sum(1 for r in results if "HEADS" in r)
print("\n⭐ GAME RESULTS ⭐")
print("====================")
print(f"Powers used: {powers}")
print(f"Flip outcomes: {results}")
print(f"TOTAL HEADS: {heads_count}/{FLIPS}")

if heads_count == FLIPS:
    print("🌟 QUANTUM MASTER! Perfect score!")
elif heads_count >= 3:
    print("👍 Great job! You're getting quantum!")
else:
    print("💡 Nice try! Use more negative power next time!")
```

We count how many heads you got and give you feedback.

### 10. Save Your Chart

```python
plt.tight_layout()
plt.savefig('quantum_probabilities.png')
print("\n📊 Check 'quantum_probabilities.png' to see your flip probabilities!")
```

Now you can see how each flip was biased — and how well you did!

Here is the full game in single code snippet: 

```python
# quantum_coin.py
import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
import matplotlib.pyplot as plt

# Game settings
MAX_POWER = np.pi / 2  # Total quantum power (≈1.57)
FLIPS = 5  # Number of coin flips

def initialize_game():
    """Initialize the quantum coin flip challenge."""
    print("\n🎮 QUANTUM COIN FLIP CHALLENGE!")
    print("================================")
    print(f"• You have {FLIPS} quantum coin flips")
    print(f"• Total quantum power: {MAX_POWER:.2f}")
    print("• Use NEGATIVE numbers for HEADS bias (⚪)")
    print("• Use POSITIVE numbers for TAILS bias (⚫)")
    print("================================")

def validate_power(power, remaining):
    """Validate quantum power input."""
    try:
        power = float(power)
        return abs(power) <= remaining
    except ValueError:
        return False

def get_player_input(remaining_power):
    """Get validated quantum power input from player."""
    while True:
        try:
            power = float(input(f"\n⚛️ FLIP {len(powers)+1}: Enter quantum power: "))
            if abs(power) <= remaining_power:
                return power
            print(f"❌ Too much power! Max left: {remaining_power:.2f}")
        except ValueError:
            print("Please enter a number (ex: -0.5 or 0.3)")

def simulate_flip(circuit):
    """Simulate a quantum coin flip."""
    simulator = AerSimulator()
    job = simulator.run(circuit, shots=1000)
    result = job.result()
    counts = result.get_counts()
    
    prob_heads = counts.get('1', 0) / 1000
    prob_tails = counts.get('0', 0) / 1000
    
    return prob_heads, prob_tails

def determine_outcome(circuit):
    """Determine the actual outcome of a flip."""
    simulator = AerSimulator()
    job = simulator.run(circuit, shots=1)
    result = job.result()
    counts = result.get_counts()
    
    return "HEADS ✅" if '1' in counts else "TAILS ❌"

# Initialize game state
powers = []
remaining_power = MAX_POWER

# Game initialization
initialize_game()

# Get player's quantum power choices
while len(powers) < FLIPS:
    power = get_player_input(remaining_power)
    remaining_power -= abs(power)
    powers.append(power)
    print(f"   Remaining power: {remaining_power:.2f}")

# Fill remaining flips with zero power if user ran out
while len(powers) < FLIPS:
    powers.append(0.0)
    print(f"⚠️  Flip {len(powers)}: No power left, auto-setting to 0.0")    

# Quantum coin flipping simulation
print("\n🌀 Quantum magic happening...")
plt.figure(figsize=(10, 5))

results = []
for i, power in enumerate(powers):
    # Create quantum circuit (1 qubit, 1 output)
    qc = QuantumCircuit(1, 1)
    
    # QUANTUM OPERATIONS
    qc.ry(2 * power, 0)  # Tilt the coin
    qc.h(0)              # Put in superposition (make it quantum!)
    qc.measure(0, 0)     # Measure (collapse to heads/tails)
    
    # Calculate probabilities
    prob_heads, prob_tails = simulate_flip(qc)
    
    # Plot probability distribution
    plt.subplot(1, FLIPS, i+1)
    plt.bar(['HEADS', 'TAILS'], [prob_heads, prob_tails], color=['blue', 'red'])
    plt.title(f"Flip {i+1}: Power={power:.2f}")
    plt.ylim(0, 1)
    
    # Determine actual outcome
    outcome = determine_outcome(qc)
    results.append(outcome)

# Show game results
heads_count = sum(1 for r in results if "HEADS" in r)
print("\n⭐ GAME RESULTS ⭐")
print("====================")
print(f"Powers used: {powers}")
print(f"Flip outcomes: {results}")
print(f"TOTAL HEADS: {heads_count}/{FLIPS}")

# Provide feedback
if heads_count == FLIPS:
    print("🌟 QUANTUM MASTER! Perfect score!")
elif heads_count >= 3:
    print("👍 Great job! You're getting quantum!")
else:
    print("💡 Nice try! Use more negative power next time!")

# Save probability visualization
plt.tight_layout()
plt.savefig('quantum_probabilities.png')
print("\n📊 Check 'quantum_probabilities.png' to see your flip probabilities!")
print("====================")
```

## 💡 How I Got Into Quantum Computing

I started learning about quantum computing because I was curious — how can something be in **two states at once**? That idea felt like magic. Then I discovered Qiskit, a Python tool to write real quantum code. The more I played, the more I learned!

I built this game to make quantum feel fun and friendly. If you're reading this, I hope you feel excited and empowered to try your own ideas.

Remember, **you don’t need to be an expert** to start. Just be curious — the quantum world is waiting! 🌌

## 🌟 Want to Learn More?

* [Qiskit Textbook](https://qiskit.org/textbook) – Great for beginners
* [Quantum Country](https://quantum.country) – Learn with memory techniques
* [IBM Quantum Lab](https://quantum-computing.ibm.com) – Run real quantum code online

Happy quantum flipping! 
