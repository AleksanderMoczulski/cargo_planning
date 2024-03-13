from pulp import *

PORT = [1, 2, 3, 4, 5, 6]
# 1= Anvers, 2= Dubai, 3= Hongkong, 4= LA, 5= NY, 6= Santos
TRAJET = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
PERIODE = [1, 2, 3, 4, 5, 6, 7, 8, 9]

REVENUE_TRAJET_PERIODE = {
    1: {1: 95, 2: 121, 3: 69, 4: 91, 5: 136, 6: 242, 7: 120, 8: 135, 9: 89},
    2: {1: 112, 2: 151, 3: 92, 4: 118, 5: 340, 6: 303, 7: 314, 8: 111, 9: 77},
    3: {1: 128, 2: 121, 3: 138, 4: 133, 5: 151, 6: 151, 7: 252, 8: 211, 9: 191},
    4: {1: 111, 2: 155, 3: 77, 4: 70, 5: 139, 6: 302, 7: 310, 8: 102, 9: 78},
    5: {1: 172, 2: 278, 3: 78, 4: 88, 5: 118, 6: 76, 7: 92, 8: 69, 9: 119},
    6: {1: 103, 2: 111, 3: 72, 4: 79, 5: 108, 6: 90, 7: 121, 8: 64, 9: 123},
    7: {1: 211, 2: 148, 3: 159, 4: 118, 5: 193, 6: 301, 7: 622, 8: 522, 9: 203},
    8: {1: 114, 2: 84, 3: 58, 4: 79, 5: 125, 6: 163, 7: 265, 8: 117, 9: 89},
    9: {1: 439, 2: 180, 3: 126, 4: 168, 5: 249, 6: 271, 7: 544, 8: 478, 9: 451},
    10: {1: 330, 2: 567, 3: 172, 4: 251, 5: 528, 6: 1159, 7: 902, 8: 314, 9: 274},
    11: {1: 348, 2: 312, 3: 244, 4: 260, 5: 416, 6: 945, 7: 439, 8: 232, 9: 758}
}
DEMANDE_TRAJET_PERIODE = {
    1: {1: 9367, 2: 8416, 3: 7461, 4: 10538, 5: 8249, 6: 13638, 7: 12584, 8: 10775, 9: 10482},
    2: {1: 4697, 2: 5389, 3: 3474, 4: 6909, 5: 8777, 6: 8680, 7: 7794, 8: 5048, 9: 2932},
    3: {1: 18253, 2: 8898, 3: 12827, 4: 7651, 5: 16429, 6: 20126, 7: 27975, 8: 21611, 9: 18727},
    4: {1: 8502, 2: 8585, 3: 5925, 4: 5809, 5: 10163, 6: 12384, 7: 13008, 8: 8259, 9: 5719},
    5: {1: 7559, 2: 7836, 3: 6227, 4: 5787, 5: 7152, 6: 6161, 7: 4754, 8: 5663, 9: 6283},
    6: {1: 9614, 2: 12705, 3: 6918, 4: 11233, 5: 13403, 6: 12289, 7: 22915, 8: 8273, 9: 13054},
    7: {1: 14860, 2: 16779, 3: 14960, 4: 10761, 5: 16162, 6: 20615, 7: 28680, 8: 21048, 9: 15502},
    8: {1: 7115, 2: 3740, 3: 4584, 4: 4578, 5: 7075, 6: 7819, 7: 9617, 8: 8035, 9: 5260},
    9: {1: 5398, 2: 4244, 3: 3010, 4: 3348, 5: 5412, 6: 5302, 7: 4825, 8: 4836, 9: 4485},
    10: {1: 38155, 2: 23848, 3: 26791, 4: 25866, 5: 38927, 6: 43773, 7: 42723, 8: 39363, 9: 22777},
    11: {1: 3382, 2: 3622, 3: 3291, 4: 4054, 5: 5544, 6: 4215, 7: 4476, 8: 3172, 9: 3514},
}
COUT_STOCK_PORT = {1: 2, 2: 6, 3: 2, 4: 3, 5: 4, 6: 5}
COUT_LEASING_PORT = {1: 75, 2: 90, 3: 85, 4: 80, 5: 80, 6: 50}
CAP_STOCK_PORT = {1: 7000, 2: 6000, 3: 8000, 4: 4000, 5: 8000, 6: 7000}
QUANTITE_MAI_PORT = {1: 30000, 2: 5000, 3: 50000, 4: 20000, 5: 10000, 6: 5000}
# ici on exprime le cout de chargement et déchargement pour chaque trajet
COUT_TRAJET = {1: 42, 2: 34, 3: 30, 4: 30, 5: 32, 6: 28, 7: 28, 8: 42, 9: 20, 10: 30, 11: 32}
CAP_TRAJET = {1: 15000, 2: 10000, 3: 35000, 4: 10000, 5: 10000, 6: 30000, 7: 20000, 8: 10000, 9: 5000, 10: 40000,
              11: 5000}

