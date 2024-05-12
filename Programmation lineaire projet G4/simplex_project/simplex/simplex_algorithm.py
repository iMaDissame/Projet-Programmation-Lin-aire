# import numpy as np

# def initialize_simplex(c, A, b, optimization_type):
#     num_vars = len(c)
#     num_constraints = len(b)
#     tableau = np.zeros((num_constraints + 1, num_vars + num_constraints + 1))
#     tableau[0, :num_vars] = -np.array(c) if optimization_type == 'max' else np.array(c)
#     tableau[1:, :num_vars] = np.array(A)
#     tableau[1:, -1] = np.array(b)
#     tableau[1:, num_vars:num_vars + num_constraints] = np.eye(num_constraints)
#     return tableau, [f"x{i+1}" for i in range(num_vars)], [f"e{i+1}" for i in range(num_constraints)]

# def simplex(c, A, b, optimization_type='max'):
#     num_vars = len(c)
#     num_constraints = len(A)
#     tableau, variable_names, slack_names = initialize_simplex(c, A, b, optimization_type)
#     all_vars = variable_names + slack_names
#     basic_vars = list(range(num_vars, num_vars + num_constraints))

#     iterations = []
#     while any(tableau[0, :-1] < 0):
#         row, col = find_pivot(tableau)
#         pivot(tableau, row, col, basic_vars)
#         current_basic_vars = [all_vars[i] for i in basic_vars]
#         current_non_basic_vars = [var for var in all_vars if var not in current_basic_vars]
#         iterations.append({
#             'tableau': np.copy(tableau),
#             'basic_vars': basic_vars[:],
#             'non_basic_vars': current_non_basic_vars
#         })

#     final_values = extract_final_values(tableau, basic_vars, num_vars, variable_names, slack_names)
#     return final_values, iterations, all_vars


# def extract_final_values(tableau, basic_vars, num_vars, variable_names, slack_names):
#     final_values = {name: 0 for name in variable_names + slack_names}
#     for i, var_index in enumerate(basic_vars):
#         if var_index < num_vars:
#             final_values[variable_names[var_index]] = tableau[i + 1, -1]
#         else:
#             final_values[slack_names[var_index - num_vars]] = tableau[i + 1, -1]
#     return final_values

# def find_pivot(tableau):
#     col = np.argmin(tableau[0, :-1])
#     if all(tableau[1:, col] <= 0):
#         raise ValueError("Problem cannot be solved; it is unbounded.")
#     ratios = [tableau[i, -1] / tableau[i, col] if tableau[i, col] > 0 else float('inf') for i in range(1, tableau.shape[0])]
#     row = np.argmin(ratios) + 1
#     return row, col

# def pivot(tableau, row, col, basic_vars):
#     tableau[row, :] /= tableau[row, col]
#     for r in range(tableau.shape[0]):
#         if r != row:
#             tableau[r, :] -= tableau[r, col] * tableau[row, :]
#     basic_vars[row - 1] = col


import numpy as np

def initialize_simplex(c, A, b, optimization_type):
    num_vars = len(c)  # Nombre de variables de décision
    num_constraints = len(b)  # Nombre de contraintes
    # Création d'un tableau de simplex initial
    tableau = np.zeros((num_constraints + 1, num_vars + num_constraints + 1))
    # Initialisation de la première ligne du tableau pour les coefficients de la fonction objectif
    tableau[0, :num_vars] = -np.array(c) if optimization_type == 'max' else np.array(c)
    # Ajout des coefficients des contraintes dans le tableau
    tableau[1:, :num_vars] = np.array(A)
    # Ajout des valeurs du côté droit des contraintes
    tableau[1:, -1] = np.array(b)
    # Ajout de l'identité pour les variables d'écart
    tableau[1:, num_vars:num_vars + num_constraints] = np.eye(num_constraints)
    # Retourne le tableau initialisé, les noms des variables de décision, et les noms des variables d'écart
    return tableau, [f"x{i+1}" for i in range(num_vars)], [f"e{i+1}" for i in range(num_constraints)]

def simplex(c, A, b, optimization_type='max'):
    num_vars = len(c)  # Nombre de variables
    num_constraints = len(A)  # Nombre de contraintes
    # Initialisation du tableau simplex
    tableau, variable_names, slack_names = initialize_simplex(c, A, b, optimization_type)
    all_vars = variable_names + slack_names  # Toutes les variables, y compris d'écart
    basic_vars = list(range(num_vars, num_vars + num_constraints))  # Indices des variables de base initiales

    iterations = []  # Liste pour stocker l'état du tableau à chaque itération
    while any(tableau[0, :-1] < 0):  # Tant qu'il existe un coût réduit négatif
        row, col = find_pivot(tableau)  # Trouver le pivot
        pivot(tableau, row, col, basic_vars)  # Pivoter autour de ce pivot
        current_basic_vars = [all_vars[i] for i in basic_vars]  # Variables de base actuelles
        current_non_basic_vars = [var for var in all_vars if var not in current_basic_vars]  # Variables hors base actuelles
        iterations.append({
            'tableau': np.copy(tableau),  # Copie du tableau
            'basic_vars': basic_vars[:],  # Variables de base
            'non_basic_vars': current_non_basic_vars  # Variables hors base
        })

    final_values = extract_final_values(tableau, basic_vars, num_vars, variable_names, slack_names)
    return final_values, iterations, all_vars  # Retourne les valeurs finales, les itérations, et toutes les variables

def extract_final_values(tableau, basic_vars, num_vars, variable_names, slack_names):
    final_values = {name: 0 for name in variable_names + slack_names}  # Initialisation des valeurs finales à 0
    for i, var_index in enumerate(basic_vars):
        if var_index < num_vars:
            final_values[variable_names[var_index]] = tableau[i + 1, -1]  # Valeur finale pour les variables de décision
        else:
            final_values[slack_names[var_index - num_vars]] = tableau[i + 1, -1]  # Valeur finale pour les variables d'écart
    return final_values  # Retour des valeurs finales des variables

def find_pivot(tableau):
    col = np.argmin(tableau[0, :-1])  # Sélection de la colonne du pivot (coût réduit le plus négatif)
    if all(tableau[1:, col] <= 0):
        raise ValueError("Problem cannot be solved; it is unbounded.")  # Problème non borné
    ratios = [tableau[i, -1] / tableau[i, col] if tableau[i, col] > 0 else float('inf') for i in range(1, tableau.shape[0])]
    row = np.argmin(ratios) + 1  # Sélection de la ligne du pivot (rapport minimum)
    return row, col  # Retourne les indices de ligne et de colonne du pivot

def pivot(tableau, row, col, basic_vars):
    tableau[row, :] /= tableau[row, col]  # Division de la ligne du pivot par l'élément pivot
    for r in range(tableau.shape[0]):  # Mise à jour des autres lignes
        if r != row:
            tableau[r, :] -= tableau[r, col] * tableau[row, :]  # Élimination de la colonne du pivot
    basic_vars[row - 1] = col  # Mise à jour des variables de base
