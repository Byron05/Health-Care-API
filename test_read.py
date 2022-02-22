from read_json import read_json

def test_read_valid():

    flag1, message1 = read_json("oxygen_level.json")
    assert flag1 == True

def test_read_invalid():

    flag1, message1 = read_json("temperature.json")
    assert flag1 == False