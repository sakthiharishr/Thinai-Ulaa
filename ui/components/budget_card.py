import streamlit as st


DEFAULT_CURRENCY_RATES = {
    "₹ INR": {
        "symbol": "₹",
        "rate": 1.0,
        "code": "INR",
    },
    "$ USD": {
        "symbol": "$",
        "rate": 1 / 83.0,
        "code": "USD",
    },
    "€ EUR": {
        "symbol": "€",
        "rate": 1 / 90.0,
        "code": "EUR",
    },
    "£ GBP": {
        "symbol": "£",
        "rate": 1 / 105.0,
        "code": "GBP",
    },
    "¥ JPY": {
        "symbol": "¥",
        "rate": 1 / 0.56,
        "code": "JPY",
    },
    "د.إ AED": {
        "symbol": "د.إ ",
        "rate": 1 / 22.6,
        "code": "AED",
    },
}


def _convert(value, currency, currency_rates):
    try:
        value = float(value or 0)
    except (TypeError, ValueError):
        value = 0.0

    currency_data = currency_rates.get(
        currency,
        DEFAULT_CURRENCY_RATES["₹ INR"],
    )

    return value * float(
        currency_data.get("rate", 1.0)
    )


def _format_amount(
    value,
    currency,
    currency_rates,
):
    currency_data = currency_rates.get(
        currency,
        DEFAULT_CURRENCY_RATES["₹ INR"],
    )

    symbol = currency_data.get(
        "symbol",
        "₹",
    )

    converted = _convert(
        value,
        currency,
        currency_rates,
    )

    return f"{symbol}{converted:,.0f}"


