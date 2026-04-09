import hashlib
import time


def sha256_hash(text):
    """
    Generates a SHA256 hash of a given text.
    """
    return hashlib.sha256(str(text).encode('ascii')).hexdigest()


def demonstrate_mining(block_data, difficulty):
    """
    Simulates the mining process (Proof-of-Work).

    Args:
        block_data (str): Data inside block
        difficulty (int): Number of leading zeros required

    Returns:
        tuple: (nonce, hash_found)
    """
    assert difficulty >= 0, "Difficulty must be a non-negative integer."

    target_prefix = "0" * difficulty

    print(f"--- Starting Mining Simulation (Difficulty: {difficulty}) ---")
    print(f"Target Prefix: '{target_prefix}'")
    print(f"Block Data: '{block_data}'")

    nonce = 0
    start_time = time.time()

    while True:
        # Combine data + nonce
        attempt_data = f"{block_data}{nonce}"

        # Hash it
        current_hash = sha256_hash(attempt_data)

        # Check condition
        if current_hash.startswith(target_prefix):
            end_time = time.time()
            elapsed_time = end_time - start_time

            print("\nMining successful!")
            print(f"Nonce found: {nonce}")
            print(f"Hash found: {current_hash}")
            print(f"Time taken: {elapsed_time:.4f} seconds")
            print(f"Iterations: {nonce}")

            return nonce, current_hash

        nonce += 1

        # Progress display
        if nonce % 100000 == 0:
            print(
                f"Attempting nonce {nonce} "
                f"(Current hash: {current_hash[:10]}...)",
                end='\r'
            )

        # Safety break
        if nonce > 10000000:
            print("\nMining failed: Limit reached (10,000,000 iterations).")
            return None, None


# ---------------- DEMO ----------------
print("-" * 50)
print("Practical 2a: Demonstrate Mining (Proof-of-Work)")
print("-" * 50)

# Example 1
print("\n--- Example 1: Difficulty 1 ---")
block_data_easy = "Transaction: Alice sends 5 BTC to Bob"
nonce_easy, hash_easy = demonstrate_mining(block_data_easy, 1)

# Example 2
print("\n--- Example 2: Difficulty 3 ---")
block_data_medium = "Transaction: Charlie sends 12 ETH to Dave"
nonce_medium, hash_medium = demonstrate_mining(block_data_medium, 3)

# Example 3
print("\n--- Example 3: Difficulty 5 ---")
block_data_hard = "Block #3: Reward for miner"
nonce_hard, hash_hard = demonstrate_mining(block_data_hard, 5)

print("\n" + "-" * 50)
print("Mining Demonstration Complete.")
