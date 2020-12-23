from example_blog.models import Article


def test_migrate_data(init_article, session):
    count = session.query(Article).count()
    assert count == 3
