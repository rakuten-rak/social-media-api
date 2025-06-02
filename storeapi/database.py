import databases
import sqlalchemy
from storeapi.config import config


# HERE CREATE OUR TABLE IN THE DATABASE
metadata = sqlalchemy.MetaData()

post_table  = sqlalchemy.Table(
    "posts",
    metadata,
    sqlalchemy.Column("id",sqlalchemy.Integer,primary_key=True),
    sqlalchemy.Column("body", sqlalchemy.String)
)

user_table = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id",sqlalchemy.Integer,primary_key=True),
    sqlalchemy.Column("email",sqlalchemy.String,unique=True),
    sqlalchemy.Column("password",sqlalchemy.String),
)


comment_table  = sqlalchemy.Table(
    "comment",
    metadata,
    sqlalchemy.Column("id",sqlalchemy.Integer,primary_key=True),
    sqlalchemy.Column("body", sqlalchemy.String),
    sqlalchemy.Column("post_id", sqlalchemy.ForeignKey("posts.id"), nullable=False)
)

engine = sqlalchemy.create_engine(
    config.DATABASE_URL, connect_args={"check_same_thread": False}
)

metadata.create_all(engine)
database = databases.Database(
    config.DATABASE_URL, force_rollback=config.DB_FORCE_ROLL_BACK
)
