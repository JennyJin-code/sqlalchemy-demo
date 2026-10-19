from typing import Optional
from sqlalchemy import create_engine, text, Column, Integer, String
from sqlalchemy.orm import DeclarativeBase, Session, Mapped, mapped_column, sessionmaker
from sqlalchemy import delete, update, insert, select

database_url = "mysql+pymysql://jinjianying:vSthoEJI440UdYpn@mysql6.sqlpub.com:3311/jin_mysql"

#1.创建引擎
engine = create_engine(
    database_url,
    echo=True,      # 打印SQL语句
    pool_size=5,    # 连接池大小
    max_overflow=10 # 最大溢出连接数
)

# 2. 定义基类
class Base(DeclarativeBase):
    pass

## 3. 创建模型类
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50))
    age: Mapped[Optional[int]] = mapped_column(Integer, default=0)
    fullname: Mapped[str] = mapped_column(String(30))
    nickname: Mapped[Optional[str]] = mapped_column(String(30), default=None)

    def __repr__(self):
        return f"User(id={self.id}, name={self.name}, age={self.age}, fullname={self.fullname}, nickname={self.nickname})"

## 3. 自动创建数据表
# Base.metadata.create_all(engine)
# 先删表（测试常用）
#Base.metadata.drop_all(engine)
# 再建表
Base.metadata.create_all(engine)

print("数据表创建成功...")


## 1. 新增用户
# def insert_user():
#     ### 1. 创建会话
#     with Session(engine) as session:
#         ### 2. 创建模型实例
#         user = User(
#             name="张三",
#             age=18,
#             fullname="张三",
#             nickname="zhangsan",
#         )
#         ### 3. 新增用户
#         session.add(user)
#         ### 4. 提交事务
#         session.commit()
#     print("新增用户成功...")

def insert_user(user: User):
    ### 1. 创建会话； session 中直接封装了所有的 CRUD 功能
    with Session(engine) as session:
        ### 3. 新增用户
        session.add(user)
        ### 4. 提交事务
        session.commit()
    print("新增用户成功...")

insert_user(User(name="李四", age=19, fullname="李四", nickname="lisi"))
insert_user(User(name="王五", age=20, fullname="王五", nickname="wangwu"))
insert_user(User(name="赵六", age=33, fullname="赵六", nickname="zhaoliu"))

from sqlalchemy import select


# 查询所有用户  适用session提供的query/get函数
def query_user():
    with Session(engine) as session:
        stmt = select(User)
        users = session.scalars(stmt).all()

    for user in users:
        print("用户信息：", user)

query_user()


# 查询指定用户
def query_user1():
    with Session(engine) as session:
        user = session.get(User, 2)
        user = session.query(User).filter(User.id == 2).first()
        print("查询用户: ", user)

query_user1()

def query_user2():
    with Session(engine) as session:
        users = session.query(User).filter(User.age > 19).order_by(User.age).all()

        for user in users:
            print("用户信息: ", user)

query_user2()     

 ### 2. 方式2：使用select() 写类似的sql语句，让session执行
# select * from users where age>18 and name like ? order by age
def query_user3():
    with Session(engine) as session:
        stmt = select(User).where(User.age > 18).where(User.name.like("%三%")).order_by(User.age)
        users = session.execute(stmt).scalars().all()

        for user in users:
            print("用户信息: ", user)   
query_user3()

#修改
# def update_user(user_id: int, age: int):
#     with Session(engine) as session:
#         # 两套API。
#         ## 1. sql api。从 select()/update()/delete()/insert() 开始自己拼
#         stmt = update(User).where(User.id == user_id).values(age=age)
#         session.execute(stmt)
#         session.commit()
#         print("更新用户成功...")
# update_user(2, 88)


def update_user(user_id: int, age: int):
    with Session(engine) as session:
        # 两套API。
        ## 1. sql api。从 select()/update()/delete()/insert() 开始自己拼
        ## 2. session api。直接使用 session 提供的功能
        user = session.get(User, user_id)
        if user:
            # 修改对象的属性值
            user.age = age
            # 重新保存对象
            session.add(user)
        else:
            print("用户不存在...")

        session.commit()
        print("更新用户成功...")
update_user(2, 88)


#删除
def delete_user_sql(user_id: int):
    with Session(engine) as session:
        stmt = delete(User).where(User.id == user_id)
        session.execute(stmt)
        session.commit()
        print("删除用户成功...")
delete_user_sql(2)


#脏追踪
def query_user(user_id: int):
    with Session() as session:
        user = session.get(User, user_id)
        if user:
            print(user)
            user.age = 99
        else:
            print("用户不存在...")
        session.commit()

query_user(1)
