import pymysql
import time
import datetime

ts = time.time()
timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
# micropda
# connection = pymysql.connect(host="localhost",
#                      user="root",
#                      passwd="",
#                      db="SocialPda")
#
#
# try:
#     with connection.cursor() as cursor:
#         # Create a new record
#         sql = "INSERT INTO `SocialPDA`.`micropda` (`dataset`, `Beta`, `l`, `date`, `k`, `delta`, `omega_cluster`, `run`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
#         cursor.execute(sql, ('test', '1.0', '30', '2017-11-09', '5', '2', 'ghjsdvf;gsdf;kbsdfbjk', '1'))
#     connection.commit()
# finally:
#     connection.close()


#particlepda
# connection = pymysql.connect(host="localhost",
#                      user="root",
#                      passwd="",
#                      db="SocialPda")
#
# try:
#     with connection.cursor() as cursor:
#         # Create a new record
#         sql = "INSERT INTO `SocialPDA`.`particlepda` (`dataset`, `beta`, `k`, `delta`, `run`, `l`, `date`, `f1`, `f2`, `f`, `bestPosition`, `Iteration`) VALUES  (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
#         cursor.execute(sql, ('test', '1', '5', '2', '1', '30', '2017-11-15', '1', '230', '182.2', '[11111111119761786120376123791623-971263-9761239612939-1236-912763-971263-971263-912763-91726]', '3'))
#     connection.commit()
# finally:
#     connection.close()

#swarmpdacluster
# connection = pymysql.connect(host="localhost",
#                      user="root",
#                      passwd="",
#                      db="SocialPda")
#
#
# try:
#     with connection.cursor() as cursor:
#         # Create a new record
#         sql = "INSERT INTO `SocialPDA`.`swarmpdacluster` (`beta`, `dataset`, `date`, `delta`, `k`, `l`, `omega_cluster_rho`, `run`) VALUES  (%s,%s,%s,%s,%s,%s,%s,%s)"
#         cursor.execute(sql, ('1', 'test', '2017-11-01', '2', '5', '30', '[adajsbdak;fbs;kfbsd;kfdf;kbdsf;kbfksadbf;knasbf;knasdbfaksnbfsdknbfsd;knbfsad;knfbsd''kfba''knfb]', '2'))
#     connection.commit()
# finally:
#     connection.close()

#
#swarmPda
# connection = pymysql.connect(host="localhost",
#                      user="root",
#                      passwd="",
#                      db="SocialPda")
#
#
# try:
#     with connection.cursor() as cursor:
#         # Create a new record
#         sql = "INSERT INTO `SocialPDA`.`swarmPda` (`beta`, `dataset`, `date`, `g`, `Iteration`, `k`, `l`, `run`) VALUES  (%s,%s,%s,%s,%s,%s,%s,%s)"
#         cursor.execute(sql, ('1', 'test', '2017-11-08', '12.1', '14', '5', '2', '2'))
#     connection.commit()
# finally:
#     connection.close()

#measure
# connection = pymysql.connect(host="localhost",
#                      user="root",
#                      passwd="",
#                      db="SocialPda")
#
#
# try:
#     with connection.cursor() as cursor:
#         # Create a new record
#         sql = "INSERT INTO `SocialPDA`.`measure` (`Beta`, `dataset`, `date`, `delta`, `k`, `l`, `run`, `harmonic`, `subgraph`, `modularity`, `transitivity`) VALUES  (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
#         cursor.execute(sql, ('0.4', 'test',timestamp, '5', '10', '30', '2', '323232.2323', '23232.323', '2323.223', '0000.2323'))
#     connection.commit()
# finally:
#     connection.close()

