from security_toolkit.core import parse_ports, service_for


def test_parse_single():
    assert parse_ports("80") == [80]


def test_parse_list():
    assert parse_ports("22,80,443") == [22, 80, 443]


def test_parse_range():
    assert parse_ports("1-5") == [1, 2, 3, 4, 5]


def test_parse_mixed_dedup_sorted():
    assert parse_ports("443,80,80,1-3") == [1, 2, 3, 80, 443]


def test_parse_invalid_range():
    try:
        parse_ports("500-100")
        assert False, "debería lanzar ValueError"
    except ValueError:
        pass


def test_parse_out_of_range():
    try:
        parse_ports("70000")
        assert False, "debería lanzar ValueError"
    except ValueError:
        pass


def test_common_services():
    assert service_for(22) == "ssh"
    assert service_for(3306) == "mysql"
    assert service_for(5432) == "postgresql"
    assert service_for(1) is None
