from services.budget.calculator import (
    calculate_accommodation_cost,
    calculate_cab_transport_cost,
    calculate_entry_fees,
    calculate_food_cost,
    calculate_miscellaneous_cost,
    calculate_total_budget,
    calculate_transport_cost,
)
from services.budget.cost_rules import COST_RULES, get_budget_rules, get_transport_config


def test_transport_cost_uses_distance_and_rate():
    assert calculate_transport_cost(100, 8) == 800.0
    assert calculate_transport_cost(-5, 8) == 0.0
    assert calculate_transport_cost("far", 8) == 0.0


def test_food_and_accommodation_scale_with_travelers_and_time():
    assert calculate_food_cost(2, 3, 500) == 3000.0
    assert calculate_accommodation_cost(2, 2, 1200) == 4800.0
    # A day trip has no nights to pay for.
    assert calculate_accommodation_cost(2, 0, 1200) == 0.0


def test_entry_fees_ignore_missing_and_bad_values():
    places = [{"entry_fee": 50}, {"entry_fee": None}, {"entry_fee": "free"}, {}]
    assert calculate_entry_fees(places, travelers=3) == 150.0


def test_total_budget_is_sum_of_parts():
    budget = calculate_total_budget(
        distance_km=39.1, travelers=2, days=3, nights=2, places=[{"entry_fee": 40}],
        transport_cost_per_km=8, food_cost_per_person_per_day=500,
        accommodation_cost_per_person_per_night=1200, miscellaneous_cost_per_day=200,
    )
    parts = ("transport", "food", "accommodation", "entry_fees", "miscellaneous")
    assert budget["total"] == round(sum(budget[part] for part in parts), 2)
    assert budget["transport"] == 312.8
    assert budget["entry_fees"] == 80.0


# ---------------------------------------------------------------------------
# Specific Scenarios for Transportation Calculation Update
# ---------------------------------------------------------------------------

def test_scenario_1_budget_retains_minimal_public_transportation():
    """1. Budget category uses public transit/bus calculation without cab/driver/waiting/toll charges."""
    res = calculate_cab_transport_cost(
        distance_km=100.0,
        days=2,
        budget_level="budget",
        travelers=2,
    )
    assert res["mode"] == "public_transit"
    assert res["driver_allowance"] == 0.0
    assert res["waiting_charges"] == 0.0
    assert res["tolls_parking"] == 0.0
    # Bus scales per traveler: 100 km * 2.5/km * 2 travelers = 500.0
    assert res["cost"] == 500.0
    assert res["rate_range"] == (2.0, 3.0)
    assert res["cost_min"] == 400.0  # 100 * 2.0 * 2
    assert res["cost_max"] == 600.0  # 100 * 3.0 * 2


def test_scenario_2_standard_uses_10_to_15_per_km():
    """2. Standard category uses WagonR cab @ ₹10–₹15/km."""
    res = calculate_cab_transport_cost(
        distance_km=300.0,
        days=1,
        budget_level="standard",
        travelers=2,
        pricing_method="distance",
    )
    assert "WagonR" in res["vehicle"]
    assert res["rate_range"] == (10.0, 15.0)
    assert res["rate_per_km"] == 12.0
    # Billable km: 300 km (above 250 min). Driver: 400, waiting: 200, tolls: 200.
    # Cost = 300 * 12 + 400 + 200 + 200 = 3600 + 800 = 4400.0
    assert res["cost"] == 4400.0
    # Min cost = 300 * 10 + 800 = 3800.0
    assert res["cost_min"] == 3800.0
    # Max cost = 300 * 15 + 800 = 5300.0
    assert res["cost_max"] == 5300.0


def test_scenario_3_premium_uses_16_to_22_per_km():
    """3. Premium category uses Innova SUV @ ₹16–₹22/km."""
    res = calculate_cab_transport_cost(
        distance_km=300.0,
        days=1,
        budget_level="premium",
        travelers=2,
        pricing_method="distance",
    )
    assert "Innova" in res["vehicle"]
    assert res["rate_range"] == (16.0, 22.0)
    assert res["rate_per_km"] == 18.0
    # Billable km: 300 km (above 250 min). Driver: 500, waiting: 300, tolls: 350.
    # Cost = 300 * 18 + 500 + 300 + 350 = 5400 + 1150 = 6550.0
    assert res["cost"] == 6550.0
    # Min cost = 300 * 16 + 1150 = 5950.0
    assert res["cost_min"] == 5950.0
    # Max cost = 300 * 22 + 1150 = 7750.0
    assert res["cost_max"] == 7750.0


