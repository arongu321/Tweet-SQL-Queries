   select lname
   from includes l
   group by lname
   having count(*) >6 and 0.5*count(*) <=
      (select count(distinct member)
       from includes l2, follows f, users u
       where l2.lname=l.lname and l2.member=f.flwer and f.flwee=u.usr
             and lower(u.name)='john doe');
