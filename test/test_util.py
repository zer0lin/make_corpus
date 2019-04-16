from util import check_chinese_char


def test_check_chinese_char_has_chinese():
    t_str = "aaaaaaaaa 在 中 一"
    assert check_chinese_char(t_str) is True


def test_check_chinese_char_no_chinese():
    t_str = "fdavwavaafq"
    assert check_chinese_char(t_str) is False
