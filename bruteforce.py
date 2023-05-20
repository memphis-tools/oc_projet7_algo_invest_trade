import csv
from argparse import ArgumentParser
from typing import List
from models.Action import Action


actions_list_unsorted: List[Action] = []
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


def set_a_bruteforce_wallet(actions_list_unsorted, client_wallet_funds, wallet_max=[]):
    """
    Paramètres:
        actions_list_unsorted: liste d'instances de classe Action, la liste de toutes les actions disponibles au catalogue
        client_wallet_funds: un nombre réel, fonds de départ du client
        wallet_max: liste d'instances de classe Action, retenues dans portefeuille client
    """
    if len(actions_list_unsorted) > 0:
        action = actions_list_unsorted[0]
        wallet1 = set_a_bruteforce_wallet(actions_list_unsorted[1:], client_wallet_funds, wallet_max)
        if client_wallet_funds - action.cost >= 0:
            wallet_max = wallet_max + [action]
            client_wallet_funds -= action.cost
            wallet2 = set_a_bruteforce_wallet(actions_list_unsorted[1:], client_wallet_funds, wallet_max)
            wallet1_profit = get_profit_from_client_wallet_funds(wallet1, actions_list_unsorted)
            wallet2_profit = get_profit_from_client_wallet_funds(wallet2, actions_list_unsorted)
            if wallet2_profit > wallet1_profit:
                return wallet2
        return wallet1
    else:
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


def get_profit_from_client_wallet_funds(wallet_max, actions_list_unsorted):
    """
    Paramètres:
        wallet_max: liste d'instances de classe Action retenues dans le portefeuille client
        actions_list_unsorted: liste d'instances de classe Action, la liste de toutes les actions disponibles au catalogue
    """
    profit = 0
    for action in wallet_max:
        profit += float(get_profit_from_action_name(action.name, actions_list_unsorted) * float(1))
    return profit


def get_amount_spend(wallet_max):
    """
    Paramètres:
        wallet_max: liste d'instances de classe Action retenues dans le portefeuille client
    """
    amount_spend = 0
    for action in wallet_max:
        amount_spend += float(1 * action.cost)
    return round(amount_spend, 2)


def get_residual_background(wallet_max, client_wallet_funds):
    """
    Paramètres:
        wallet_max: liste d'instances de classe Action retenues dans le portefeuille optimal
        client_wallet_funds: un nombre réel, fonds de départ du client
    """
    amount_spend = 0
    for action in wallet_max:
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


def debug_display_winnings(client_wallet_list, actions_list_unsorted, client_wallet_funds):
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
    print(f"MAX PROFIT: {get_profit_from_client_wallet_funds(client_wallet_list, actions_list_unsorted)}€")
    print("")


# on récupère une liste d'actions non triées par gains unitaires décroissants
actions_list_unsorted = get_an_actions_list_unsorted(parser.dataset_filename)

client_wallet_funds = int(parser.wallet_funds)
wallet_max = set_a_bruteforce_wallet(actions_list_unsorted, client_wallet_funds)
if parser.debug == "True":
    debug_display_winnings(wallet_max, actions_list_unsorted, client_wallet_funds)
