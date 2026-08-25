import pickle
import sys
import os


def load_q_table(filename="models/q_table.pkl"):
    """loads q-table from a pickle file"""
    if not isinstance(filename, str):
        print("Filename should be a string")
        return None
    if not os.path.isfile(filename):
        print("File not found.")
        return None
    if not os.stat(filename).st_size:
        print("File is empty.")
        return None
    with open(filename, "rb") as f:
        try:
            data = pickle.load(f)
        except (
            pickle.UnpicklingError,
            EOFError,
            AttributeError,
            ImportError,
            IndexError
        ) as e:
            print(f"Error parsing pickle file: {e}.")
            sys.exit(1)

    q_table = data['q_table']
    print('loaded', filename)
    return q_table


def save_q_table(q_table, filename="models/q_table.pkl"):
    """saves the q-table into a pickle file"""
    # store the datasets to be stowed in pickle file
    data = {
        'q_table': q_table,
    }
    with open(filename, "wb") as f:
        pickle.dump(data, f)
    print("q-table saved to", filename)
