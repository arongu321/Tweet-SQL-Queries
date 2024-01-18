select writer
from tweets
intersect
select flwee
from follows
intersect
select member
from includes;
