import pytest
from shipping_quote import process_shipments, monitor_container_pressures

# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# process_shipments â€“ guard clause
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

def test_raises_if_shipments_not_list():
    """Branch: not isinstance(shipments, list) â†’ True"""
    with pytest.raises(ValueError):
        process_shipments("not a list", 10.0)

def test_raises_if_handling_fee_negative():
    """Branch: handling_fee < 0 â†’ True"""
    with pytest.raises(ValueError):
        process_shipments([], -1.0)

# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# process_shipments â€“ empty / no-cargo paths
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

def test_empty_shipments_list_returns_no_cargo():
    """No shipments â†’ total_quote stays 0.0 â†’ NO_CARGO"""
    result = process_shipments([], 5.0)
    assert result["total_quote"] == 0.0
    assert result["status"] == "NO_CARGO"

def test_all_shipments_not_approved_returns_no_cargo():
    """Branch: manifest_approved False â†’ continue (all skipped) â†’ NO_CARGO"""
    shipments = [
        {"manifest_approved": False, "mode": "ground", "packages": [{"weight_kg": 10, "is_hazmat": False}]}
    ]
    result = process_shipments(shipments, 5.0)
    assert result["status"] == "NO_CARGO"

# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# process_shipments â€“ transport mode branches
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

def test_single_ground_shipment():
    """Branch: mode == 'ground' â†’ base_rate = 4.0; weight â‰¤ 30 â†’ weight * base_rate"""
    shipments = [
        {
            "manifest_approved": True,
            "mode": "ground",
            "is_fragile": False,
            "express_priority": False,
            "packages": [{"weight_kg": 10, "is_hazmat": False}]
        }
    ]
    result = process_shipments(shipments, 20.0)
    # handling_fee 20 + 10*4 = 60
    assert result["total_quote"] == 60.0
    assert result["status"] == "CLEARED"

def test_single_air_shipment():
    """Branch: mode == 'air' â†’ base_rate = 12.0"""
    shipments = [
        {
            "manifest_approved": True,
            "mode": "air",
            "is_fragile": False,
            "express_priority": False,
            "packages": [{"weight_kg": 5, "is_hazmat": False}]
        }
    ]
    result = process_shipments(shipments, 10.0)
    # handling_fee 10 + 5*12 = 70
    assert result["total_quote"] == 70.0
    assert result["status"] == "CLEARED"

def test_unknown_transport_mode_rejected():
    """Branch: mode not 'air'/'ground' â†’ rejected_parcels += 1; continue"""
    shipments = [
        {
            "manifest_approved": True,
            "mode": "sea",          # unknown mode
            "is_fragile": False,
            "express_priority": False,
            "packages": [{"weight_kg": 5, "is_hazmat": False}]
        }
    ]
    result = process_shipments(shipments, 0.0)
    # rejected_parcels == 1 (â‰¤ 3), total_quote stays 0 â†’ NO_CARGO
    assert result["status"] == "NO_CARGO"

# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# process_shipments â€“ package weight branches
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

def test_package_zero_weight_rejected():
    """Branch: weight <= 0 â†’ rejected_parcels += 1; continue"""
    shipments = [
        {
            "manifest_approved": True,
            "mode": "ground",
            "is_fragile": False,
            "express_priority": False,
            "packages": [{"weight_kg": 0, "is_hazmat": False}]
        }
    ]
    result = process_shipments(shipments, 0.0)
    # Only handling_fee (0) is added; total_quote == 0 â†’ NO_CARGO
    assert result["status"] == "NO_CARGO"

def test_package_negative_weight_rejected():
    """Branch: weight <= 0 (negative) â†’ rejected_parcels += 1; continue"""
    shipments = [
        {
            "manifest_approved": True,
            "mode": "ground",
            "is_fragile": False,
            "express_priority": False,
            "packages": [{"weight_kg": -5, "is_hazmat": False}]
        }
    ]
    result = process_shipments(shipments, 0.0)
    assert result["status"] == "NO_CARGO"

def test_heavy_package_above_30kg():
    """Branch: weight > 30 â†’ weight * (base_rate * 1.5)"""
    shipments = [
        {
            "manifest_approved": True,
            "mode": "ground",
            "is_fragile": False,
            "express_priority": False,
            "packages": [{"weight_kg": 40, "is_hazmat": False}]
        }
    ]
    result = process_shipments(shipments, 0.0)
    # 40 * (4.0 * 1.5) = 40 * 6 = 240
    assert result["total_quote"] == 240.0
    assert result["status"] == "CLEARED"

