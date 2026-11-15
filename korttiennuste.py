
from collections import Counter
from decimal import Decimal, ROUND_HALF_UP

# DP World Tour Championship 2026
# Race to Dubai -pisteet sijoille 1–50.
POINTS = [
    2000, 1335, 752, 600, 509, 420, 359, 300,
    267, 240, 220, 206.4, 193.2, 183.6, 176.4,
    169.2, 162, 154.8, 147.6, 144, 140.4, 136.8,
    133.2, 129.6, 126, 122.4, 118.8, 115.2,
    111.6, 108, 104.4, 100.8, 98.4, 96, 93.6,
    91.2, 88.8, 86.4, 84, 81.6, 79.2, 76.8,
    74.4, 72, 69.6, 67.2, 64.8, 62.4, 60, 57.6
]

# PGA Tour -korttirankingin lähtöpisteet
# ennen finaalikilpailua 8.11.2026.
#
# HUOM: Lista on keskeneräinen.
# Puuttuvat pelaajat on täydennettävä
# ennen ennusteen julkaisemista.

BASE_POINTS = {
    "Eugenio Chacarra": 4243.79,
    "Patrick Reed": 3528.62,
    "Casey Jarvis": 2892.98,
    "Jayden Schaper": 2445.79,
    "Daniel Hillier": 2351.25,
    "Jacob Skov Olesen": 2111.49,
    "Bernd Wiesberger": 2022.59,
    "Andy Sullivan": 1977.87,
    "Oliver Lindell": 1787.14,
    "Joe Dean": 1758.76,
    "Angel Ayora": 1714.00,
    "Nacho Elvira": 1653.57,
    "Angel Hidalgo": 1593.72,
    "Hennie Du Plessis": 1491.01,
    "Dan Bradbury": 1464.06,
    "Francesco Laporta": 1438.62,
    "Shaun Norris": 1437.06,
    "Davis Bryant": 1405.05,
    "Thriston Lawrence": 1361.10,
    "Marcus Armitage": 1357.63
}


def calculate(players, base_points):
    """
    Laskee pelaajien ennustetut kokonaispisteet
    kilpailun tämänhetkisen sijoituksen perusteella.

    Tasasijoissa jaetaan kyseisten sijoitusten
    pisteiden keskiarvo.

    HUOM: Tuloksena on osittainen ranking, jos
    base_points ei sisällä kaikkia korttiehdokkaita.
    """

    if len(players) != 50:
        raise ValueError(
            f"Odotettiin 50 pelaajaa, saatiin {len(players)}"
        )

    positions = [
        int(str(p["pos"]).lstrip("T"))
        for p in players
    ]

    counts = Counter(positions)
    result = []

    for player, position in zip(players, positions):
        name = player["name"]
        count = counts[position]

        if position < 1 or position + count - 1 > 50:
            raise ValueError(
                f"Virheellinen sijoitus: {name}, {position}"
            )

        earned = sum(
            Decimal(str(POINTS[i - 1]))
            for i in range(position, position + count)
        ) / Decimal(count)

        if name not in base_points:
            continue

        total = (
            Decimal(str(base_points[name])) + earned
        )

        result.append({
            "name": name,
            "position": position,
            "event_points": float(
                earned.quantize(
                    Decimal("0.01"),
                    rounding=ROUND_HALF_UP
                )
            ),
            "total_points": float(
                total.quantize(
                    Decimal("0.01"),
                    rounding=ROUND_HALF_UP
                )
            )
        })

    result.sort(
        key=lambda p: (
            -p["total_points"],
            p["name"]
        )
    )

    for index, player in enumerate(result, 1):
        player["rank"] = index

    return result
    
def compare_with_lindell(forecast):
    oliver = next(
        p for p in forecast
        if p["name"] == "Oliver Lindell"
    )

    oliver_points = oliver["total_points"]

    comparisons = []

    for player in forecast:
        comparisons.append({
            "name": player["name"],
            "rank_partial": player["rank"],
            "total_points": player["total_points"],
            "difference_to_oliver": round(
                player["total_points"] - oliver_points,
                2
            ),
            "ahead_of_oliver": (
                player["total_points"] > oliver_points
            )
        })

    return {
        "oliver_points": oliver_points,
        "oliver_partial_rank": oliver["rank"],
        "comparisons": comparisons,
        "complete": False,
        "missing_candidates": [
            "Mikael Lindberg",
            "Calum Hill",
            "David Puig"
        ]
    }

