select * from error_codes;
select * from Asset_information;

select * from error_code_feature_def;
select * from asset_ib_info;

select 
i.customer_asset_identifier,i.serial_number,i.installed_date, f.model_name,f.model_group_id,
f.category_id,f.type_id, f.capacity, i.service_provider_id,r.site_name, r.ekryp_partner_id, c.company_name 
from  asset_ib_info as i 
outer join asset_features as f on f.id = i.id
inner join company_record as c on i.customer_id = c.company_id
inner join  site_record as r on r.site_id = i.site;