def render_budget_card(
    budget,
    currency="₹ INR",
    currency_rates=None,
):
    if not budget:
        st.info(
            "No budget information available."
        )
        return

    currency_rates = (
        currency_rates
        or DEFAULT_CURRENCY_RATES
    )

    transport = budget.get(
        "transport",
        0,
    )

    food = budget.get(
        "food",
        0,
    )

    accommodation = budget.get(
        "accommodation",
        0,
    )

    entry_fees = budget.get(
        "entry_fees",
        0,
    )

    miscellaneous = budget.get(
        "miscellaneous",
        0,
    )

    total = budget.get(
        "total",
        0,
    )

    transport_details = budget.get("transport_details") or {}

    if transport_details:
        mode = transport_details.get("mode", "cab")
        vehicle = transport_details.get("vehicle", "Cab")
        vehicle_count = transport_details.get("vehicles", 1)
        vehicle_text = f"{vehicle} x {vehicle_count}" if vehicle_count > 1 else vehicle
        cost_min = transport_details.get("cost_min", transport)
        cost_max = transport_details.get("cost_max", transport)
        pricing_model = transport_details.get("pricing_model_used", "")
        billable_km = transport_details.get("billable_km", 0.0)
        actual_km = transport_details.get("actual_km", 0.0)
        driver = transport_details.get("driver_allowance", 0.0)
        tolls = transport_details.get("tolls_parking", 0.0)
        waiting = transport_details.get("waiting_charges", 0.0)

        range_str = f" (Est. range: {_format_amount(cost_min, currency, currency_rates)} – {_format_amount(cost_max, currency, currency_rates)})"

        if mode == "public_transit":
            st.caption(
                f"🚌 **Public Transit ({vehicle_text})**: Approximate bus/train fare for {actual_km:.1f} km{range_str}. "
                "No cab rental, driver, or toll charges apply. *(Approximate planning estimate)*"
            )
        else:
            model_info = (
                "Day rental package"
                if pricing_model == "fixed_package"
                else (
                    f"Distance-based ({billable_km:.0f} billable km"
                    + (f", actual route: {actual_km:.0f} km" if billable_km > actual_km else "")
                    + ")"
                )
            )
            addl_notes = []
            if driver > 0:
                addl_notes.append(f"driver allowance {_format_amount(driver, currency, currency_rates)}")
            if waiting > 0:
                addl_notes.append(f"waiting charges {_format_amount(waiting, currency, currency_rates)}")
            if tolls > 0:
                addl_notes.append(f"tolls/parking {_format_amount(tolls, currency, currency_rates)}")
            addl_str = f" Includes {', '.join(addl_notes)}." if addl_notes else ""
            st.caption(
                f"🚕 **Transportation ({vehicle_text})**: {model_info}{range_str}.{addl_str} *(Approximate planning estimate)*"
            )

    lines = (
        (
            "Accommodation",
            accommodation,
        ),
        (
            "Food",
            food,
        ),
        (
            "Transportation",
            transport,
        ),
        (
            "Miscellaneous",
            miscellaneous,
        ),
        (
            "Entry fees",
            entry_fees,
        ),
    )

    try:
        total_value = float(total)
    except (TypeError, ValueError):
        total_value = 0.0

    denominator = (
        total_value
        if total_value > 0
        else 1.0
    )

    rows = []

    for label, value in lines:

        try:
            numeric_value = float(
                value or 0
            )
        except (TypeError, ValueError):
            numeric_value = 0.0

        share = (
            max(
                0.0,
                numeric_value,
            )
            / denominator
            * 100
        )

        rows.append(
            '<div class="budget-item">'
            '<div class="budget-item-head">'
            f'<span class="budget-label">{label}</span>'
            f'<span class="budget-value">'
            f'{_format_amount(value, currency, currency_rates)}'
            f'<span class="budget-share">'
            f'{share:.0f}%'
            "</span>"
            "</span>"
            "</div>"
            f'<div class="budget-bar">'
            f'<span style="--share:{share:.1f}%"></span>'
            "</div>"
            "</div>"
        )

    html = (
        '<div class="budget-card reveal">'
        '<div class="budget-total-label">'
        "Estimated total"
        "</div>"
        f'<div class="budget-total">'
        f'{_format_amount(total, currency, currency_rates)}'
        "</div>"
        + "".join(rows)
        + "</div>"
    )

    st.markdown(
        html,
        unsafe_allow_html=True,
    )

    with st.expander("📋 Detailed Transportation & Expense Breakdown", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Transportation Breakdown**")
            if transport_details and transport_details.get("mode") == "cab":
                if transport_details.get("pricing_model_used") == "fixed_package":
                    st.write(f"- Base package: {_format_amount(transport_details.get('base_package', 0), currency, currency_rates)}")
                    st.write(f"- Extra km charges: {_format_amount(transport_details.get('distance_charge', 0), currency, currency_rates)}")
                else:
                    st.write(f"- Distance charges ({transport_details.get('billable_km', 0):.0f} billable km): {_format_amount(transport_details.get('distance_charge', 0), currency, currency_rates)}")
                st.write(f"- Driver allowance: {_format_amount(transport_details.get('driver_allowance', 0), currency, currency_rates)}")
                st.write(f"- Waiting charges: {_format_amount(transport_details.get('waiting_charges', 0), currency, currency_rates)}")
                st.write(f"- Tolls & parking: {_format_amount(transport_details.get('tolls_parking', 0), currency, currency_rates)}")
                st.write(f"- **Total Transportation:** {_format_amount(transport, currency, currency_rates)}")
            elif transport_details and transport_details.get("mode") == "public_transit":
                st.write(f"- Bus / Train transit fare: {_format_amount(transport, currency, currency_rates)}")
                st.write(f"- Driver allowance: {_format_amount(0, currency, currency_rates)}")
                st.write(f"- Waiting charges: {_format_amount(0, currency, currency_rates)}")
                st.write(f"- Tolls & parking: {_format_amount(0, currency, currency_rates)}")
                st.write(f"- **Total Transportation:** {_format_amount(transport, currency, currency_rates)}")
            else:
                st.write(f"- Transit estimate: {_format_amount(transport, currency, currency_rates)}")
        with col2:
            st.markdown("**Other Trip Expenses**")
            st.write(f"- Food expenses: {_format_amount(food, currency, currency_rates)}")
            st.write(f"- Accommodation: {_format_amount(accommodation, currency, currency_rates)}")
            st.write(f"- Entry fees: {_format_amount(entry_fees, currency, currency_rates)}")
            st.write(f"- Other expenses: {_format_amount(miscellaneous, currency, currency_rates)}")
            st.write(f"- **Total Estimated Budget:** {_format_amount(total, currency, currency_rates)}")
        st.caption("All figures are approximate planning estimates and subject to actual operator tariffs and route conditions.")


def render_budget_summary(
    budget,
    currency="₹ INR",
    currency_rates=None,
):
    if not budget:
        return

    currency_rates = (
        currency_rates
        or DEFAULT_CURRENCY_RATES
    )

    total = budget.get(
        "total",
        0,
    )

    try:
        total = float(total)
    except (TypeError, ValueError):
        total = 0.0

    st.metric(
        "Estimated Trip Cost",
        _format_amount(
            total,
            currency,
            currency_rates,
        ),
    )