def test_scenario_4_increasing_distance_increases_estimate():
    """4. Increasing route distance increases distance-based transport estimate appropriately."""
    short_trip = calculate_cab_transport_cost(
        distance_km=300.0,
        days=1,
        budget_level="standard",
        pricing_method="distance",
    )
    long_trip = calculate_cab_transport_cost(
        distance_km=500.0,
        days=1,
        budget_level="standard",
        pricing_method="distance",
    )
    assert long_trip["cost"] > short_trip["cost"]
    assert long_trip["cost"] - short_trip["cost"] == (500.0 - 300.0) * 12.0


def test_scenario_5_daily_minimum_billable_km_applied():
    """5. A day's minimum billable km applies when actual distance is below the configured minimum."""
    res = calculate_cab_transport_cost(
        distance_km=80.0,
        days=1,
        budget_level="standard",
        pricing_method="distance",
        daily_min_km=250.0,
    )
    assert res["actual_km"] == 80.0
    assert res["billable_km"] == 250.0
    assert res["is_minimum_distance_applied"] is True
    # Distance charge should be on 250 km, not 80 km
    assert res["distance_charge"] == 250.0 * 12.0


def test_scenario_6_multi_day_trips_apply_daily_minimum_separately_per_day():
    """6. Multi-day trips apply daily minimum separately to each rental day rather than once to trip."""
    # Day 1: 50 km (< 250 min) -> billable 250
    # Day 2: 320 km (> 250 min) -> billable 320
    # Day 3: 100 km (< 250 min) -> billable 250
    # Total billable: 250 + 320 + 250 = 820 km (actual: 470 km)
    # If applied as 3 * 250 = 750, it would incorrectly give 750 km.
    res = calculate_cab_transport_cost(
        distance_km=470.0,
        days=3,
        budget_level="standard",
        daily_distances=[50.0, 320.0, 100.0],
        pricing_method="distance",
        daily_min_km=250.0,
    )
    assert res["daily_billable_km"] == [250.0, 320.0, 250.0]
    assert res["billable_km"] == 820.0
    assert res["actual_km"] == 470.0
    assert res["distance_charge"] == 820.0 * 12.0


def test_scenario_7_fixed_daily_packages_handled_without_duplicate_distance_charges():
    """7. Fixed daily package comparison without duplicate distance charges."""
    # 1-day package with 100 km included @ ₹2200 base, extra km @ ₹12.
    # Total trip 150 km: base covers 100 km, extra 50 km charged @ ₹12 = ₹600.
    res = calculate_cab_transport_cost(
        distance_km=150.0,
        days=1,
        budget_level="standard",
        pricing_method="package",
    )
    assert res["pricing_model_used"] == "fixed_package"
    assert res["included_km"] == 100.0
    assert res["extra_km"] == 50.0
    assert res["base_package"] == 2200.0
    assert res["distance_charge"] == 50.0 * 12.0  # extra km charge only
    # Driver and waiting are included in base package
    assert res["driver_allowance"] == 0.0
    assert res["waiting_charges"] == 0.0
    # Tolls & parking (200.0) added
    assert res["tolls_parking"] == 200.0
    assert res["cost"] == 2200.0 + 600.0 + 200.0  # 3000.0


def test_scenario_8_driver_allowance_and_waiting_charges_included_only_when_applicable():
    """8. Driver allowance and waiting charges included only when applicable."""
    standard_res = calculate_cab_transport_cost(
        distance_km=300.0,
        days=2,
        budget_level="standard",
        pricing_method="distance",
    )
    assert standard_res["driver_allowance"] == 400.0 * 2  # ₹800
    assert standard_res["waiting_charges"] == 200.0 * 2  # ₹400

    premium_res = calculate_cab_transport_cost(
        distance_km=300.0,
        days=2,
        budget_level="premium",
        pricing_method="distance",
    )
    assert premium_res["driver_allowance"] == 500.0 * 2  # ₹1000
    assert premium_res["waiting_charges"] == 300.0 * 2  # ₹600

    budget_res = calculate_cab_transport_cost(
        distance_km=300.0,
        days=2,
        budget_level="budget",
    )
    assert budget_res["driver_allowance"] == 0.0
    assert budget_res["waiting_charges"] == 0.0


def test_scenario_9_shared_cab_cost_not_multiplied_by_number_of_passengers():
    """9. Shared cab cost is at vehicle level, not multiplied by number of passengers."""
    cost_1_pax = calculate_cab_transport_cost(
        distance_km=300.0,
        days=1,
        budget_level="standard",
        travelers=1,
        pricing_method="distance",
    )
    cost_4_pax = calculate_cab_transport_cost(
        distance_km=300.0,
        days=1,
        budget_level="standard",
        travelers=4,
        pricing_method="distance",
    )
    # Capacity is 4, so 1 or 4 passengers both need 1 vehicle
    assert cost_1_pax["vehicles"] == 1
    assert cost_4_pax["vehicles"] == 1
    assert cost_1_pax["cost"] == cost_4_pax["cost"]

    # 5 travelers need 2 vehicles (WagonR capacity is 4)
    cost_5_pax = calculate_cab_transport_cost(
        distance_km=300.0,
        days=1,
        budget_level="standard",
        travelers=5,
        pricing_method="distance",
    )
    assert cost_5_pax["vehicles"] == 2
    assert cost_5_pax["cost"] == cost_1_pax["cost"] * 2


