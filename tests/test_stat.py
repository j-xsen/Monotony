from objects.player.stat import Stat

def test_change_value():
    add_stat = Stat(100)
    sub_stat = Stat(0)
    add_stat += 25
    sub_stat -= 25
    assert add_stat.value == 100 and sub_stat.value == 0
