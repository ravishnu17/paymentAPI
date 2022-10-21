from sqlalchemy import Column , Integer , String , Float
from DBConnection.dbConnection import Base
class PaymentData(Base):
    __tablename__ = "paymentDetails"
    id = Column(Integer , primary_key = True , nullable = False)
    firstname = Column(String , nullable = False)
    lastname = Column(String , nullable = False)
    email = Column(String , nullable = False)
    paid_to = Column(String , nullable = False)
    paypal_id = Column(String , nullable= False)
    refund_link = Column(String , nullable = False)
    amount = Column(Float , nullable = False)