# Création du problème
Xpress_prob = LpProblem("ExpressFeeders_planning", LpMaximize)

# Création des variables
# i pour PERIODE
# j pour TRAJET
# k pour PORT
X_vars = LpVariable.dicts("Nombre de conteneurs remplis transportés par trajet par période",
                          [(i, j) for j in TRAJET for i in PERIODE], cat='Integer')
V_vars = LpVariable.dicts("Nombre de conteneurs vides transportés par trajet par période",
                          [(i, j) for j in TRAJET for i in PERIODE], lowBound=0, cat='Integer')
S_vars = LpVariable.dicts("Nombre de conteneurs stockés au port à la période", [(i, k) for k in PORT for i in PERIODE],
                          lowBound=0, cat='Integer')
L_vars = LpVariable.dicts("Nombre de conteneurs leasés pour port de départ", PORT, lowBound=0, cat='Integer')

# Création de la fonction objective
Xpress_prob += lpSum((REVENUE_TRAJET_PERIODE[j][i]) * X_vars[(i, j)] for j in TRAJET for i in PERIODE) - lpSum(
    COUT_STOCK_PORT[k] * S_vars[(i, k)] for k in PORT for i in PERIODE) - lpSum(
    COUT_TRAJET[j] * X_vars[(i, j)] for j in TRAJET for i in PERIODE) - lpSum(
    COUT_TRAJET[j] * V_vars[(i, j)] for j in TRAJET for i in PERIODE) - lpSum(
    COUT_LEASING_PORT[k] * L_vars[k] for k in PORT)

# Création des contraintes

for i in PERIODE:
    for j in TRAJET:
        Xpress_prob += X_vars[(i, j)] >= (0.6 * DEMANDE_TRAJET_PERIODE[j][i])
        Xpress_prob += X_vars[(i, j)] <= DEMANDE_TRAJET_PERIODE[j][i]
        if X_vars[(i, j)] == DEMANDE_TRAJET_PERIODE[j][i]:
            Xpress_prob += V_vars[(i, j)] >= 0
        else:
            Xpress_prob += V_vars[(i, j)] == 0

for i in PERIODE:
    for j in TRAJET:
        Xpress_prob += (X_vars[(i, j)] + V_vars[(i, j)]) <= CAP_TRAJET[j]

