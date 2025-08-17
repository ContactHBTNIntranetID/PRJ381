import sys
import os

# Add the root folder to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from validator import Validator

@pytest.fixture
def validator():
    return Validator()

# ------------------ TEMPERATURE ------------------ #
def test_validate_temperature_valid(validator):
    result = validator.validate_temperature(25)
    assert result["valid"] is True
    assert "Valid temperature" in result["message"]

def test_validate_temperature_invalid_type(validator):
    result = validator.validate_temperature("hot")
    assert result["valid"] is False
    assert "must be a number" in result["message"]

def test_validate_temperature_out_of_range(validator):
    result = validator.validate_temperature(-100)
    assert result["valid"] is False
    assert "out of realistic range" in result["message"]

# ------------------ HUMIDITY ------------------ #
def test_validate_humidity_valid(validator):
    result = validator.validate_humidity(50)
    assert result["valid"] is True

def test_validate_humidity_invalid_type(validator):
    result = validator.validate_humidity("wet")
    assert result["valid"] is False

def test_validate_humidity_out_of_range(validator):
    result = validator.validate_humidity(200)
    assert result["valid"] is False

# ------------------ PRESSURE ------------------ #
def test_validate_pressure_valid(validator):
    result = validator.validate_pressure(1013)
    assert result["valid"] is True

def test_validate_pressure_out_of_range(validator):
    result = validator.validate_pressure(200)
    assert result["valid"] is False

# ------------------ RAINFALL ------------------ #
def test_validate_rainfall_valid(validator):
    result = validator.validate_rainfall(10)
    assert result["valid"] is True

def test_validate_rainfall_negative(validator):
    result = validator.validate_rainfall(-5)
    assert result["valid"] is False

# ------------------ GPS ------------------ #
def test_validate_gps_coordinates_valid(validator):
    result = validator.validate_gps_coordinates(-25.7, 28.2)
    assert result["valid"] is True

def test_validate_gps_coordinates_invalid_type(validator):
    result = validator.validate_gps_coordinates("lat", "lon")
    assert result["valid"] is False

def test_validate_gps_coordinates_out_of_range(validator):
    result = validator.validate_gps_coordinates(100, 200)
    assert result["valid"] is False



