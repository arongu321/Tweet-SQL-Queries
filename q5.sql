   select t.writer, t.tdate, t.text
   from tweets t, follows f, retweets r
   where t.writer=f.flwee and r.usr=f.flwer and t.tdate=r.tdate
   group by t.writer, t.tdate, t.text
   having count(distinct f.flwer) >=3;
