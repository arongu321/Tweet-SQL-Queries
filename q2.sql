select distinct f1.flwer
from follows f1, follows f2, users u
where f1.flwee= f2.flwee and f2.flwer=u.usr and lower(u.name) ='john doe' and
julianday('now')-julianday(f1.start_date)>=90 and 
julianday('now')-julianday(f2.start_date)<90;
