
import cx_Oracle

# Connect as user "hr" with password "welcome" to the "oraclepdb" service running on this computer.
# ip = '10.211.55.2'
# port = 11521
# SID = 'orcl'
# dsn_tns = cx_Oracle.makedsn(ip, port, SID)
# connection = cx_Oracle.connect("sys", "orcl_01", dsn_tns,
#                                mode=cx_Oracle.SYSDBA)
#                                #, purity=cx_Oracle.ATTR_PURITY_SELF)
connection = cx_Oracle.connect("sys/orcl_01@//10.211.55.2:11521/orcl",
                               mode=cx_Oracle.SYSDBA)

cursor = connection.cursor()
cursor.execute("""
SELECT
  table_name
FROM
  user_tables
ORDER BY
  table_name""")
for tname in cursor:
    print("Table: ", tname)
