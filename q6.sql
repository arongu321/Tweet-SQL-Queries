   select t.writer, t.tdate, t.text
   from tweets t, (
   select writer, tdate, rank () over (order by count(*) desc) as rnk
   from retweets
   group by writer, tdate) r
   where t.writer=r.writer and t.tdate=r.tdate and rnk <=3;
