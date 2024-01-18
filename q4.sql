   select distinct usr, name
   from users u, tweets t1, tweets t2
   where u.usr=t1.writer and u.usr=t2.writer and t1.tdate != t2.tdate
   and not exists (select flwee
		     from follows f1, users u1
		     where f1.flwer=u1.usr and lower(u1.name)='john doe'
		     except
		     select flwee
		     from follows f2
		     where f2.flwer=u.usr);