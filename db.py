import sqlite3
import threading

lock = threading.Lock()



class DB:
	def __init__(self, database):

		self.connection = sqlite3.connect(database, check_same_thread = False)
		self.cursor = self.connection.cursor()

	def check_user(self, uid):
		# Проверка на наличие пользователя в БД.
		with self.connection:
			with lock:
				result = self.cursor.execute('SELECT * FROM `user` WHERE `uid` = ?', (uid,)).fetchall()
				return bool(result)
			
	def check_admin(self, uid):
		# Проверка на наличие пользователя в списке администраторов.
		with self.connection:
			with lock:
				result = self.cursor.execute('SELECT * FROM `admins` WHERE `id` = ?', (uid,)).fetchall()
				return bool(result)
			
	def get_admins(self):
		# Получения списка всех книг.
		with self.connection:
			with lock:
				return self.cursor.execute("SELECT * FROM `admins`").fetchall()
			
	def delete_admin(self, id):
		# Удаление админа
		with self.connection:
			with lock:
				result = self.cursor.execute('DELETE FROM `admins` WHERE `id` = ?;', (id,)).fetchone()

	def add_admin(self, uid):
		# Добавление пользователя в БД.
		with self.connection:
			with lock:
				return self.cursor.execute("INSERT INTO `admins` (`id`) VALUES(?)", (uid,))

	def add_user(self, uid, un, name):
		# Добавление пользователя в БД.
		with self.connection:
			with lock:
				return self.cursor.execute("INSERT INTO `user` (`uid`, `un`, `name`) VALUES(?,?,?)", (uid, un, name,))

	def get_user(self, uid):
		# Получение строки пользователя по ID.
		with self.connection:
			with lock:
				result = self.cursor.execute('SELECT * FROM `user` WHERE `uid` = ?', (uid,)).fetchone()
				return result

	def set_status(self, uid, status):
		# Присвоение состояния пользователю.
		with self.connection:
			with lock:
				return self.cursor.execute("UPDATE `user` SET `status` = ? WHERE `uid` = ?", (status, uid,))

	def get_status(self, uid):
		# Получения статуса пользователя.
		with self.connection:
			with lock:
				return self.cursor.execute("SELECT `status` FROM `user` WHERE `uid` = ?", (uid,)).fetchone()[0]
			
	def set_ban(self, uid, banned):
		# Присвоение состояния пользователю.
		with self.connection:
			with lock:
				return self.cursor.execute("UPDATE `user` SET `is_banned` = ? WHERE `uid` = ?", (banned, uid,))
			
			
	def get_all_channels(self):
		# Получения списка всех книг.
		with self.connection:
			with lock:
				return self.cursor.execute("SELECT * FROM `chans`").fetchall()
	
	def get_chan(self, id):
		# Получение строки канала по ID.
		with self.connection:
			with lock:
				return self.cursor.execute('SELECT * FROM `chans` WHERE `id` = ?', (id,)).fetchone()
				
			
	def add_chan(self, id, name, ch_type, link):
		# Добавление пользователя в БД.
		with self.connection:
			with lock:
				return self.cursor.execute("INSERT INTO `chans` (`id`, `name`, `type`, `link`) VALUES(?,?,?,?)", (id, name, ch_type, link))
			
	def delete_chan(self, id):
		# Получение строки канала по ID.
		with self.connection:
			with lock:
				result = self.cursor.execute('DELETE FROM `chans` WHERE `id` = ?;', (id,)).fetchone()

	def set_chan_name(self, uid, name):
		# Присвоение состояния пользователю.
		with self.connection:
			with lock:
				return self.cursor.execute("UPDATE `chans` SET `name` = ? WHERE `id` = ?", (name, uid,))