for i in PERIODE:
    for k in PORT:
        if i == 1:
            if k == 1:
                Xpress_prob += (X_vars[(1, 1)] + X_vars[(1, 2)] + X_vars[(1, 3)]) + (
                            V_vars[(1, 1)] + V_vars[(1, 2)] + V_vars[(1, 3)]) + S_vars[(1, 1)] == QUANTITE_MAI_PORT[1] + L_vars[1]
            if k == 2:
                Xpress_prob += (X_vars[(1, 4)] + V_vars[(1, 4)]) + S_vars[(1, 2)] == QUANTITE_MAI_PORT[2] + L_vars[2]
            if k == 3:
                Xpress_prob += ((X_vars[(1, 7)] + X_vars[(1, 9)] + X_vars[(1, 10)]) + (
                            V_vars[(1, 7)] + V_vars[(1, 9)] + V_vars[(1, 10)])) + S_vars[(1, 3)] == QUANTITE_MAI_PORT[3] + L_vars[3]
            if k == 4:
                Xpress_prob += (X_vars[(1, 6)] + V_vars[(1, 6)]) + S_vars[(1, 4)] == QUANTITE_MAI_PORT[4] + L_vars[4]
            if k == 5:
                Xpress_prob += (X_vars[(1, 8)] + X_vars[(1, 11)] + V_vars[(1, 8)] + V_vars[(1, 11)]) + S_vars[(1, 5)] == QUANTITE_MAI_PORT[5] + L_vars[5]
            if k == 6:
                Xpress_prob += (X_vars[(1, 5)] + V_vars[(1, 5)]) + S_vars[(1, 6)] == QUANTITE_MAI_PORT[6] + L_vars[6]
        else:
            if k == 1:
                Xpress_prob += ((X_vars[(i, 1)] + X_vars[(i, 2)] + X_vars[(i, 3)]) + (
                            V_vars[(i, 1)] + V_vars[(i, 2)] + V_vars[(i, 3)])) + S_vars[(i, 1)] == (S_vars[(i - 1, 1)] + (
                            X_vars[(i - 1, 4)] + X_vars[(i - 1, 8)] + X_vars[(i - 1, 10)]) + (V_vars[(i - 1, 4)] +
                                                                                              V_vars[(i - 1, 8)] +
                                                                                              V_vars[(i - 1, 10)]))
            if k == 2:
                Xpress_prob += (X_vars[(i, 4)] + V_vars[(i, 4)]) + S_vars[(i, 2)] == (
                            S_vars[(i - 1, 2)] + X_vars[(i - 1, 9)] + X_vars[(i - 1, 11)] + V_vars[(i - 1, 9)] + V_vars[
                        (i - 1, 11)])
            if k == 3:
                Xpress_prob += ((X_vars[(i, 7)] + X_vars[(i, 9)] + X_vars[(i, 10)]) + (
                            V_vars[(i, 7)] + V_vars[(i, 9)] + V_vars[(i, 10)])) + S_vars[(i, 3)] == S_vars[(i - 1, 3)] + (
                                           X_vars[(i - 1, 3)] + X_vars[(i - 1, 6)]) + (
                                           V_vars[(i - 1, 3)] + V_vars[(i - 1, 6)])
            if k == 4:
                Xpress_prob += (X_vars[(i, 6)] + V_vars[(i, 6)]) + S_vars[(i, 4)] == (
                            (S_vars[(i - 1, 4)] + (X_vars[(i - 1, 5)]) + X_vars[(i - 1, 7)]) + (
                                V_vars[(i - 1, 5)] + V_vars[(i - 1, 7)]))
            if k == 5:
                Xpress_prob += ((X_vars[(i, 8)] + X_vars[(i, 11)]) + (V_vars[(i, 8)] + V_vars[(i, 11)])) + S_vars[(i, 5)] == S_vars[
                    (i - 1, 5)] + (X_vars[(i - 1, 1)]) + (V_vars[(i - 1, 1)])
            if k == 6:
                Xpress_prob += (X_vars[(i, 5)] + V_vars[(i, 5)]) + S_vars[(i, 6)] == S_vars[(i - 1, 6)] + (X_vars[(i - 1, 2)]) + (V_vars[(i - 1, 2)])

for i in PERIODE:
    Xpress_prob += lpSum(X_vars[(i, j)] for j in TRAJET) + lpSum(V_vars[(i, j)] for j in TRAJET) + lpSum(
        S_vars[(i, k)] for k in PORT) == 120000 + lpSum(L_vars[k] for k in PORT)

# Xpress_prob += lpSum(L_vars[k] for k in PORT) + 120000 <= 230000
Xpress_prob += lpSum(L_vars[k] for k in PORT) <= 110000


Xpress_prob.solve()
print("Status:", LpStatus[Xpress_prob.status])

for v in Xpress_prob.variables():
    print(v.name, "=", v.varValue)

print("Valeur de l'objectif", value(Xpress_prob.objective))