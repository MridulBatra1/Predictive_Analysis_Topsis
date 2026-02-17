import sys
from .core import calculate_topsis

def main():
    if len(sys.argv) != 5:
        print("Usage: python -m topsis.cli <input.csv> <weights> <impacts> <output.csv>")
        sys.exit()

    input_file = sys.argv[1]
    weights = sys.argv[2]
    impacts = sys.argv[3]
    output_file = sys.argv[4]

    try:
        calculate_topsis(input_file, weights, impacts, output_file)
        print("Result saved to", output_file)
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
