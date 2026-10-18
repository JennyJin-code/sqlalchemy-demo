from sqlalchemy import create_engine, text

database_url = "mysql+pymysql://jinjianying:vSthoEJI440UdYpn@mysql6.sqlpub.com:3311/jin_mysql"

# 1.创建引擎
engine = create_engine(
    database_url,
    echo=True,      # 打印SQL语句
    pool_size=5,    # 连接池大小
    max_overflow=10 # 最大溢出连接数
)


# 2.从引擎中获取会话
conn = engine.connect()

# 3.在会话中执行crud

#3.1老式代码
result  = conn.execute(text("SELECT 1"))
print("获取result",result.fetchone())
conn.close()

# 3.2 新式代码 python 上下文管理器。自动关闭连接 ✨
with engine.connect() as conn:
    result = conn.execute(text("select 'hello jjy'"))
    print("获取结果", result.fetchone())

# 插入多行数据【批量插入】： 变量 代码动态填充
#stat = text("insert into person(name, age, sex) values(:name, :age, :sex)") 
# with engine.connect() as conn:
#     conn.execute(text("""
#         create table if not exists person(
#             id int primary key auto_increment,
#             name varchar(50),
#             age int,
#             sex varchar(10)
#         )
#     """))
#     conn.execute(
#         stat,
#         [
#         {
#             "name": "jjn",
#             "age": 18,
#             "sex": "男"
#         },
#         {
#             "name": "jjy",
#             "age": 19,
#             "sex": "女"
#         }
#         ]
#     )
#     conn.execute(text("drop table if exists persion"))

    stmt2 = text("delete from person where id in (7,8,9,10,11,12,13,14)")
    conn.execute(stmt2)


    stmt1 = text("select * from person")
    # 执行SQL，得到 CursorResult 可迭代对象
    result = conn.execute(stmt1)

    # ========== 方式1：直接遍历result，row是Row对象【支持 .属性名 / 下标索引】 ==========
    print("=====方式1：直接遍历result，Row对象=====")
    for row in result:
        print(f"row: {row}")
        # 1. 通过属性名取值
        print(f"通过属性名获取结果: name: {row.name}, age: {row.age}")
        # 2. 通过索引下标取值（表列顺序：id是0号，name是1号，age是2号）
        print(f"通过索引获取结果: name: {row[1]}, age: {row[2]}")

    # ⚠️重要：CursorResult只能迭代一次！上面循环读完后result耗尽，下面演示要重新执行execute
    result = conn.execute(stmt1)

    # ========== 方式2：result.mappings() 遍历，返回字典Mapping【key是字符串列名】 ==========
    print("\n=====方式2：result.mappings() 返回字典映射 =====")
    for row in result.mappings():
        print(f"row: {row}")
        # 用字符串列名取值，类似字典
        print(f"通过key获取结果: name: {row['name']}, age: {row['age']}")

    result = conn.execute(stmt1)
    # ========== 方式3：元组解构（解包） ==========
    print("\n=====方式3：元组解构解包 ======")
    for id_, name, age, sex in result:
        print(f"通过元组解构获取结果: name: {name}, age: {age}")

    # ========== 方式4：all() 一次性取出全部列表（list[Row]） ==========
    result = conn.execute(stmt1)
    print("\n=====方式4：result.all() 取出所有行，返回列表=====")
    rows = result.all()
    print("rows全部数据：", rows)
    for r in rows:
        print(r.name, r.age)

    # ========== 方式5：fetchone() 循环，每次取一行（原生游标风格） ==========
    result = conn.execute(stmt1)
    print("\n=====方式5：fetchone() 逐行读取 ======")
    while row := result.fetchone():
        print(f"fetchone拿到：name={row.name}, age={row.age}")

    conn.commit()


