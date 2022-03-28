from ISS_Tracker_app import *
from flask import jsonify
import pytest

def test_help():
    assert isinstance(help(),str)==True

def test_get_epochs():
    assert isinstance(get_epochs(),str)==True
    assert isinstance(get_epochs(),float)==False

def test_get_countries():
    assert isinstance(list_countries(), int)==False

def test_list_cities():
    assert isinstance(list_regions('x'), float)==False

def test_city_data():
    assert isinstance(city_data('x','y','z'), int)==False


def test_load():
    with pytest.raises(TypeError):
        load('')

def test_get_epoch():
    with pytest.raises(NameError):
        get_epoch(x)

def test_country_data():
    with pytest.raises(TypeError):
        country_data()

def test_list_regions():
    with pytest.raises(TypeError):
        list_regions()

def test_region_data():
    with pytest.raises(TypeError):
        region_data()
