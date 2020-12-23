import pytest

from example_blog.dependencies import CommonQueryParams


@pytest.mark.parametrize(
    ['args', 'expect_value'],
    [
        ((), (0, 10)),
        ((0,), (0, 10)),
        ((-10, -10), (0, 10)),
        ((5, 100), (4, 100)),
    ]
)
def test_common_query_params(args, expect_value):
    params = CommonQueryParams(*args)
    assert params.offset == expect_value[0]
    assert params.limit == expect_value[1]