def test_package_exactly_30kg_uses_normal_rate():
    """Boundary: weight == 30 â†’ NOT > 30 â†’ normal rate"""
    shipments = [
        {
            "manifest_approved": True,
            "mode": "ground",
            "is_fragile": False,
            "express_priority": False,
            "packages": [{"weight_kg": 30, "is_hazmat": False}]
        }
    ]
    result = process_shipments(shipments, 0.0)
    # 30 * 4.0 = 120
    assert result["total_quote"] == 120.0
    assert result["status"] == "CLEARED"

# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# process_shipments â€“ hazmat branches
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

def test_hazmat_non_fragile_adds_surcharge():
    """Branch: hazmat True, is_fragile False â†’ rejected += 1; shipment_cost += 50"""
    shipments = [
        {
            "manifest_approved": True,
            "mode": "ground",
            "is_fragile": False,
            "express_priority": False,
            "packages": [{"weight_kg": 10, "is_hazmat": True}]
        }
    ]
    result = process_shipments(shipments, 0.0)
    # 0 + 50 = 50
    assert result["total_quote"] == 50.0
    assert result["status"] == "CLEARED"

def test_hazmat_fragile_shipment_cost_zeroed_and_breaks():
    """Branch: hazmat True, is_fragile True â†’ shipment_cost = 0.0; break"""
    shipments = [
        {
            "manifest_approved": True,
            "mode": "ground",
            "is_fragile": True,
            "express_priority": False,
            "packages": [
                {"weight_kg": 10, "is_hazmat": True},
                {"weight_kg": 20, "is_hazmat": False}  # should NOT be processed after break
            ]
        }
    ]
    result = process_shipments(shipments, 100.0)
    # shipment_cost = 0.0 after break; express_priority False so stays 0
    # total_quote = 0.0 â†’ NO_CARGO
    assert result["total_quote"] == 0.0
    assert result["status"] == "NO_CARGO"

def test_hazmat_fragile_with_express_priority():
    """After fragile+hazmat break, express_priority multiplier applied to 0.0 â†’ still 0"""
    shipments = [
        {
            "manifest_approved": True,
            "mode": "air",
            "is_fragile": True,
            "express_priority": True,
            "packages": [{"weight_kg": 5, "is_hazmat": True}]
        }
    ]
    result = process_shipments(shipments, 50.0)
    # shipment_cost zeroed â†’ 0 * 1.25 = 0 â†’ NO_CARGO
    assert result["total_quote"] == 0.0
    assert result["status"] == "NO_CARGO"

# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# process_shipments â€“ express priority branch
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

def test_express_priority_multiplier():
    """Branch: express_priority True â†’ shipment_cost *= 1.25"""
    shipments = [
        {
            "manifest_approved": True,
            "mode": "ground",
            "is_fragile": False,
            "express_priority": True,
            "packages": [{"weight_kg": 10, "is_hazmat": False}]
        }
    ]
    result = process_shipments(shipments, 0.0)
    # (0 + 10*4) * 1.25 = 40 * 1.25 = 50
    assert result["total_quote"] == 50.0
    assert result["status"] == "CLEARED"

# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# process_shipments â€“ FLAGGED_REVIEW branch (rejected_parcels > 3)
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

def test_flagged_review_when_rejected_parcels_exceeds_3():
    """Branch: rejected_parcels > 3 â†’ FLAGGED_REVIEW"""
    # 4 unknown-mode shipments â†’ 4 rejections
    bad_mode_shipment = {
        "manifest_approved": True,
        "mode": "sea",
        "is_fragile": False,
        "express_priority": False,
        "packages": []
    }
    # Also add one valid shipment so total_quote > 0
    valid_shipment = {
        "manifest_approved": True,
        "mode": "ground",
        "is_fragile": False,
        "express_priority": False,
        "packages": [{"weight_kg": 5, "is_hazmat": False}]
    }
    shipments = [bad_mode_shipment] * 4 + [valid_shipment]
    result = process_shipments(shipments, 0.0)
    assert result["status"] == "FLAGGED_REVIEW"

def test_flagged_review_via_bad_packages():
    """Reach rejected_parcels > 3 through zero-weight + hazmat packages"""
    shipment = {
        "manifest_approved": True,
        "mode": "ground",
        "is_fragile": False,
        "express_priority": False,
        "packages": [
            {"weight_kg": 0, "is_hazmat": False},   # rejected
            {"weight_kg": 0, "is_hazmat": False},   # rejected
            {"weight_kg": 10, "is_hazmat": True},   # rejected (hazmat non-fragile)
            {"weight_kg": 10, "is_hazmat": True},   # rejected (hazmat non-fragile)
        ]
    }
    result = process_shipments([shipment], 0.0)
    # rejected_parcels == 4 > 3 â†’ FLAGGED_REVIEW
    assert result["status"] == "FLAGGED_REVIEW"

