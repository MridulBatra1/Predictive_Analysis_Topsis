import pandas as pd
import numpy as np

def calculate_topsis(input_file, weights, impacts, output_file):

    if input_file.endswith('.csv'):
        data = pd.read_csv(input_file, encoding='latin1')
    elif input_file.endswith('.xlsx'):
        data = pd.read_excel(input_file)
    else:
        raise Exception("Unsupported file format. Please upload CSV or Excel file.")

    if data.shape[1] < 3:
        raise Exception("Input file must have at least 3 columns")

    data_numeric = data.iloc[:, 1:]

    decision_matrix = data_numeric.select_dtypes(include=[np.number])

    if decision_matrix.shape[1] == 0:
        raise Exception("No numeric columns found for TOPSIS calculation")

    weights = list(map(float, weights.split(',')))
    impacts = impacts.split(',')

    print("Detected numeric columns:", decision_matrix.columns)
    print("Number of criteria:", decision_matrix.shape[1])
    print("Weights:", weights)
    print("Impacts:", impacts)

    if len(weights) != decision_matrix.shape[1]:
        raise Exception(f"Weights mismatch: expected {decision_matrix.shape[1]} but got {len(weights)}")

    if len(impacts) != decision_matrix.shape[1]:
        raise Exception(f"Impacts mismatch: expected {decision_matrix.shape[1]} but got {len(impacts)}")

    for i in impacts:
        if i not in ['+', '-']:
            raise Exception("Impacts must be + or -")

    norm = decision_matrix / np.sqrt((decision_matrix**2).sum())

    weighted = norm * weights

    ideal_best = []
    ideal_worst = []

    for i in range(len(impacts)):
        if impacts[i] == '+':
            ideal_best.append(weighted.iloc[:, i].max())
            ideal_worst.append(weighted.iloc[:, i].min())
        else:
            ideal_best.append(weighted.iloc[:, i].min())
            ideal_worst.append(weighted.iloc[:, i].max())

    ideal_best = np.array(ideal_best)
    ideal_worst = np.array(ideal_worst)

    dist_best = np.sqrt(((weighted - ideal_best)**2).sum(axis=1))
    dist_worst = np.sqrt(((weighted - ideal_worst)**2).sum(axis=1))

    score = dist_worst / (dist_best + dist_worst)

    data['Topsis Score'] = score
    data['Rank'] = data['Topsis Score'].rank(ascending=False)

    data.to_csv(output_file, index=False)

    return data
