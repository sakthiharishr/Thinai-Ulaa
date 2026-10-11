DEFAULT_COSTS = {
    "transport_per_km": 12.0,
    "food_per_person_per_day": 500.0,
    "accommodation_per_person_per_day": 1000.0,
    "entry_fee_buffer": 0.0,
    "miscellaneous_per_day": 200.0,
}


def calculate_cab_transport_cost(
    distance_km,
    days=1,
    budget_level="standard",
    travelers=1,
    daily_distances=None,
    pricing_method="auto",
    rate_per_km=None,
    daily_min_km=None,
    driver_allowance_per_day=None,
    waiting_charges_per_day=None,
    tolls_parking_per_day=None,
):
    """Estimate tourist transportation budget.

    - Budget: Public bus / transit calculation per passenger without cab/driver charges.
    - Standard: WagonR or similar small 5-seater cab (approx. ₹10–₹15/km).
    - Premium: Innova or similar premium SUV (approx. ₹16–₹22/km).

    Supports:
    - Daily minimum billable distance evaluated per day.
    - Additional expenses: driver allowance (₹300–₹600/day), waiting charges, tolls/parking.
    - Comparison with fixed daily rental packages without double-counting.
    - Shared cab vehicle-level scaling based on vehicle capacity.
    - Minimum and maximum planning estimate ranges.
    """
    try:
        distance_km = max(0.0, float(distance_km))
    except (TypeError, ValueError):
        distance_km = 0.0

    try:
        days = max(1, int(days))
    except (TypeError, ValueError):
        days = 1

    try:
        travelers = max(1, int(travelers))
    except (TypeError, ValueError):
        travelers = 1

    from .cost_rules import BUDGET_LEVELS, get_transport_config

    if budget_level not in BUDGET_LEVELS:
        budget_level = "standard"

    cfg = get_transport_config(budget_level)
    mode = cfg.get("mode", "cab")

    # 1. Budget: Public transit / bus mode
    if budget_level == "budget" or mode == "public_transit":
        def_rate = float(rate_per_km if rate_per_km is not None else cfg.get("default_rate_per_km", 2.5))
        min_rate = float(cfg.get("min_rate_per_km", 2.0))
        max_rate = float(cfg.get("max_rate_per_km", 3.0))
        min_fare = float(cfg.get("min_fare_per_person", 30.0))

        cost = max(min_fare * travelers, distance_km * def_rate * travelers)
        cost_min = max(min_fare * travelers, distance_km * min_rate * travelers)
        cost_max = max(min_fare * travelers, distance_km * max_rate * travelers)

        daily_dist = [round(distance_km / days, 2)] * days
        return {
            "cost": round(cost, 2),
            "cost_min": round(cost_min, 2),
            "cost_max": round(cost_max, 2),
            "mode": "public_transit",
            "vehicle": cfg.get("vehicle", "Public Bus / Transit"),
            "vehicles": 1,
            "actual_km": round(distance_km, 2),
            "billable_km": round(distance_km, 2),
            "daily_actual_km": daily_dist,
            "daily_billable_km": daily_dist,
            "rate_per_km": round(def_rate, 2),
            "rate_range": (round(min_rate, 2), round(max_rate, 2)),
            "distance_charge": round(cost, 2),
            "driver_allowance": 0.0,
            "waiting_charges": 0.0,
            "tolls_parking": 0.0,
            "base_package": 0.0,
            "package_cost": None,
            "distance_based_cost": round(cost, 2),
            "pricing_model_used": "public_transit",
            "is_minimum_distance_applied": False,
            "daily_min_km": 0.0,
            # Backward compatibility keys
            "included_km": 0.0,
            "extra_km": round(distance_km, 2),
            "extra_km_charge": round(cost, 2),
        }

    # 2. Standard & Premium: Cab mode
    capacity = int(cfg.get("capacity", 4))
    vehicles = max(1, (travelers + capacity - 1) // capacity)

    def_rate = float(rate_per_km if rate_per_km is not None else cfg.get("default_rate_per_km", 12.0))
    min_rate = float(cfg.get("min_rate_per_km", 10.0))
    max_rate = float(cfg.get("max_rate_per_km", 15.0))
    min_daily_km = float(daily_min_km if daily_min_km is not None else cfg.get("daily_min_km", 250.0))
    driver_rate = float(
        driver_allowance_per_day if driver_allowance_per_day is not None else cfg.get("driver_allowance_per_day", 400.0)
    )
    waiting_rate = float(
        waiting_charges_per_day if waiting_charges_per_day is not None else cfg.get("waiting_charges_per_day", 200.0)
    )
    tolls_rate = float(
        tolls_parking_per_day if tolls_parking_per_day is not None else cfg.get("tolls_parking_per_day", 200.0)
    )

    # Clean daily distances or partition total distance across trip days
    clean_daily = []
    if daily_distances and isinstance(daily_distances, (list, tuple)):
        for d in daily_distances:
            try:
                clean_daily.append(max(0.0, float(d)))
            except (TypeError, ValueError):
                clean_daily.append(0.0)
        if len(clean_daily) < days:
            accounted = sum(clean_daily)
            rem_dist = max(0.0, distance_km - accounted)
            rem_days = days - len(clean_daily)
            clean_daily.extend([rem_dist / rem_days] * rem_days)
        elif len(clean_daily) > days:
            clean_daily = clean_daily[:days]
    else:
        clean_daily = [distance_km / days] * days

    # Calculate daily billable distance separately for each rental day
    daily_billable = [max(d, min_daily_km) for d in clean_daily]
    total_billable_km = sum(daily_billable)
    total_actual_km = sum(clean_daily)
    is_min_applied = any(b > a for a, b in zip(clean_daily, daily_billable))

    # Distance-based calculation (per vehicle)
    dist_charge = total_billable_km * def_rate
    dist_charge_min = total_billable_km * min_rate
    dist_charge_max = total_billable_km * max_rate
    driver_charge = driver_rate * days
    waiting_charge = waiting_rate * days
    tolls_charge = tolls_rate * days

    dist_total_per_v = dist_charge + driver_charge + waiting_charge + tolls_charge
    dist_min_per_v = dist_charge_min + driver_charge + waiting_charge + tolls_charge
    dist_max_per_v = dist_charge_max + driver_charge + waiting_charge + tolls_charge

    # Fixed rental package calculation (per vehicle)
    pkg = cfg.get("fixed_package")
    if pkg:
        pkg_base = float(pkg.get("base_per_day", 2200.0)) * days
        pkg_inc_km = float(pkg.get("included_km_per_day", 100.0)) * days
        pkg_extra_km = max(0.0, total_actual_km - pkg_inc_km)
        pkg_extra_rate = float(pkg.get("extra_km_rate", def_rate))
        pkg_extra_charge = pkg_extra_km * pkg_extra_rate
        pkg_extra_min = pkg_extra_km * min_rate
        pkg_extra_max = pkg_extra_km * max_rate
        pkg_driver = 0.0 if pkg.get("driver_included", True) else driver_charge
        pkg_waiting = 0.0 if pkg.get("waiting_included", True) else waiting_charge
        pkg_tolls = 0.0 if pkg.get("tolls_parking_included", False) else tolls_charge

        pkg_total_per_v = pkg_base + pkg_extra_charge + pkg_driver + pkg_waiting + pkg_tolls
        pkg_min_per_v = pkg_base + pkg_extra_min + pkg_driver + pkg_waiting + pkg_tolls
        pkg_max_per_v = pkg_base + pkg_extra_max + pkg_driver + pkg_waiting + pkg_tolls
    else:
        pkg_total_per_v = None
        pkg_min_per_v = None
        pkg_max_per_v = None
        pkg_inc_km = 0.0
        pkg_extra_km = total_actual_km
        pkg_extra_charge = 0.0
        pkg_base = 0.0
        pkg_driver = driver_charge
        pkg_waiting = waiting_charge
        pkg_tolls = tolls_charge

    # Pricing method selection
    if pricing_method == "package" and pkg_total_per_v is not None:
        model_used = "fixed_package"
        chosen_cost_per_v = pkg_total_per_v
        chosen_min_per_v = pkg_min_per_v
        chosen_max_per_v = pkg_max_per_v
    elif pricing_method == "distance":
        model_used = "distance_based"
        chosen_cost_per_v = dist_total_per_v
        chosen_min_per_v = dist_min_per_v
        chosen_max_per_v = dist_max_per_v
    else:  # "auto"
        if pkg_total_per_v is not None and pkg_total_per_v < dist_total_per_v:
            model_used = "fixed_package"
            chosen_cost_per_v = pkg_total_per_v
            chosen_min_per_v = pkg_min_per_v
            chosen_max_per_v = pkg_max_per_v
        else:
            model_used = "distance_based"
            chosen_cost_per_v = dist_total_per_v
            chosen_min_per_v = dist_min_per_v
            chosen_max_per_v = dist_max_per_v

    # Scale costs strictly by vehicle count (NOT by number of travelers)
    cost = chosen_cost_per_v * vehicles
    cost_min = chosen_min_per_v * vehicles
    cost_max = chosen_max_per_v * vehicles

    if model_used == "fixed_package":
        base_pkg = pkg_base * vehicles
        extra_charge = pkg_extra_charge * vehicles
        driver_total = pkg_driver * vehicles
        waiting_total = pkg_waiting * vehicles
        tolls_total = pkg_tolls * vehicles
        distance_charge_disp = extra_charge
        included_km_disp = pkg_inc_km
        extra_km_disp = pkg_extra_km
    else:
        base_pkg = 0.0
        extra_charge = 0.0
        driver_total = driver_charge * vehicles
        waiting_total = waiting_charge * vehicles
        tolls_total = tolls_charge * vehicles
        distance_charge_disp = dist_charge * vehicles
        included_km_disp = 0.0
        extra_km_disp = total_billable_km

    return {
        "cost": round(cost, 2),
        "cost_min": round(cost_min, 2),
        "cost_max": round(cost_max, 2),
        "mode": "cab",
        "vehicle": cfg.get("vehicle", "Cab"),
        "vehicles": vehicles,
        "actual_km": round(total_actual_km, 2),
        "billable_km": round(total_billable_km, 2),
        "daily_actual_km": [round(d, 2) for d in clean_daily],
        "daily_billable_km": [round(d, 2) for d in daily_billable],
        "rate_per_km": round(def_rate, 2),
        "rate_range": (round(min_rate, 2), round(max_rate, 2)),
        "distance_charge": round(distance_charge_disp, 2),
        "driver_allowance": round(driver_total, 2),
        "waiting_charges": round(waiting_total, 2),
        "tolls_parking": round(tolls_total, 2),
        "base_package": round(base_pkg, 2),
        "package_cost": round(pkg_total_per_v * vehicles, 2) if pkg_total_per_v is not None else None,
        "distance_based_cost": round(dist_total_per_v * vehicles, 2),
        "pricing_model_used": model_used,
        "is_minimum_distance_applied": is_min_applied,
        "daily_min_km": min_daily_km,
        # Backward compatibility
        "included_km": round(included_km_disp, 2),
        "extra_km": round(extra_km_disp, 2),
        "extra_km_charge": round(extra_charge, 2),
    }


def calculate_transport_cost(
    distance_km,
    transport_cost_per_km=None,
):
    try:
        distance_km = float(distance_km)
    except (TypeError, ValueError):
        return 0.0

    if transport_cost_per_km is None:
        transport_cost_per_km = DEFAULT_COSTS[
            "transport_per_km"
        ]

    try:
        transport_cost_per_km = float(
            transport_cost_per_km
        )
    except (TypeError, ValueError):
        return 0.0

    return round(
        max(0, distance_km)
        * max(0, transport_cost_per_km),
        2,
    )


def calculate_food_cost(
    travelers,
    days,
    cost_per_person_per_day=None,
):
    try:
        travelers = max(1, int(travelers))
        days = max(1, int(days))
    except (TypeError, ValueError):
        return 0.0

    if cost_per_person_per_day is None:
        cost_per_person_per_day = DEFAULT_COSTS[
            "food_per_person_per_day"
        ]

    try:
        cost_per_person_per_day = float(
            cost_per_person_per_day
        )
    except (TypeError, ValueError):
        return 0.0

    return round(
        travelers
        * days
        * max(0, cost_per_person_per_day),
        2,
    )


def calculate_accommodation_cost(
    travelers,
    nights,
    cost_per_person_per_night=None,
):
    try:
        travelers = max(1, int(travelers))
        nights = max(0, int(nights))
    except (TypeError, ValueError):
        return 0.0

    if cost_per_person_per_night is None:
        cost_per_person_per_night = DEFAULT_COSTS[
            "accommodation_per_person_per_day"
        ]

    try:
        cost_per_person_per_night = float(
            cost_per_person_per_night
        )
    except (TypeError, ValueError):
        return 0.0

    return round(
        travelers
        * nights
        * max(0, cost_per_person_per_night),
        2,
    )


def calculate_entry_fees(places, travelers=1):
    if not places:
        return 0.0

    try:
        travelers = max(1, int(travelers))
    except (TypeError, ValueError):
        travelers = 1

    total = 0.0

    for place in places:
        try:
            fee = float(
                place.get("entry_fee", 0)
            )
        except (TypeError, ValueError):
            fee = 0.0

        total += max(0, fee) * travelers

    return round(total, 2)


def calculate_miscellaneous_cost(
    days,
    cost_per_day=None,
):
    try:
        days = max(1, int(days))
    except (TypeError, ValueError):
        return 0.0

    if cost_per_day is None:
        cost_per_day = DEFAULT_COSTS[
            "miscellaneous_per_day"
        ]

    try:
        cost_per_day = float(cost_per_day)
    except (TypeError, ValueError):
        return 0.0

    return round(
        days * max(0, cost_per_day),
        2,
    )


def calculate_total_budget(
    distance_km,
    travelers,
    days,
    nights,
    places,
    transport_cost_per_km=None,
    food_cost_per_person_per_day=None,
    accommodation_cost_per_person_per_night=None,
    miscellaneous_cost_per_day=None,
    budget_level=None,
    daily_distances=None,
    pricing_method="auto",
    **kwargs,
):
    transport_details = None
    if budget_level is not None:
        from .cost_rules import get_budget_rules

        rules = get_budget_rules(budget_level)
        if food_cost_per_person_per_day is None:
            food_cost_per_person_per_day = rules.get("food_per_person_per_day")
        if accommodation_cost_per_person_per_night is None:
            accommodation_cost_per_person_per_night = rules.get(
                "accommodation_per_person_per_night"
            )
        if miscellaneous_cost_per_day is None:
            miscellaneous_cost_per_day = rules.get("miscellaneous_per_day")

        transport_details = calculate_cab_transport_cost(
            distance_km=distance_km,
            days=days,
            budget_level=budget_level,
            travelers=travelers,
            daily_distances=daily_distances,
            pricing_method=pricing_method,
            **kwargs,
        )
        transport = transport_details["cost"]
    else:
        transport = calculate_transport_cost(
            distance_km,
            transport_cost_per_km,
        )

    food = calculate_food_cost(
        travelers,
        days,
        food_cost_per_person_per_day,
    )

    accommodation = calculate_accommodation_cost(
        travelers,
        nights,
        accommodation_cost_per_person_per_night,
    )

    entry_fees = calculate_entry_fees(
        places,
        travelers,
    )

    miscellaneous = calculate_miscellaneous_cost(
        days,
        miscellaneous_cost_per_day,
    )

    total = (
        transport
        + food
        + accommodation
        + entry_fees
        + miscellaneous
    )

    if transport_details and "cost_min" in transport_details and "cost_max" in transport_details:
        total_min = round(
            transport_details["cost_min"]
            + food
            + accommodation
            + entry_fees
            + miscellaneous,
            2,
        )
        total_max = round(
            transport_details["cost_max"]
            + food
            + accommodation
            + entry_fees
            + miscellaneous,
            2,
        )
    else:
        total_min = round(total, 2)
        total_max = round(total, 2)

    return {
        "transport": round(transport, 2),
        "transport_details": transport_details,
        "food": round(food, 2),
        "accommodation": round(
            accommodation,
            2,
        ),
        "entry_fees": round(
            entry_fees,
            2,
        ),
        "miscellaneous": round(
            miscellaneous,
            2,
        ),
        "total": round(total, 2),
        "total_min": total_min,
        "total_max": total_max,
    }