def test_exactly_3_rejections_not_flagged():
    """Boundary: rejected_parcels == 3 â†’ NOT flagged (must be > 3)"""
    bad_mode_shipment = {
        "manifest_approved": True,
        "mode": "sea",
        "is_fragile": False,
        "express_priority": False,
        "packages": []
    }
    valid_shipment = {
        "manifest_approved": True,
        "mode": "ground",
        "is_fragile": False,
        "express_priority": False,
        "packages": [{"weight_kg": 5, "is_hazmat": False}]
    }
    shipments = [bad_mode_shipment] * 3 + [valid_shipment]
    result = process_shipments(shipments, 0.0)
    # rejected_parcels == 3, not > 3 â†’ CLEARED
    assert result["status"] == "CLEARED"

# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# process_shipments â€“ multiple packages in one shipment
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

def test_multiple_packages_mixed():
    """Multiple packages: normal, heavy, hazmat non-fragile all in one shipment"""
    shipments = [
        {
            "manifest_approved": True,
            "mode": "air",
            "is_fragile": False,
            "express_priority": False,
            "packages": [
                {"weight_kg": 10, "is_hazmat": False},   # 10 * 12 = 120
                {"weight_kg": 40, "is_hazmat": False},   # 40 * 18 = 720
                {"weight_kg": 5,  "is_hazmat": True},    # +50 (hazmat surcharge)
            ]
        }
    ]
    result = process_shipments(shipments, 0.0)
    # 0 + 120 + 720 + 50 = 890
    assert result["total_quote"] == 890.0
    assert result["status"] == "CLEARED"

def test_shipment_with_no_packages():
    """Shipment with empty packages list â†’ only handling_fee added"""
    shipments = [
        {
            "manifest_approved": True,
            "mode": "ground",
            "is_fragile": False,
            "express_priority": False,
            "packages": []
        }
    ]
    result = process_shipments(shipments, 15.0)
    assert result["total_quote"] == 15.0
    assert result["status"] == "CLEARED"

# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# monitor_container_pressures
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

def test_empty_pressure_logs_returns_no_data():
    """Branch: not pressure_logs (empty list) â†’ NO_DATA"""
    assert monitor_container_pressures([]) == "NO_DATA"

def test_none_pressure_logs_returns_no_data():
    """Branch: not pressure_logs (None) â†’ NO_DATA"""
    assert monitor_container_pressures(None) == "NO_DATA"

def test_all_pressures_stable():
    """Branch: all psi >= 14.0 â†’ streak always reset â†’ STABLE"""
    logs = [[15.0, 16.0, 14.5, 20.0]]
    assert monitor_container_pressures(logs) == "STABLE"

def test_single_low_pressure_no_leak():
    """Branch: one psi < 14, streak = 1 (< 2) â†’ no leak; resets on next ok â†’ STABLE"""
    logs = [[15.0, 13.0, 15.0]]
    assert monitor_container_pressures(logs) == "STABLE"

def test_two_consecutive_low_pressures_leak_detected():
    """Branch: streak >= 2 â†’ LEAK_DETECTED"""
    logs = [[15.0, 13.0, 13.0, 15.0]]
    assert monitor_container_pressures(logs) == "LEAK_DETECTED"

def test_leak_on_first_two_readings():
    """Leak detected immediately on first two readings"""
    logs = [[13.0, 12.0]]
    assert monitor_container_pressures(logs) == "LEAK_DETECTED"

def test_leak_in_second_container():
    """LEAK_DETECTED found in second container while first is stable"""
    logs = [
        [15.0, 16.0],           # stable container
        [14.5, 13.0, 12.5]     # leak in second container
    ]
    assert monitor_container_pressures(logs) == "LEAK_DETECTED"

def test_multiple_containers_all_stable():
    """Multiple containers, all stable â†’ STABLE"""
    logs = [
        [15.0, 14.0, 16.0],
        [20.0, 18.0],
        [14.1, 14.2, 15.0]
    ]
    assert monitor_container_pressures(logs) == "STABLE"

def test_streak_resets_after_normal_pressure():
    """Low psi then normal psi resets streak; next low does not trigger leak alone"""
    logs = [[13.0, 15.0, 13.0, 15.0]]
    # streak hits 1, then resets, then 1 again â†’ STABLE
    assert monitor_container_pressures(logs) == "STABLE"

def test_exactly_at_14_psi_is_stable():
    """Boundary: psi == 14.0 is NOT < 14.0 â†’ streak resets â†’ STABLE"""
    logs = [[14.0, 14.0, 14.0]]
    assert monitor_container_pressures(logs) == "STABLE"

def test_just_below_14_psi_counts_toward_streak():
    """Boundary: psi == 13.999 < 14.0 â†’ counted as low pressure"""
    logs = [[13.999, 13.999]]
    assert monitor_container_pressures(logs) == "LEAK_DETECTED"
