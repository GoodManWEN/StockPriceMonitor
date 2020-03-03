from sqlalchemy import create_engine, ForeignKey 
from sqlalchemy import text as sqltext
from sqlalchemy import Column, Integer , SmallInteger, String , Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from os import path



class SQLhandler:

	Base = declarative_base()
	class Tasks(Base):
		__tablename__ = 'tasks'
		taskid = Column(Integer, primary_key=True ,autoincrement=True)
		stocknum = Column(String(20) ,nullable=False)
		targetprice = Column(Float ,nullable=False)
		incdesc = Column(SmallInteger ,nullable=False)
		isover = Column(SmallInteger ,nullable=False , default=0)
		currentprice = Column(Float ,nullable=False,default = 0)
		lastupdatetime = Column(String(26) ,nullable=False,default = "1971-01-01 08:00:00+08:00")

		def __str__(self):
			return f'Tasks(taskid = {self.taskid} , stocknum = {self.stocknum} , targetprice = {self.targetprice} , incdesc = {self.incdesc} , isover = {self.isover} , currentprice = {self.currentprice}) , lastupdatetime = { self.lastupdatetime }'

		def __repr__(self):
			return self.__str__()


	def __init__(self , database_name = 'foo.db'):
		self._working_path = path.dirname(path.abspath(__file__))
		self._database_path = path.join(self._working_path , database_name)
		self.base = SQLhandler.Base
		self.engine = create_engine(f'sqlite:///{self._database_path}', echo=False)
		self.base.metadata.create_all(self.engine)
		self.session = sessionmaker(bind = self.engine)
		self.single_session = self.session()

	def _convert_tablename_into_class(self , table_name):
		for target_table in self.base.__subclasses__():
			if target_table.__name__ == table_name:
				return target_table
		else:
			return False

	def insert_row(self , table_name , **kwargs):
		try:
			target_table = self._convert_tablename_into_class(table_name)
			assert target_table != False
			append_ = target_table(**kwargs)
			self.single_session.add(append_)
			self.single_session.commit()
			return True
		except:
			self.single_session.rollback()
			return False

		return target_table

	def flush_all(self , table_name):
		try:
			target_table = self._convert_tablename_into_class(table_name)
			assert target_table != False
			rownum = self.single_session.query(target_table).delete()
			self.single_session.commit()
			return rownum
		except:
			self.single_session.rollback()
			return False

	def query(self , table_name , filter_expr):
		try:
			target_table = self._convert_tablename_into_class(table_name)
			assert target_table != False
			return self.single_session.query(target_table).filter(filter_expr)
		except:
			self.single_session.rollback()
			return False

	def delete(self , query_result):
		try:
			row_num = query_result.delete()
			self.single_session.commit()
			return row_num
		except:
			self.single_session.rollback()
			return False

	def query_and_delete(self , table_name , filter_expr):
		try:
			target_table = self._convert_tablename_into_class(table_name)
			assert target_table != False
			row_num = self.single_session.query(target_table).filter(filter_expr).delete()
			self.single_session.commit()
			return row_num
		except:
			self.single_session.rollback()
			return False

	def query_and_update(self , table_name , query_col , ornval , **kwargs):
		try:
			target_table = self._convert_tablename_into_class(table_name)
			assert target_table != False
			assert hasattr(target_table , query_col)
			query_target_col = getattr(target_table , query_col)
			query_res = self.single_session.query(target_table).filter(query_target_col == ornval).one()
			for modify_col , newval in kwargs.items():
				assert hasattr(query_res , modify_col)
				setattr(query_res , modify_col , newval)
			self.single_session.commit()
			return True
		except Exception as e:
			self.single_session.rollback()
			return False

	def show_recent_100(self , table_name , order_by , limit = 100):
		try:
			target_table = self._convert_tablename_into_class(table_name)
			assert target_table != False
			assert hasattr(target_table , order_by)
			query_target_col = getattr(target_table , order_by)
			return self.single_session.query(target_table).order_by(query_target_col.desc()).limit(limit).all()
		except Exception as e:
			self.single_session.rollback()
			return False

	def get_all_monitor_target(self):
		return self.single_session.query(SQLhandler.Tasks).filter(SQLhandler.Tasks.isover == 0).all()

	def print_all(self , table_name):
		try:
			target_table = self._convert_tablename_into_class(table_name)
			assert target_table != False
			rows = self.single_session.query(target_table).all()
			print(f'Table : {target_table.__name__}')
			for row in rows:
				print('  ',end='')
				print(row)
		except:
			self.single_session.rollback()
			return False

	def _example(self):
		'''
		这里都是接口使用范例 ,简单写 , 实现比较混乱 , 怕忘了。
		

		1、新增
		print(sql.insert_row('Tasks' ,stocknum='000055', targetprice=6.22 ,incdesc = 0))
		print(sql.insert_row('Tasks' ,stocknum='000056', targetprice=6.22 ,incdesc = 0))
		print(sql.insert_row('Tasks' ,stocknum='000057', targetprice=6.22 ,incdesc = 0))
		print(sql.insert_row('Tasks' ,stocknum='000058', targetprice=6.22 ,incdesc = 0))

		2、查询
		sql.query('Tasks',Tasks.taskid >= 3)

		3、删除 ， 输入一个查询对象
		sql.delete(sql.query('Tasks',Tasks.taskid >= 3))

		4、查询并删除
		sql.query_and_delete('Tasks',Tasks.taskid >= 3)

		5、删除全部
		sql.flush_all('Tasks')

		6、打印全部，查看状态
		sql.print_all('Tasks')

		7、查询并更新
		sql.query_and_update('Tasks' , 'taskid' , 2 , stocknum = 600060 , isover = 1)
		'''
		pass


if __name__ == '__main__':
	# for testing.
	sql = SQLhandler()
	print(sql.insert_row('Tasks' ,stocknum='000055', targetprice=6.22 ,incdesc = 0 ))
	print(sql.insert_row('Tasks' ,stocknum='000056', targetprice=6.22 ,incdesc = 0,isover = 1))
	print(sql.insert_row('Tasks' ,stocknum='000057', targetprice=6.22 ,incdesc = 0,isover = 1))
	print(sql.insert_row('Tasks' ,stocknum='000058', targetprice=6.22 ,incdesc = 0 ,isover = 0))

	print(sql.query_and_update('Tasks' , 'taskid' , 2 , stocknum = 666660 , lastupdatetime = 'abc'))

	sql.print_all('Tasks')
	# print(sql.show_recent_100('Tasks','taskid'))
	# print(sql.get_all_monitor_target())
	print(sql.flush_all('Tasks'))
