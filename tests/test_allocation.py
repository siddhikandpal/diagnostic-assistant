import pytest
from modules.allocation import HospitalResourceAllocator

def test_resource_allocation():
    """Test resource allocation logic."""
    hospitals = {
        'Hospital_A': {'beds': 10, 'ambulances': 3},
        'Hospital_B': {'beds': 15, 'ambulances': 5},
        'Hospital_C': {'beds': 20, 'ambulances': 2}
    }
    patients = [
        {'id': 1, 'triage': 'Red'},
        {'id': 2, 'triage': 'Yellow'},
        {'id': 3, 'triage': 'Green'},
        {'id': 4, 'triage': 'Red'}
    ]

    allocator = HospitalResourceAllocator(hospitals, patients)
    allocator.allocate_resources()

    # Add assertions to verify the allocation logic
    # For example, check if all patients are assigned to hospitals