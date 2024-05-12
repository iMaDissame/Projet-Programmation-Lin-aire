# from django.shortcuts import render
# from django.http import HttpResponse
# from .simplex_algorithm import simplex

# def simplex_view(request):
#     if request.method == 'POST':
#         try:
#             num_vars = int(request.POST['num_vars'])
#             num_constraints = int(request.POST['num_constraints'])
#             c = list(map(float, request.POST['c'].split(',')))
#             A = []
#             b = []

#             for i in range(1, num_constraints + 1):
#                 constraint_coeffs = request.POST[f'A{i}'].split(',')
#                 rhs_value = float(request.POST[f'b{i}'])
#                 A.append(list(map(float, constraint_coeffs)))
#                 b.append(rhs_value)

#             optimization_type = request.POST['optimization_type']

#             final_values, iterations, all_vars = simplex(c, A, b, optimization_type)

#             # Preprocess iterations for easier template rendering
#             for iteration in iterations:
#                 for i, row in enumerate(iteration['tableau']):
#                     iteration['tableau'][i] = list(map(lambda x: "{:.2f}".format(x), row))
#                 iteration['basic_and_values'] = [
#                     (all_vars[basic], iteration['tableau'][i + 1][-1])
#                     for i, basic in enumerate(iteration['basic_vars'])
#                 ]
#                 iteration['non_basic_vars'] = [
#                     (var, 0.0) for var in iteration['non_basic_vars']  # Assume 0 as initial value for non-basic vars
#                 ]
#                 objective_value = iterations[-1]['tableau'][0, -1] if optimization_type == 'max' else -iterations[-1]['tableau'][0, -1]

#             context = {
#                 'final_values': final_values,
#                 'iterations': iterations,
#                 'all_vars': all_vars,
#                 'objective_value': objective_value
#             }
#             return render(request, 'results.html', context)
#         except Exception as e:
#             return HttpResponse(f"Error processing the Simplex problem: {str(e)}")
#     else:
#         return render(request, 'input_form.html')


from django.shortcuts import render
from django.http import HttpResponse
from .simplex_algorithm import simplex

def simplex_view(request):
    # Vérifier si la requête est de type POST
    if request.method == 'POST':
        try:
            # Récupérer le nombre de variables et de contraintes depuis le formulaire
            num_vars = int(request.POST['num_vars'])
            num_constraints = int(request.POST['num_constraints'])
            
            # Convertir les coefficients de la fonction objectif en liste de floats
            c = list(map(float, request.POST['c'].split(',')))
            A = []
            b = []

            # Boucle pour récupérer les coefficients des contraintes et les valeurs du côté droit
            for i in range(1, num_constraints + 1):
                constraint_coeffs = request.POST[f'A{i}'].split(',')
                rhs_value = float(request.POST[f'b{i}'])
                A.append(list(map(float, constraint_coeffs)))
                b.append(rhs_value)

            # Récupérer le type d'optimisation (maximiser ou minimiser)
            optimization_type = request.POST['optimization_type']

            # Appel à la fonction simplex pour résoudre le problème
            final_values, iterations, all_vars = simplex(c, A, b, optimization_type)

            # Prétraiter chaque itération pour un affichage facilité
            for iteration in iterations:
                for i, row in enumerate(iteration['tableau']):
                    # Formater chaque cellule du tableau à deux décimales
                    iteration['tableau'][i] = list(map(lambda x: "{:.2f}".format(x), row))
                # Stocker les variables de base et leurs valeurs pour l'affichage
                iteration['basic_and_values'] = [
                    (all_vars[basic], iteration['tableau'][i + 1][-1])
                    for i, basic in enumerate(iteration['basic_vars'])
                ]
                # Gérer les variables hors base en assumant une valeur initiale de 0
                iteration['non_basic_vars'] = [
                    (var, 0.0) for var in iteration['non_basic_vars']
                ]
                # Calculer la valeur objectif finale
                objective_value = iterations[-1]['tableau'][0, -1] if optimization_type == 'max' else -iterations[-1]['tableau'][0, -1]

            # Créer le contexte pour le template
            context = {
                'final_values': final_values,
                'iterations': iterations,
                'all_vars': all_vars,
                'objective_value': objective_value
            }
            # Rendre la réponse en utilisant le template 'results.html'
            return render(request, 'results.html', context)
        except Exception as e:
            # Gérer les exceptions et renvoyer une réponse HTTP avec l'erreur
            return HttpResponse(f"Error processing the Simplex problem: {str(e)}")
    else:
        # Si la requête n'est pas POST, afficher le formulaire d'entrée
        return render(request, 'input_form.html')
