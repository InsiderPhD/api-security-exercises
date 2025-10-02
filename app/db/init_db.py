from sqlalchemy.exc import SQLAlchemyError

from app.db.session import Base, engine, SessionLocal

# Import models so they are registered with SQLAlchemy's metadata
# Each exercise keeps its own models.py to preserve isolation
from app.exercises.ex1 import models as ex1_models  # noqa: F401
from app.exercises.ex2 import models as ex2_models  # noqa: F401
from app.exercises.ex3 import models as ex3_models  # noqa: F401
from app.exercises.ex4 import models as ex4_models  # noqa: F401
from app.exercises.ex5 import models as ex5_models  # noqa: F401
from app.exercises.ex6 import models as ex6_models  # noqa: F401
from app.exercises.ex7 import models as ex7_models  # noqa: F401
from app.exercises.ex8 import models as ex8_models  # noqa: F401
from app.exercises.ex10 import models as ex10_models  # noqa: F401
from app.exercises.ex12 import models as ex12_models  # noqa: F401


def initialize_database() -> None:
    try:
        Base.metadata.create_all(bind=engine)
        # Seed base data
        with SessionLocal() as session:
            has_message = session.query(ex1_models.Message).first() is not None
            if not has_message:
                session.add(ex1_models.Message(content="hello world!"))
                session.commit()

            has_coupon = session.query(ex3_models.Coupon).filter(ex3_models.Coupon.code == "WELCOME5").first()
            if not has_coupon:
                session.add(ex3_models.Coupon(code="WELCOME5", discount_amount_cents=500, remaining_uses=3))
                session.commit()

            has_docs = session.query(ex6_models.Document).first() is not None
            if not has_docs:
                user_a = "11111111-1111-1111-1111-111111111111"
                user_b = "22222222-2222-2222-2222-222222222222"
                session.add_all([
                    ex6_models.Document(author_uuid=user_a, title="A: Welcome", content="Welcome document for A"),
                    ex6_models.Document(author_uuid=user_a, title="A: Notes", content="Private notes for A"),
                    ex6_models.Document(author_uuid=user_b, title="B: Welcome", content="Welcome document for B"),
                ])
                session.commit()

            has_users = session.query(ex7_models.User).first() is not None
            if not has_users:
                victim_uuid = "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
                attacker_uuid = "bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb"
                session.add_all([
                    ex7_models.User(uuid=victim_uuid, name="Victim"),
                    ex7_models.User(uuid=attacker_uuid, name="Attacker"),
                ])
                session.add_all([
                    ex7_models.Document(owner_uuid=victim_uuid, title="Victim Payroll", content="Salary details..."),
                    ex7_models.Document(owner_uuid=victim_uuid, title="Victim Secret", content="Secret plans..."),
                    ex7_models.Document(owner_uuid=attacker_uuid, title="Attacker Notes", content="Recon notes..."),
                ])
                session.commit()

            has_customers = session.query(ex8_models.Customer).first() is not None
            if not has_customers:
                session.add_all([
                    ex8_models.Customer(
                        name="Alice",
                        email="alice@example.com",
                        ssn="111-22-3333",
                        credit_card_number="4111111111111111",
                        api_key="alice-api-key-123",
                    ),
                    ex8_models.Customer(
                        name="Bob",
                        email="bob@example.com",
                        ssn="222-33-4444",
                        credit_card_number="5555555555554444",
                        api_key="bob-api-key-456",
                    ),
                ])
                session.commit()

            has_products = session.query(ex10_models.Product).first() is not None
            if not has_products:
                session.add_all([
                    ex10_models.Product(name="Widget", price_cents=1000, stock=5),
                    ex10_models.Product(name="Gadget", price_cents=2500, stock=2),
                ])
                session.commit()

            has_roles = session.query(ex12_models.Role).first() is not None
            if not has_roles:
                session.add_all([
                    ex12_models.Role(id=1, name="user"),
                    ex12_models.Role(id=2, name="admin"),
                ])
                session.commit()

            has_ex12_user = session.query(ex12_models.User).first() is not None
            if not has_ex12_user:
                session.add_all([
                    ex12_models.User(email="student@example.com", display_name="Student", role_id=1),
                ])
                session.commit()
    except SQLAlchemyError as exc:
        raise exc
