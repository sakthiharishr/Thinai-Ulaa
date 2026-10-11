"""Cost rules and transportation pricing configuration for Tamil Nadu tourism."""

# Approximate planning estimates for Tamil Nadu travel budgeting.
# All rates are configurable for future adjustments.
COST_RULES = {
    # Transportation base rates per kilometre:
    # - budget: Public bus / transit rate per passenger-km (₹2.5/km)
    # - standard: WagonR / 5-seater cab default rate (₹12/km, range: ₹10–₹15/km)
    # - premium: Innova / premium SUV default rate (₹18/km, range: ₹16–₹22/km)
    "transport": {
        "budget": 2.5,
        "standard": 12.0,
        "premium": 18.0,
    },
    # Detailed transportation configuration per tier
    "transport_config": {
        "budget": {
            "mode": "public_transit",
            "vehicle": "Public Bus / Transit",
            "capacity": 40,
            "min_rate_per_km": 2.0,
            "max_rate_per_km": 3.0,
            "default_rate_per_km": 2.5,
            "daily_min_km": 0.0,
            "driver_allowance_per_day": 0.0,
            "waiting_charges_per_day": 0.0,
            "tolls_parking_per_day": 0.0,
            "min_fare_per_person": 30.0,
            "description": "Public bus / train transit (minimal economical option)",
        },
        "standard": {
            "mode": "cab",
            "vehicle": "WagonR / 5-Seater Cab",
            "capacity": 4,
            "min_rate_per_km": 10.0,
            "max_rate_per_km": 15.0,
            "default_rate_per_km": 12.0,
            "daily_min_km": 250.0,
            "driver_allowance_per_day": 400.0,  # Configurable range: ₹300–₹600
            "waiting_charges_per_day": 200.0,
            "tolls_parking_per_day": 200.0,
            "fixed_package": {
                "name": "Local/Daily Rental Package",
                "base_per_day": 2200.0,
                "included_km_per_day": 100.0,
                "extra_km_rate": 12.0,
                "driver_included": True,
                "waiting_included": True,
                "tolls_parking_included": False,
            },
            "description": "WagonR or similar small 5-seater cab",
        },
        "premium": {
            "mode": "cab",
            "vehicle": "Innova / Premium SUV",
            "capacity": 6,
            "min_rate_per_km": 16.0,
            "max_rate_per_km": 22.0,
            "default_rate_per_km": 18.0,
            "daily_min_km": 250.0,
            "driver_allowance_per_day": 500.0,  # Configurable range: ₹300–₹600
            "waiting_charges_per_day": 300.0,
            "tolls_parking_per_day": 350.0,
            "fixed_package": {
                "name": "Local/Daily Rental Package",
                "base_per_day": 4000.0,
                "included_km_per_day": 100.0,
                "extra_km_rate": 18.0,
                "driver_included": True,
                "waiting_included": True,
                "tolls_parking_included": False,
            },
            "description": "Innova or similar premium SUV (6-seater)",
        },
    },
    # Backward compatible transport_package dictionary
    "transport_package": {
        "budget": {
            "vehicle": "Public Bus / Transit",
            "capacity": 40,
            "base_per_day": 0.0,
            "included_km_per_day": 0.0,
            "extra_km_rate": 2.5,
            "driver_allowance_per_day": 0.0,
        },
        "standard": {
            "vehicle": "WagonR / 5-Seater Cab",
            "capacity": 4,
            "base_per_day": 2200.0,
            "included_km_per_day": 100.0,
            "extra_km_rate": 12.0,
            "driver_allowance_per_day": 400.0,
        },
        "premium": {
            "vehicle": "Innova / Premium SUV",
            "capacity": 6,
            "base_per_day": 4000.0,
            "included_km_per_day": 100.0,
            "extra_km_rate": 18.0,
            "driver_allowance_per_day": 500.0,
        },
    },
    "food_per_person_per_day": {
        "budget": 300.0,
        "standard": 500.0,
        "premium": 900.0,
    },
    "accommodation_per_person_per_night": {
        "budget": 700.0,
        "standard": 1200.0,
        "premium": 2500.0,
    },
    "miscellaneous_per_day": {
        "budget": 100.0,
        "standard": 200.0,
        "premium": 400.0,
    },
}

BUDGET_LEVELS = [
    "budget",
    "standard",
    "premium",
]


def get_cost_rule(category, budget_level="standard"):
    if category not in COST_RULES:
        return 0.0

    if budget_level not in BUDGET_LEVELS:
        budget_level = "standard"

    return COST_RULES[category].get(
        budget_level,
        0.0,
    )


def get_budget_rules(budget_level="standard"):
    if budget_level not in BUDGET_LEVELS:
        budget_level = "standard"

    return {
        category: values.get(
            budget_level,
            0.0,
        )
        for category, values in COST_RULES.items()
    }


def get_transport_config(budget_level="standard"):
    if budget_level not in BUDGET_LEVELS:
        budget_level = "standard"
    return COST_RULES["transport_config"].get(
        budget_level,
        COST_RULES["transport_config"]["standard"],
    )


def calculate_estimated_daily_cost(
    budget_level="standard",
):
    rules = get_budget_rules(budget_level)

    return round(
        rules["food_per_person_per_day"]
        + rules["accommodation_per_person_per_night"]
        + rules["miscellaneous_per_day"],
        2,
    )