
-- we can pass separate schema for each table 
use catalog namaste_catalog ; 
use schema sdp ; 

CREATE OR REFRESH STREAMING TABLE namaste_catalog.sdp.orders_bronze 
TBLPROPERTIES ( 'pipelines.reset.allowed'=FALSE)
AS
select * , _metadata.file_name as source_file
from stream read_files (
'${source}/csv' , 
format => 'CSV' , 
header => True ) ;


CREATE OR REFRESH STREAMING TABLE namaste_catalog.sdp.orders_silver
AS
select order_id,customer_id,cast(order_date as date) as order_date,amount,city ,source_file, current_timestamp as ingestion_timestamp 
from stream orders_bronze 
where _rescued_data is null ;

CREATE OR REFRESH STREAMING TABLE namaste_catalog.sdp.orders_silver_with_constrainsts   
( 
constraint  con1 expect  (amount between 0 and 10000) on violation drop row  , 
constraint  con2  expect ( len(city) >  1  )  on violation  fail update ,
constraint  con3 expect ( len(source_file) >  0  ) on violation fail update 
)  
AS
select order_id,customer_id,cast(order_date as date) as order_date,amount,city,source_file, current_timestamp as ingestion_timestamp
from  stream orders_bronze
;


create materialized view namaste_catalog.sdp.orders_by_date_gold
as
select order_date, sum(amount) as total_amount
, count(distinct customer_id) as total_customers
, count(*) as no_of_orders      --,avg(amount) as avg_amount
from orders_silver
group by order_date;

