select p.uuid,
       p.name,
       p.email,
       p.is_bot,
       p.country_code,
       o.name
from profiles p
left outer join enrollments e on e.uuid = p.uuid
left outer join organizations o on o.id = e.organization_id;

