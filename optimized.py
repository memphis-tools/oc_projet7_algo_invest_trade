import csv
from argparse import ArgumentParser
from typing import List
from models.Action import ActionOptimized


actions_list_unsorted: List[ActionOptimized] = []
wallet_max = []
wallet_max_profit = 0.0

args = ArgumentParser(description="A bruteforce example")
args.add_argument("-v", "--version", action="version", version="%(prog)s 1.0")
args.add_argument(
    "-df", 
    "--dataset_filename", 
    dest="dataset_filename", default="False", help="the dataset filename located in static/files/", required=True)
args.add_argument("-wf", "--wallet_funds", dest="wallet_funds", default=500, help="default starting funds")
args.add_argument("-d", "--debug", dest="debug", default="True", help="set a True /False(default) debug mode")
parser = args.parse_args()


def read_csv_file(csv_filename):
    actions_list: List[ActionOptimized] = []
    with open(csv_filename) as csv_file:
        line = csv.reader(csv_file, delimiter=',')
        next(line, None)
        for elem in line:
            if float(elem[1]) > 0 and elem[0] not in actions_list:
                action = ActionOptimized(
                    name = elem[0],
                    cost = elem[1],
                    rate = float(elem[2])*100,
                    number = 0
                )
                actions_list.append(action)
    return actions_list


def print_matrice(mat):
    for m in mat:
        print(m)
    print("")


def set_an_optimized_wallet(client_wallet_funds, actions_list_unsorted):
    matrice = [[0.0 for x in range(client_wallet_funds + 1)] for x in range(len(actions_list_unsorted) + 1)]
    
    for i in range(1, len(actions_list_unsorted) + 1):
        for w in range(1, client_wallet_funds + 1):
            if actions_list_unsorted[i-1].cost <= w:
                matrice[i][w] = max(
                    actions_list_unsorted[i-1].profit + matrice[i-1][w-actions_list_unsorted[i-1].cost], matrice[i-1][w])
            else:
                matrice[i][w] = matrice[i-1][w]

    # Retrouver les éléments en fonction de la somme
    w = client_wallet_funds
    n = len(actions_list_unsorted)
    wallet_max = []

    while w >= 0 and n >= 0:
        e = actions_list_unsorted[n-1]
        if matrice[n][w] == matrice[n-1][w-e.cost] + e.profit:
            wallet_max.append(e)
            w -= e.cost
        n -= 1

    return wallet_max

def get_profit_from_action_name(action_name, actions_list_unsorted):
    """
    Paramètres:
        action_name: une chaine de caractères, le nom d'une action telle que renseigné dans dump_list
        actions_list_unsorted: liste d'instances de classe Action, la liste de toutes les actions disponibles au catalogue
    """
    for action in actions_list_unsorted:
        if action.name == action_name:
            return action.profit
    return 0


def get_profit_from_client_wallet_funds(client_wallet_list, actions_list_unsorted):
    """
    Paramètres:
        client_wallet_list: liste d'instances de classe Action retenues dans le portefeuille client
        actions_list_unsorted: liste d'instances de classe Action, la liste de toutes les actions disponibles au catalogue
    """
    profit = 0
    for action in client_wallet_list:
        profit += float(get_profit_from_action_name(action.name, actions_list_unsorted) * 1)
    return profit/100000000


def get_action_cost(action_name, actions_list_unsorted):
    for action in actions_list_unsorted:
        if str(action_name) == action.name:
            return action.cost
    return None


def get_amount_spend(client_wallet_list):
    """
    Paramètres:
        client_wallet_list: liste d'instances de classe Action retenues dans le portefeuille client
    """
    amount_spend = 0
    for action in client_wallet_list:
        amount_spend += float(1 * get_action_cost(action, actions_list_unsorted))
    return round(amount_spend, 2)


def get_residual_background(client_wallet_list, client_wallet_funds):
    """
    Paramètres:
        client_wallet_list: liste d'instances de classe Action retenues dans le portefeuille optimal
        client_wallet_funds: un nombre réel, fonds de départ du client
    """
    amount_spend = 0
    for action in client_wallet_list:
        amount_spend += float(1) * float(action.cost)
    return round(client_wallet_funds - amount_spend, 2)


def get_an_actions_list_unsorted(dataset_filename):
    """
    Paramètres:
        dataset_filename: le nom d'un fichier de données format csv avec 3 en-têtes 'name,price,profit'
    """
    # on crée une liste d'actions non triées
    [actions_list_unsorted.append(action) for action in read_csv_file(f"static/files/{dataset_filename}")]

    return actions_list_unsorted


def debug_display_the_actions_list_unsorted(actions_list_unsorted):
    """
    Paramètres:
        actions_list_sorted_by_profit: liste non triée d'instances de classe Action
    """
    print(f"[DEBUG] actions_list_unsorted")
    for i in actions_list_unsorted:
        print(f"{i} init_cost: {i.cost}€ and profit: {round(i.profit, 2)}€")
    print(f"[DEBUG] LEN actions_list_unsorted: {len(actions_list_unsorted)}")
    print("")


def debug_display_winnings(client_wallet_list, actions_list_unsorted, client_wallet_funds):
    """
    Paramètres:
        client_wallet_list: liste d'instances de classe Action retenues dans le portefeuille optimal
    """
    print(f"BEST CLIENT WALLET: {client_wallet_list}")
    for wallet in client_wallet_list:
        print(wallet)
    print(f"AMOUNT SPEND: {get_amount_spend(client_wallet_list)/100}€")
    print(f"RESIDUAL: {get_residual_background(client_wallet_list, client_wallet_funds)/100}€")
    print(f"MAX PROFIT: {get_profit_from_client_wallet_funds(client_wallet_list, actions_list_unsorted)}€")
    print("")


# on récupère une liste d'actions non triées par gains unitaires décroissants
actions_list_unsorted = get_an_actions_list_unsorted(parser.dataset_filename)

client_wallet_funds = int(parser.wallet_funds)
wallet_max =  set_an_optimized_wallet(client_wallet_funds*100, actions_list_unsorted)
debug_display_winnings(wallet_max, actions_list_unsorted, client_wallet_funds*100)