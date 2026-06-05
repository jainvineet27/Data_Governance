create streaming table if not exists   namaste_catalog.sdp.customers
select *,_metadata.file_name as file_name , current_timestamp() as ingest_timestamp 
from stream read_files( "${source}/customers", format=> 'JSON') ; 


create streaming table if not exists  namaste_catalog.sdp.orders
select *,_metadata.file_name as file_name , current_timestamp() as ingest_timestamp 
from stream read_files("${source}/orders", format=> 'JSON') ; 



create streaming table if not exists  namaste_catalog.sdp.silver_customers
select customer_name, city, customer_id , cast(updated_at as date) ,file_name, ingest_timestamp 
from stream customers ; 


create streaming table if not exists  namaste_catalog.sdp.silver_orders
select amount ,city, customer_id , date(order_date),order_id ,file_name, ingest_timestamp 
from stream orders ; 


create materialized view namaste_catalog.sdp.full_order_info_gold
as 
select  so.order_id ,so.amount , so.city , sc.customer_name ,so.file_name as order_file_name , sc.file_name as customer_file_name
from  silver_orders so 
inner join silver_customers sc
on so.customer_id  = sc.customer_id ; 

CREATE STREAMING TABLE orders_silver_violation_chk
(
CONSTRAINT valid_amount EXPECT (amount > 0),
CONSTRAINT valid_order_date EXPECT (order_date is not null) 
on violation drop row,
CONSTRAINT valid_customer_id EXPECT (customer_id is not null) ON VIOLATION fail UPDATE
)
select order_id, date(order_date) as order_date, customer_id, amount, city, file_name, ingest_timestamp
from stream orders 
