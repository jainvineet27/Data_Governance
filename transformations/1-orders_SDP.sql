-- we can pass separate schema for each table 
CREATE STREAMING TABLE orders_bronze
select * ,
_metadata.file_name as source_file,
current_timestamp as ingestion_timestamp
from stream read_files (
'${source}/csv',
format => 'CSV' , 
header =>True
) ;

CREATE STREAMING TABLE orders_silver
select order_id,customer_id,order_date,amount,city ,source_file, ingestion_timestamp
from stream orders_bronze ; 
--where _rescued_data is null

create materialized view orders_by_date_gold
as
select order_date, sum(amount) as total_amount
, count(distinct customer_id) as total_customers
, count(*) as no_of_orders      --,avg(amount) as avg_amount
from orders_silver
group by order_date;


