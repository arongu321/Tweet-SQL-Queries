  drop view if exists tStat;
  create view tStat (writer, tdate, text, rep_cnt, ret_cnt, sim_cnt) as
  select t.writer, t.tdate, t.text, count(distinct t2.writer || t2.tdate),
         count(distinct r.usr), count(distinct m2.writer || m2.tdate)
  from (((tweets t left outer join tweets t2 on t.writer=t2.replyto_w and 
         t.tdate=t2.replyto_d)
         left outer join retweets r on t.writer=r.writer and t.tdate=r.tdate)
        left outer join mentions m on t.writer=m.writer and t.tdate=m.tdate)
        left outer join mentions m2 on m.term=m2.term 
  group by t.writer, t.tdate, t.text;
    with R(usr,rcnt_avg) as (
    select writer, avg(ret_cnt)
    from tStat s
    group by writer),
  F(usr, fcnt) as (
    select flwee, count(*)
    from follows
    group by flwee)
  select usr, 'top in retweets'
  from R
  where rcnt_avg >= (select max(rcnt_avg) from R)
  union
  select usr, 'top in followers'
  from F
  where fcnt >= (select max(fcnt) from F);
