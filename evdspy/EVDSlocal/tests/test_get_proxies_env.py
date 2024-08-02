from evdspy.EVDSlocal.console.proxy_for_menu import get_proxies_env_helper


def test_get_proxies_env_helper(capsys):
    x1 = (["example:80", None, "example:80", None], {'http': 'example:80'})
    x2 = (["example:80", "example:80", "example:80", None], {'http': 'example:80', 'https': 'example:80'})
    x3 = (["example:80", "example:89", "example:90", "example:91"], {'http': 'example:80', 'https': 'example:89'})
    x4 = ([None, None, "example:90", "example:91"], {'http': 'example:90', 'https': 'example:91'})
    liste = [x1, x2, x3, x4]
    with capsys.disabled():
        for x, expected in liste:
            res = get_proxies_env_helper(*x)
            print(res)
            assert res == expected
