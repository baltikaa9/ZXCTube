from crud import CRUDBase
from models import UserDB
from schemas import UserCreate


class CRUDUser(CRUDBase[UserDB, UserCreate]):
    ...
