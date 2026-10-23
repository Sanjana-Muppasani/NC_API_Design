import os
import pytest
from dotenv import load_dotenv

load_dotenv()

@pytest.fixture(autouse=True, scope="function")
def configure_test_database():

    os.environ["ENV"] = "test"

    from db.seed import seed_database
    seed_database()