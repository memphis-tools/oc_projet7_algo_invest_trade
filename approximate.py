import csv
from argparse import ArgumentParser
from typing import List
from models.Action import Action


global client_wallet_list
global wallets_list
global actions_list_sorted_by_profit
actions_list_sorted_by_profit: List[Action] = []
wallets_list = []
wallet_max = []
wallet_max_profit = 0

args = ArgumentParser(description="A bruteforce example")
args.add_argument("-v", "--version", action="version", version="%(prog)s 1.0")
args.add_argument("-df", "--dataset_filename", dest="dataset_filename", default="False", help="the dataset filename located in static/files/", required=True)
args.add_argument("-wf", "--wallet_funds", dest="wallet_funds", default=500, help="default starting funds")
args.add_argument("-d", "--debug", dest="debug", default="False", help="set a True /False(default) debug mode")
parser = args.parse_args()


def read_csv_file(csv_filename):
    actions_list: List[Action] = []
    with open(csv_filename) as csv_file:
        line = csv.reader(csv_file, delimiter=',')
        next(line, None)
        for elem in line:
            if float(elem[1]) > 0 and elem[0] not in actions_list:
                action = Action(
                    name = elem[0],
                    cost = float(str(elem[1])),
                    rate = float(
                        str(elem[2]).replace("%", "")
                    ) / 100,
                    number = 0
                )
                actions_list.append(action)
    return actions_list


def is_action_bought(action_name, client_wallet_list):
    """
    Paramètres:
        action_name: une chaine de caractères, le nom d'une action
        client_wallet_list: liste d'instances de classe Action retenues dans le portefeuille client
    """
    for action in client_wallet_list:
        if action.name == action_name:
            return True
    return False


def set_an_optimized_wallet(
        actions_list_sorted_by_profit, client_wallet_funds, client_wallet_list=[]):
    """
    Paramètres:
        actions_list_sorted_by_profit: liste triée d'instances de classe Action
        client_wallet_funds: un nombre réel, fonds du client 
        client_wallet_list: liste d'instances de classe Action retenues dans le portefeuille client
    """
    if client_wallet_funds == int(parser.wallet_funds):
        client_wallet_list: List[Action] = []
    for action in actions_list_sorted_by_profit:
        # on introduit la notion d'action avec valeurs inférieures ou égale à 0
        if action.cost <= 0:
            continue
        if client_wallet_funds - action.cost >= 0:
            if is_action_bought(action.name, client_wallet_list):
                continue
            else:
                client_wallet_funds -= action.cost
                client_wallet_list.append(
                    Action(name=action.name, number=1, cost=action.cost, profit=action.profit, rate=action.rate))

            # au lieu de boucler n fois sur la 1ere entree de la liste, on fait un appel récursif
            return set_an_optimized_wallet(
                actions_list_sorted_by_profit, client_wallet_funds, client_wallet_list)
        else:
            continue

    return client_wallet_list


def get_profit_from_action_name(action_name, actions_list_sorted_by_profit):
    """
    Paramètres:
        action_name: une chaine de caractères, le nom d'une action telle que renseigné dans actions_list_sorted_by_profit
        actions_list_sorted_by_profit: liste d'instances de classe Action, la liste de toutes les actions disponibles au catalogue
    """
    for action in actions_list_sorted_by_profit:
        if action.name == action_name:
            return action.profit


def get_profit_from_client_wallet_funds(client_wallet_list, actions_list_sorted_by_profit):
    """
    Paramètres:
        client_wallet_list: liste d'instances de classe Action retenues dans le portefeuille optimal
    """
    profit = 0
    for action in client_wallet_list:
        profit += float(get_profit_from_action_name(action.name, actions_list_sorted_by_profit) * float(1))
    return profit


def get_amount_spend(client_wallet_list):
    """
    Paramètres:
        client_wallet_list: liste d'instances de classe Action retenues dans le portefeuille optimal
    """
    amount_spend = 0
    for action in client_wallet_list:
        amount_spend += float(action.number * action.cost)
    return round(amount_spend, 2)


def get_residual_background(client_wallet_list, client_wallet_funds):
    """
    Paramètres:
        client_wallet_list: liste d'instances de classe Action retenues dans le portefeuille optimal
        client_wallet_funds: un nombre réel, fonds de départ du client
    """
    amount_spend = 0
    for action in client_wallet_list:
        amount_spend += float(action.number) * float(action.cost)
    return round(client_wallet_funds - amount_spend, 2)


def get_an_actions_list_sorted_by_profit(dataset_filename):
    """
    Paramètres:
        dataset_filename: le nom d'un fichier de données format csv avec 3 en-têtes 'name,price,profit'
    """
    # on crée une liste d'actions triées par rapports profit/coût décroissants
    [actions_list_sorted_by_profit.append(action) for action in sorted(
        read_csv_file(f"static/files/{dataset_filename}"),
        key=lambda x: x.profit/x.cost,
        reverse=True)
    ]
    return actions_list_sorted_by_profit


def debug_display_the_actions_list_sorted_by_profit(actions_list_sorted_by_profit):
    """
    Paramètres:
        actions_list_sorted_by_profit: liste triée d'instances de classe Action
    """
    print(f"[DEBUG] actions_list_sorted_by_profit")
    for i in actions_list_sorted_by_profit:
        print(f"{i} init_cost: {i.cost}€ and profit: {round(i.profit, 2)}€")
    print(f"[DEBUG] LEN actions_list_sorted_by_profit: {len(actions_list_sorted_by_profit)}")
    print("")


def display_winnings(client_wallet_list, actions_list_sorted_by_profit):
    """
    Paramètres:
        client_wallet_list: liste d'instances de classe Action retenues dans le portefeuille optimal
    """
    print(f"BEST CLIENT WALLET: {client_wallet_list}")
    print("[BEST CLIENT WALLET]")
    for action in client_wallet_list:
        print(action)
    print(f"AMOUNT SPEND: {get_amount_spend(client_wallet_list)}€")
    print(f"RESIDUAL: {get_residual_background(client_wallet_list, client_wallet_funds)}€")
    print(f"MAX PROFIT: {get_profit_from_client_wallet_funds(client_wallet_list, actions_list_sorted_by_profit)}€")
    print("")


# on récupère une liste d'actions triées par gains unitaires décroissants
actions_list_sorted_by_profit = get_an_actions_list_sorted_by_profit(parser.dataset_filename)

for _ in range(len(actions_list_sorted_by_profit)):
    client_wallet_funds = int(parser.wallet_funds)
    client_wallet_list = set_an_optimized_wallet(actions_list_sorted_by_profit, client_wallet_funds)
    wallets_list.append(client_wallet_list)
    temp_profit = get_profit_from_client_wallet_funds(client_wallet_list, actions_list_sorted_by_profit)
    if temp_profit > wallet_max_profit:
        wallet_max_profit = temp_profit
        wallet_max = client_wallet_list
    

if parser.debug == "True":
    debug_display_the_actions_list_sorted_by_profit(actions_list_sorted_by_profit)
display_winnings(wallet_max, actions_list_sorted_by_profit)
