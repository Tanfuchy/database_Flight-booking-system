/*
HOTELS(String location, int price, int numRooms, int numAvail)；
BUS(String location, int price, int numBus, int numAvail)；
CUSTOMERS(String custName,custID)；
RESERVATIONS(String custName, int resvType, String resvKey) 

FLIGHTS (String flightNum, int price, int numSeats, int numAvail, String FromCity, String ArivCity)；
HOTELS(String hotelNum,String location, int price, int numRooms, int numAvail)；
BUS(String BusNum（bus编号）,String location, int price, int numBus(剩余座位数), int numAvail)；
CUSTOMERS(int custID,String custName)；
RESERVATIONS(String resvNum,String custID, int resvType, String resvKey)；
*/

# 创建数据库
create database TourBooking;
use TourBooking;

# 创建航班表
create table FLIGHTS(
	flightNum	varchar(5) not null, # 航班号
	price		int check(price>0),  # 价格
	numSeats	int check(numSeats>0), # 总座位数量
	numAvail	int, # 剩余可用座位
	FromCity	varchar(20), # 出发地点
	ArivCity	varchar(20), # 到达地点
	primary key(flightNum));  # 航班号是主码

# 创建大巴班车表
create table BUS(
	busNum      varchar(5) not null, # 大巴班次
	location	varchar(50) not null, # 地点
	price		int check(price>0), # 价格
	numSeats	int check(numSeats>0), # 总座位数量
	numAvail	int, # 剩余座位数量 
	primary key(busNum));
    
# 创建宾馆房间表
create table HOTELS(
	hotelNum	varchar(5) not null, # 宾馆号
	location	varchar(50), # 地点
	price		int check(price>0), # 价格 
	numRooms	int check(numRooms>0), # 总房间数量
	numAvail	int, # 剩余可用房间数量
	primary key(hotelNum));

# 创建客户数据表
create table CUSTOMERS(
	custID		varchar(5) not null, # 用户id
	custName	varchar(10) not null, # 用户名
    password	varchar(20) NOT NULL, # 密码
	primary key(custID));
	
# 创建预定表
create table RESERVATIONS(
	resvNum		    varchar(5) not null, # 序号
	custID		    varchar(5) not null, # 用户id
	resvType	    int check(resvType in (1, 2, 3)), # 预定类型 
	flight_resvKey  varchar(5) , # 飞机的航班号
    bus_resvKey     varchar(5) , # 大巴的班次 
    hotel_resvKey   varchar(5) , # 宾馆号 一行数据其实这三个只能有一个起作用
    location		varchar(20) DEFAULT NULL, # 地点说明
    foreign key(flight_resvKey) references FLIGHTS(flightNum),
    foreign key(bus_resvKey) references BUS(busNum),
    foreign key(hotel_resvKey) references HOTELS(hotelNum),
	primary key(resvNum));
	