def test_scenario_10_tolls_parking_food_stays_entry_fees_in_total_budget():
    """10. Tolls, parking, food, stays, and entry fees are correctly included in total budget."""
    places = [{"entry_fee": 100.0}, {"entry_fee": 50.0}]
    budget = calculate_total_budget(
        distance_km=300.0,
        travelers=2,
        days=2,
        nights=1,
        places=places,
        budget_level="standard",
        pricing_method="distance",
    )
    # Entry fees = (100 + 50) * 2 travelers = 300.0
    assert budget["entry_fees"] == 300.0
    # Food = 2 travelers * 2 days * 500 = 2000.0
    assert budget["food"] == 2000.0
    # Accommodation = 2 travelers * 1 night * 1200 = 2400.0
    assert budget["accommodation"] == 2400.0
    # Miscellaneous = 2 days * 200 = 400.0
    assert budget["miscellaneous"] == 400.0
    # Transport includes distance + driver + waiting + tolls/parking
    t_details = budget["transport_details"]
    assert t_details["tolls_parking"] == 200.0 * 2  # 400.0
    assert budget["total"] == round(
        budget["transport"]
        + budget["food"]
        + budget["accommodation"]
        + budget["entry_fees"]
        + budget["miscellaneous"],
        2,
    )


def test_scenario_11_changing_duration_route_or_budget_category_recalculates():
    """11. Changing itinerary duration, route, or budget category recalculates estimate."""
    budget_standard_1d = calculate_total_budget(
        distance_km=100.0, travelers=2, days=1, nights=0, places=[], budget_level="standard"
    )
    budget_standard_3d = calculate_total_budget(
        distance_km=100.0, travelers=2, days=3, nights=2, places=[], budget_level="standard"
    )
    budget_premium_1d = calculate_total_budget(
        distance_km=100.0, travelers=2, days=1, nights=0, places=[], budget_level="premium"
    )
    # Changing days increases budget
    assert budget_standard_3d["total"] > budget_standard_1d["total"]
    # Changing category from standard to premium increases budget
    assert budget_premium_1d["total"] > budget_standard_1d["total"]


def test_scenario_12_missing_coordinates_and_optional_data_safe():
    """12. Missing coordinates, bad inputs, and optional pricing data do not crash."""
    safe_cab = calculate_cab_transport_cost(
        distance_km=None,
        days="invalid",
        budget_level="unknown_tier",
        travelers=-1,
        daily_distances=[None, "bad", -10],
    )
    assert safe_cab["cost"] >= 0.0
    assert safe_cab["vehicles"] >= 1

    safe_budget = calculate_total_budget(
        distance_km=None,
        travelers=None,
        days=-5,
        nights="unknown",
        places=None,
        budget_level=None,
    )
    assert safe_budget["total"] >= 0.0
    assert safe_budget["transport"] >= 0.0


def test_scenario_13_route_distance_deduplication_and_fallback():
    """13. Starting place is not counted twice as destination, and missing coordinates fallback safely."""
    from app_pages.itinerary import _calculate_route_distance, _calculate_budget

    p1 = {"place_id": 1, "latitude": 11.0, "longitude": 77.0}
    p2 = {"place_id": 2, "latitude": 11.2, "longitude": 77.2}
    p_no_coord = {"place_id": 3, "latitude": None, "longitude": None}

    # Starting place p1 is also in destination list - must not be counted twice
    dist_with_duplicate = _calculate_route_distance([p1, p2], start_place=p1)
    dist_without_duplicate = _calculate_route_distance([p2], start_place=p1)
    assert dist_with_duplicate == dist_without_duplicate

    # Missing coordinates use fallback 25 km leg safely
    dist_with_missing = _calculate_route_distance([p_no_coord], start_place=p1)
    assert dist_with_missing == 25.0

    # Integration: _calculate_budget returns valid budget structure with daily_distances
    budget, total_km = _calculate_budget(
        selected_places=[p1, p2],
        travelers=2,
        days=2,
        budget_level="standard",
        start_place=p1,
        daily_distances=[100.0, 150.0],
    )
    assert budget["total"] > 0
    assert budget["transport_details"]["billable_km"] == 500.0  # 2 days * 250 km daily min
