# 预定后
-- delimiter $
-- create trigger update_insert after insert on RESERVATIONS for each row
-- begin
-- 	if new.resvType = 1 then 
--     update FLIGHTS set numAvail = numAvail - 1 where	new.resvType = 1 and flightNum = new.flight_resvKey;
--     elseif new.resvType = 2 then 
--     update	HOTELS set numAvail = numAvail - 1  where new.resvType = 2 and hotelNum = new.hotel_resvKey;
--     elseif new.resvType = 3 then 
--     update	BUS set numAvail = numAvail - 1 where new.resvType = 3 and busNum = new.bus_resvKey;
--     end if;
-- end $
-- delimiter ;

# 更新航班信息
create trigger flight_update after insert on RESERVATIONS
for each row
update	FLIGHTS
set		numAvail = numAvail - 1
where	new.resvType = 1 and flightNum = new.flight_resvKey;

# 更新大巴信息
create trigger bus_update after insert on RESERVATIONS
for each row
update	BUS
set		numAvail = numAvail - 1
where	new.resvType = 2 and busNum = new.bus_resvKey;

# 更新宾馆信息
create trigger hotel_update after insert on RESERVATIONS
for each row
update	HOTELS
set		numAvail = numAvail - 1
where	new.resvType = 3 and hotelNum = new.hotel_resvKey;


# 取消预定后
# 更新航班信息
create trigger flight_update2 after delete on RESERVATIONS
for each row
update	FLIGHTS
set		numAvail = numAvail + 1
where	old.resvType = 1 and flightNum = old.flight_resvKey;

# 更新大巴信息
create trigger bus_update2 after delete on RESERVATIONS
for each row
update	BUS
set		numAvail = numAvail + 1
where	old.resvType = 2 and busNum = old.bus_resvKey;

# 更新宾馆信息
create trigger hotel_update2 after delete on RESERVATIONS
for each row
update	HOTELS
set		numAvail = numAvail + 1
where	old.resvType = 3 and hotelNum = old.hotel_resvKey;
