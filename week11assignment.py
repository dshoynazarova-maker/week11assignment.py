def redeem_prize(players_db, prize_catalog, player_id, item_name, quantity):
        total_cost = 0
        if not player_id in players_db:
            raise KeyError('Player not found')
        if not item_name in prize_catalog:
            raise KeyError('Prize not available')
        if type(quantity) != int or quantity < 1:
            raise ValueError('Quantity must be positive integer')
        total_cost = quantity * prize_catalog[item_name]['cost']
        if quantity >= 3:
            if total_cost -100 >0:
                total_cost -= 100
        if players_db[player_id]['tickets'] < total_cost:
            raise ValueError('Not enough tickets')
        players_db[player_id]['tickets'] -= total_cost
        return total_cost
def process_redemptions(players_db, prize_catalog, queue):
   new_dict = {}
   tickets_spent = 0
   failed_redemptions = 0
   for player_id, item, qty in queue:
        try:
            cost = redeem_prize(players_db, prize_catalog, player_id, item, qty)
            tickets_spent += cost
        except Exception as e:
            print(f"Redemption Error for {player_id}: {e}")
            failed_redemptions += 1
   new_dict['ticket_spent'] = tickets_spent
   new_dict['failed_redemptions'] = failed_redemptions
   return new_dict
 
# Format: {Item: {"cost": int}}
prizes = {
    "Bear": {"cost": 500},
    "Candy": {"cost": 50}
}

# Format: {PlayerID: {"tickets": int}}
players = {
    "P1": {"tickets": 1000},
    "P2": {"tickets": 100}
}

queue = [
    ("P1", "Candy", 4),     # Valid. Cost: (200 - 100) = 100. Rem: 900.
    ("P2", "Bear", 1),      # Error: Cost 500 > 100.
    ("P9", "Toy", 1),       # Error: Player not found.
    ("P1", "PS5", 1),       # Error: Prize not available.
    ("P1", "Bear", 0)       # Error: Quantity must be positive integer.
]
print(process_redemptions(players, prizes, queue))
 
