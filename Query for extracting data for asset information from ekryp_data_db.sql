# Query for asset_information
select 
i.customer_asset_identifier,i.serial_number,i.installed_date, f.model_name,f.model_group_id,
f.category_id,f.type_id, f.capacity, s.service_provider,r.site_name, r.ekryp_partner_id, c.company_name 
from service_order_record as s 
INNER JOIN asset_ib_info as i ON s.id = i.id 
inner join asset_features as f on f.id = s.id 
inner join  site_record as r on r.id = s.id 
inner join company_record as c on i.id = c.id;


select 
i.customer_asset_identifier,i.serial_number,i.installed_date, f.model_name,f.model_group_id,
f.category_id,f.type_id, f.capacity, s.service_provider,r.site_name, r.ekryp_partner_id, c.company_name 
from service_order_record as s,
asset_ib_info as i,
asset_features as f, 
site_record as r,
company_record as c;


select * from site_record;

select * from asset_features;

select * from service_order_record;
select * from asset_ib_info;
select * from company_record;

select code, code_mapped_id from asset_codes;
select * from Asset_information;
select
i.customer_asset_identifier,i.serial_number,i.installed_date, f.model_name,f.model_group_id,
f.category_id,f.type_id, f.capacity, s.service_provider,r.site_name, r.ekryp_partner_id, c.company_name 
from service_order_record as s 
inner join asset_ib_info as i ON s.service_provider = i.service_provider_id 
inner join asset_features as f on f.ekryp_partner_id = s.ekryp_partner_id
inner join  site_record as r on r.site_id = i.site
inner join company_record as c on i.customer_id = c.company_id;