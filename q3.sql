select t1.writer
from tweets t1, tweets t2, tweets t3
where t1.writer=t2.writer and t2.writer=t3.writer and t1.tdate > t2.tdate and
        t2.tdate > t3.tdate and lower(t1.text) like '%edmonton%' and
        lower(t2.text) like '%edmonton%' and lower(t3.text) like '%edmonton%'
except
select flwee
from follows;
